from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import GenericRecord, UserProfile


class Command(BaseCommand):
    help = "Create the local FXJ Suits demo account and sample records."

    def handle(self, *args, **options):
        # Do not use a hard-coded primary key in defaults. A previous local seed
        # or migrated Supabase row may already own that ID while using another email.
        # Looking up by the stable demo email and letting Django generate the ID
        # makes this command safe to run repeatedly in any environment.
        with transaction.atomic():
            admin = UserProfile.objects.filter(email="admin@buwembo.com").first()
            if admin is None:
                admin = UserProfile(
                    email="admin@buwembo.com",
                    name="System Admin",
                    role="admin",
                )
            else:
                admin.name = "System Admin"
                admin.role = "admin"
            admin.set_password("password123")
            admin.save()

        samples = [
            (
                "clients",
                "demo-client-1",
                {
                    "id": "demo-client-1",
                    "name": "Kampala Holdings Ltd",
                    "type": "Corporate",
                    "email": "legal@kampalaholdings.example",
                    "phone": "+256 700 000 000",
                    "dateAdded": "2026-01-15T09:00:00Z",
                },
            ),
            (
                "court_cases",
                "demo-case-1",
                {
                    "id": "demo-case-1",
                    "fileName": "Kampala Holdings v. Sunrise Properties",
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
        self.stdout.write(self.style.SUCCESS("FXJ Suits demo data is ready."))
