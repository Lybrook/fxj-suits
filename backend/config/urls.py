from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import connection
from django.http import JsonResponse
from django.urls import include, path


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok", "service": "fxj-suits-api", "database": "ok"})
    except Exception as exc:
        payload = {
            "status": "error",
            "service": "fxj-suits-api",
            "database": "unavailable",
        }
        if settings.DEBUG:
            payload["detail"] = str(exc)
        return JsonResponse(payload, status=503)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("api/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
