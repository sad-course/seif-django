import os
import json

from django.core.management.base import BaseCommand
from django.db import DatabaseError, IntegrityError, OperationalError, ProgrammingError
from django.core.exceptions import ValidationError

from django.conf import settings
from management.models import ActivityType

ACTIVITY_TYPES_JSON = os.path.join(
    settings.BASE_DIR, "management", "data", "activity_types.json"
)


class Command(BaseCommand):
    help = "Populate activity types"

    def handle(self, *args, **options):

        with open(ACTIVITY_TYPES_JSON, encoding="utf-8") as json_file:
            activity_types = json.load(json_file)

            message = self.style.SUCCESS(
                "Activity Types were succesfully updated to database!"
            )
            try:
                for type_ in activity_types:
                    ActivityType.objects.get_or_create(
                        name=type_["name"], description=type_["description"]
                    )
            except (ValidationError, IntegrityError) as exception:
                message = self.style.ERROR(
                    "An exception was raised during the seed of Activity Types. \
                    Exception: %s, Message: %s",
                    type(exception).__name__,
                    str(exception),
                )
            except (DatabaseError, OperationalError, ProgrammingError):
                message = self.style.ERROR(
                    "An exception was raised during the seed of Activity Types. \
                    Exception: %s, Message: %s",
                    type(exception).__name__,
                    str(exception),
                )
            self.stdout.write(message)
