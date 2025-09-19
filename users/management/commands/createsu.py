import os
from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = "Create a superuser from environment variables if it doesn't exist"

    def handle(self, *args, **options):
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        first_name = os.getenv("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
        last_name = os.getenv("DJANGO_SUPERUSER_LAST_NAME", "User")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(self.style.ERROR(
                "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set!"
            ))
            return

        if not CustomUser.objects.filter(email=email).exists():
            CustomUser.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(
                f"Superuser {email} created!"))
        else:
            self.stdout.write(self.style.WARNING(
                f"Superuser {email} already exists."))
