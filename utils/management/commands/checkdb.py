import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Check and create the database if it does not exist."

    def handle(self, *args, **kwargs):
        db_url = settings.DATABASES["default"]
        db_name = db_url["NAME"]
        db_user = db_url["USER"]
        db_password = db_url["PASSWORD"]
        db_host = db_url["HOST"]
        db_port = db_url["PORT"]

        try:
            # Connect to the PostgreSQL server
            connection = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            # Create a cursor and check if the database exists
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT datname FROM pg_database WHERE datname = '{db_name}';"
            )
            exists = cursor.fetchone()

            if not exists:
                self.stdout.write(f"Database '{db_name}' does not exist. Creating...")
                cursor.execute(f"CREATE DATABASE {db_name};")
                self.stdout.write(f"✅ Database '{db_name}' created successfully.")
            else:
                self.stdout.write(f"✅ Database '{db_name}' already exists.")

            self.stdout.write(self.style.SUCCESS("📂 Applying schema to database..."))
            call_command("migrate")
        except psycopg2.Error as exception:
            self.stderr.write(f"🛑 Error connecting to PostgreSQL: {exception}")
        finally:
            if connection:
                cursor.close()
                connection.close()
