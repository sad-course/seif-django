from django.core.management.base import BaseCommand

VALID_ENV_VARS = {
    "dev": "development",
    "prod": "production",
}


class Command(BaseCommand):
    help = "Set environment for the Django application SEIF."

    def add_arguments(self, parser):
        parser.add_argument(
            "environment",
            type=str,
            help="Specify the environment for the Django application SEIF.\
            [dev, prod]",
        )

    def handle(self, *args, **kwargs):
        # Set environment variables for SEIF
        env_value = kwargs.get("environment", None)
        if env_value is not None and env_value in VALID_ENV_VARS:
            with open(".env", "w", encoding="UTF-8") as env_file:
                env_file.write(f"SEIF_ENV={VALID_ENV_VARS[env_value]}\n")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Environment switched to {env_value}"
                )  # pylint: disable=no-member
            )
        else:
            self.stderr.write(
                self.style.ERROR(
                    f"Invalid environment. Choose one from {VALID_ENV_VARS}."
                )  # pylint: disable=no-member
            )
