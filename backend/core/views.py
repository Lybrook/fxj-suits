import re
import uuid
from typing import Any

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import get_value, normalize_payload, payload_id
from .models import Document, GenericRecord, UserProfile
from .serializers import DocumentSerializer, GenericRecordSerializer, UserSerializer

ALLOWED_TABLES = {
    "users",
    "transactions",
    "court_cases",
    "clients",
    "letters",
    "tasks",
    "invoices",
    "expenses",
    "draft_requests",
    "filing_requests",
    "land_titles",
    "land_title_notes",
    "requisitions",
    "notifications",
    "comm_logs",
    "push_subscriptions",
}


def _validate_table(table: str) -> None:
    if table not in ALLOWED_TABLES or not re.fullmatch(r"[a-z_]+", table):
        raise ValueError("Unsupported table")


def _records_for_table(table: str):
    return GenericRecord.objects.filter(table=table)


def _record_response(record: GenericRecord) -> dict[str, Any]:
    payload = dict(record.payload or {})
    payload.setdefault("id", record.record_id)
    return payload


def _with_land_title_notes(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    notes = list(_records_for_table("land_title_notes"))
    by_title: dict[str, list[dict[str, Any]]] = {}
    for note in notes:
        payload = _record_response(note)
        title_id = str(payload.get("title_id") or payload.get("titleId") or "")
        by_title.setdefault(title_id, []).append(payload)
    for record in records:
        record["notes_history"] = by_title.get(str(record.get("id")), [])
    return records


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = str(request.data.get("password", ""))
        user = UserProfile.objects.filter(email__iexact=email).first()
        if not user or not user.password_hash or not check_password(password, user.password_hash):
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"token": user.auth_token, "user": UserSerializer(user).data})


class MeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.headers.get("Authorization", "").replace("Token ", "").strip()
        user = UserProfile.objects.filter(auth_token=token).first() if token else None
        if not user:
            return Response({"user": None})
        return Response({"user": UserSerializer(user).data})


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Token ", "").strip()
        UserProfile.objects.filter(auth_token=token).update(auth_token=uuid.uuid4().hex)
        return Response({"success": True})


class TableView(APIView):
    permission_classes = [AllowAny]

    def dispatch(self, request, *args, **kwargs):
        try:
            _validate_table(kwargs["table"])
        except ValueError:
            return Response({"detail": "Unsupported table."}, status=status.HTTP_404_NOT_FOUND)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, table: str):
        if table == "users":
            users = UserProfile.objects.all()
            email = request.query_params.get("email")
            role = request.query_params.get("role")
            if email:
                users = users.filter(email__iexact=email)
            if role:
                users = users.filter(role=role)
            data = UserSerializer(users, many=True).data
            return Response(data)

        records = list(_records_for_table(table))
        for key, expected in request.query_params.items():
            if key in {"order", "ascending", "limit", "offset"}:
                continue
            records = [record for record in records if str(get_value(record.payload or {}, key, "")) == str(expected)]
        order_key = request.query_params.get("order")
        if order_key:
            records.sort(key=lambda record: str(get_value(record.payload or {}, order_key, "")), reverse=request.query_params.get("ascending") == "false")
        offset = max(int(request.query_params.get("offset", "0")), 0)
        limit = request.query_params.get("limit")
        sliced = records[offset: offset + int(limit)] if limit else records[offset:]
        data = [_record_response(record) for record in sliced]
        if table == "land_titles":
            data = _with_land_title_notes(data)
        return Response(data)

    @transaction.atomic
    def post(self, request, table: str):
        items = request.data if isinstance(request.data, list) else [request.data]
        if table == "users":
            serialized = []
            for item in items:
                user_id = str(item.get("id") or uuid.uuid4())
                existing = UserProfile.objects.filter(id=user_id).first()
                if existing:
                    serializer = UserSerializer(existing, data=item, partial=True)
                else:
                    serializer = UserSerializer(data={**item, "id": user_id})
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                serialized.append(UserSerializer(user).data)
            return Response(serialized if isinstance(request.data, list) else serialized[0], status=status.HTTP_201_CREATED)

        saved = []
        for item in items:
            payload = normalize_payload(dict(item), payload_id(dict(item)) or str(uuid.uuid4()))
            record, _ = GenericRecord.objects.update_or_create(
                table=table,
                record_id=str(payload["id"]),
                defaults={"payload": payload},
            )
            saved.append(_record_response(record))
        return Response(saved if isinstance(request.data, list) else saved[0], status=status.HTTP_201_CREATED)

    @transaction.atomic
    def patch(self, request, table: str, record_id: str):
        if table == "users":
            user = get_object_or_404(UserProfile, id=record_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(UserSerializer(serializer.save()).data)
        record = get_object_or_404(GenericRecord, table=table, record_id=record_id)
        payload = dict(record.payload or {})
        payload.update(dict(request.data))
        payload["id"] = record_id
        record.payload = payload
        record.save(update_fields=["payload", "updated_at"])
        return Response(_record_response(record))

    @transaction.atomic
    def delete(self, request, table: str, record_id: str):
        if table == "users":
            UserProfile.objects.filter(id=record_id).delete()
        else:
            GenericRecord.objects.filter(table=table, record_id=record_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationRelayView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, channel: str):
        payload = request.data
        if channel == "email":
            recipients = payload.get("to") or []
            if isinstance(recipients, str):
                recipients = [recipients]
            if recipients and getattr(settings, "EMAIL_HOST", ""):
                send_mail(
                    payload.get("subject", "FXJ Suits notification"),
                    payload.get("html", ""),
                    getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@fxjsuits.co.ke"),
                    recipients,
                    html_message=payload.get("html", ""),
                    fail_silently=True,
                )
        # Push and Telegram are intentionally server-owned extension points. They
        # acknowledge requests locally when provider credentials are not configured.
        return Response({"accepted": True, "channel": channel})


class DocumentUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response({"detail": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
        table = str(request.data.get("table", "documents"))
        record_id = str(request.data.get("record_id", ""))
        document = Document.objects.create(
            table=table,
            record_id=record_id,
            file=uploaded,
            original_name=uploaded.name,
        )
        return Response(DocumentSerializer(document, context={"request": request}).data, status=status.HTTP_201_CREATED)
