from django.core.management.base import BaseCommand
from .env import VALID_ENV_VARS


class Command(BaseCommand):
    help = "Create a new env file"

    def add_arguments(self, parser):
        parser.add_argument(
            "environment",
            type=str,
            help="Specify the environment for the Django application SEIF.\
            [prod, dev]",
        )

    def handle(self, *args, **kwargs):
        env_value = kwargs.get("environment")
        if env_value is not None and env_value in VALID_ENV_VARS:
            env_file = f".env.{env_value}"

            password = input("Enter the database password: ")

            with open(env_file, "w", encoding="UTF-8") as env_file:
                env_file.writelines("DEBUG=True\n")
                env_file.writelines(
                    "ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com\n"
                )
                env_file.writelines('DB_NAME="seif_dev_db"\n')
                env_file.writelines('DB_USER="postgres"\n')
                env_file.writelines(f'DB_PASSWORD="{password}"\n')
                env_file.writelines('DB_HOST="127.0.0.1"\n')
                env_file.writelines('DB_PORT="5432"\n')
