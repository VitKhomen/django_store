from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Создаёт суперюзера, если он ещё не существует"

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")
        first_name = "Admin"
        last_name = "User"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(
                f"Суперпользователь '{email}' создан"))
        else:
            self.stdout.write(self.style.WARNING(
                f"Суперпользователь '{email}' уже существует"))
