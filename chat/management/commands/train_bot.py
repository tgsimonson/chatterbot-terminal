"""Management command that (re)trains the chatbot.

Usage:
    python manage.py train_bot           # train, adding to any existing data
    python manage.py train_bot --reset   # clear learned data, then train
"""
from django.core.management.base import BaseCommand

from chat.bot import build_chatbot, train_chatbot


class Command(BaseCommand):
    help = "Train the chatbot on the ChatterBot English corpus and this project's conversations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete everything the bot has learned before training.",
        )

    def handle(self, *args, **options):
        # training has to write to the database, so read_only is off here
        bot = build_chatbot(read_only=False)

        if options["reset"]:
            bot.storage.drop()
            self.stdout.write("Cleared existing training data.")

        self.stdout.write("Training the chatbot. This takes a minute the first time...")
        train_chatbot(bot)
        self.stdout.write(
            self.style.SUCCESS(f"Training complete. {bot.storage.count()} statements stored.")
        )
