from django.urls import path

from .views import DocumentUploadView, LoginView, LogoutView, MeView, NotificationRelayView, TableView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/me", MeView.as_view(), name="me"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("uploads", DocumentUploadView.as_view(), name="uploads"),
    path("notifications/<str:channel>", NotificationRelayView.as_view(), name="notification-relay"),
    path("records/<str:table>", TableView.as_view(), name="table-records"),
    path("records/<str:table>/<str:record_id>", TableView.as_view(), name="table-record"),
]
