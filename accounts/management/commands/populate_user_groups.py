from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import DatabaseError, IntegrityError, OperationalError, ProgrammingError
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Populate the Group profiles"

    def handle(self, *args, **options):
        user_groups = set()
        user_groups.add("Organizers")
        user_groups.add("Administrators")

        try:
            message = self.style.SUCCESS(
                "Group profiles were succesfully updated to database!"
            )

            for group_name in user_groups:
                Group.objects.get_or_create(name=group_name)

        except (ValidationError, IntegrityError) as exception:
            message = self.style.ERROR(
                "An exception was raised during the seed of Group. \
                Exception: %s, Message: %s",
                type(exception).__name__,
                str(exception),
            )
        except (DatabaseError, OperationalError, ProgrammingError):
            message = self.style.ERROR(
                "An exception was raised during the seed of Group. \
                Exception: %s, Message: %s",
                type(exception).__name__,
                str(exception),
            )

        self.stdout.write(message)
