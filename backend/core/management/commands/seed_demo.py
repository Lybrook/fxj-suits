from django.core.management.base import BaseCommand

from core.models import GenericRecord, UserProfile


class Command(BaseCommand):
    help = "Create the local FXJ Suits demo account and sample records."

    def handle(self, *args, **options):
        admin, created = UserProfile.objects.get_or_create(
            email="admin@fxjsuits.co.ke",
            defaults={
                "id": "d70d4e47-1422-4501-961a-c1e69a1c15d7",
                "name": "System Admin",
                "role": "admin",
            },
        )
        if created or not admin.password_hash:
            admin.set_password("password123")
            admin.save()

        samples = [
            (
                "clients",
                "demo-client-1",
                {
                    "id": "demo-client-1",
                    "name": "Nakuru Holdings Ltd",
                    "type": "Corporate",
                    "email": "legal@nakuruholdings.example",
                    "phone": "+254 700 000 000",
                    "dateAdded": "2026-01-15T09:00:00Z",
                },
            ),
            (
                "court_cases",
                "demo-case-1",
                {
                    "id": "demo-case-1",
                    "fileName": "Nakuru Holdings v. Sunrise Properties",
                    "details": "Commercial dispute — sample record for local development.",
                    "status": "Ongoing",
                    "billed": 4200000,
                    "paid": 2100000,
                    "balance": 2100000,
                    "nextCourtDate": "2026-09-04",
                    "categories": ["Commercial"],
                    "archived": False,
                    "documents": [],
                    "progressNotes": [],
                    "deadlines": [],
                },
            ),
        ]
        for table, record_id, payload in samples:
            GenericRecord.objects.update_or_create(
                table=table,
                record_id=record_id,
                defaults={"payload": payload},
            )
        self.stdout.write(self.style.SUCCESS("FXJ Suits Kenya demo data is ready."))
