import uuid

from django.contrib.auth.hashers import make_password
from django.db import models


ROLE_CHOICES = [
    ("admin", "Admin"),
    ("manager", "Manager"),
    ("managing_partner", "Managing Partner"),
    ("lawyer", "Lawyer"),
    ("clerk", "Clerk"),
    ("accountant", "Accountant"),
]


def new_id() -> str:
    return str(uuid.uuid4())


class UserProfile(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=new_id)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="lawyer")
    password_hash = models.CharField(max_length=255, blank=True)
    auth_token = models.CharField(max_length=128, unique=True, default=new_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def set_password(self, raw_password: str) -> None:
        self.password_hash = make_password(raw_password)


class GenericRecord(models.Model):
    table = models.CharField(max_length=64)
    record_id = models.CharField(max_length=128)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["table", "record_id"], name="unique_table_record"),
        ]
        indexes = [models.Index(fields=["table", "updated_at"])]


class Document(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=new_id)
    table = models.CharField(max_length=64)
    record_id = models.CharField(max_length=128)
    file = models.FileField(upload_to="documents/%Y/%m/%d")
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
