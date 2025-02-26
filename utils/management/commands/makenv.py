import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a new env file"

    def handle(self, *args, **kwargs):

        if os.path.exists(".env"):
            override_env = input("Do you want override .env? (Y/n)  ")
            if override_env:
                if override_env in ["n"]:
                    return

        self.stdout.write(
            self.style.WARNING(
                "Pay attention, it's your password to access \
            YOUR postgresql database. You can change it if necessary in .env"
            )
        )
        password = input(" Enter the database password: ")

        with open(".env", "w", encoding="utf-8") as env_file:
            env_file.writelines("DEBUG=True\n")
            env_file.writelines("ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com\n")
            env_file.writelines('DB_NAME="seif_dev_db"\n')
            env_file.writelines('DB_USER="postgres"\n')
            env_file.writelines(f'DB_PASSWORD="{password}"\n')
            env_file.writelines('DB_HOST="127.0.0.1"\n')
            env_file.writelines('DB_PORT="5432"\n')
