from typing import NamedTuple

from django.core.management import get_commands, call_command
from django.core.management.base import BaseCommand


class CommandItem(NamedTuple):
    name: str
    initial_message: str


COMMANDS = [
    CommandItem("populate_user_groups", "Populate the group entity..."),
    CommandItem("populate_activity_types", "Populate the activity types..."),
]


class Command(BaseCommand):
    help = "Seed the database with pre-data"

    def handle(self, *args, **options):
        valid_commands = [
            command for command in COMMANDS if command.name in get_commands()
        ]

        for command in valid_commands:
            self.stdout.write(command.initial_message)
            call_command(command.name)
