from django.contrib import admin

from .models import Document, GenericRecord, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "role", "updated_at")
    search_fields = ("email", "name")
    list_filter = ("role",)


@admin.register(GenericRecord)
class GenericRecordAdmin(admin.ModelAdmin):
    list_display = ("table", "record_id", "updated_at")
    search_fields = ("table", "record_id")
    list_filter = ("table",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("original_name", "table", "record_id", "created_at")
    search_fields = ("original_name", "table", "record_id")
