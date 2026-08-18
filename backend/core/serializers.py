from rest_framework import serializers

from .models import Document, GenericRecord, UserProfile, new_id


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    id = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ["id", "name", "email", "role", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password", "")
        user = UserProfile(id=validated_data.pop("id", new_id()), **validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("password", None)
        return data


class GenericRecordSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="record_id")

    class Meta:
        model = GenericRecord
        fields = ["id", "payload", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def to_representation(self, instance):
        payload = dict(instance.payload or {})
        payload.setdefault("id", instance.record_id)
        return payload


class DocumentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    name = serializers.CharField(source="original_name")

    class Meta:
        model = Document
        fields = ["id", "table", "record_id", "name", "url", "created_at"]

    def get_url(self, obj):
        request = self.context.get("request")
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url
