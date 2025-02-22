import shutil
import os
from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Copy Event Banner default from static to MEDIA_ROOT"

    def handle(self, *args, **options):
        media_path_to_default_banner = os.path.join(
            settings.MEDIA_ROOT, "events/banners/event-banner-default.jpg"
        )
        static_path_to_default_banner = os.path.join(
            settings.STATIC_ROOT, "img/event-banner-default.jpg"
        )

        call_command("collectstatic")

        if not os.path.exists(media_path_to_default_banner):
            try:
                shutil.copyfile(
                    static_path_to_default_banner, media_path_to_default_banner
                )
                self.stdout.write(
                    self.style.SUCCESS("Static file was copied succesfully!")
                )

            except Exception as exception:
                self.stdout.write(
                    self.style.ERROR(
                        f"Exception when copying the file. Exception: {type(exception).__name__} \
                        Message: {str(exception)}"
                    )
                )
