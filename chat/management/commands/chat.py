"""Management command that runs the terminal chat session.

Usage:
    python manage.py chat           # chat using what the bot was trained on
    python manage.py chat --learn   # also save each exchange as new knowledge

Type "quit" or "exit" (or press Ctrl+C) to end the session.
"""
from django.core.management.base import BaseCommand

from chat.bot import build_chatbot, is_trained, train_chatbot

# words that end the session instead of being sent to the bot
EXIT_COMMANDS = {"quit", "exit"}


class Command(BaseCommand):
    help = "Start a terminal conversation with the ChatterBot chatbot."

    def add_arguments(self, parser):
        parser.add_argument(
            "--learn",
            action="store_true",
            help="Let the bot save new input/response pairs from this session.",
        )

    def handle(self, *args, **options):
        bot = build_chatbot(read_only=not options["learn"])

        # train automatically on first run so the bot never starts empty
        if not is_trained(bot):
            self.stdout.write("No training data found. Training the chatbot first...")
            train_chatbot(build_chatbot(read_only=False), show_progress=False)
            self.stdout.write(self.style.SUCCESS("Training complete.\n"))

        self.stdout.write(f"Chatting with {bot.name}. Type 'quit' or 'exit' to leave.\n")
        self.run_chat_loop(bot)

    def run_chat_loop(self, bot):
        """Read user input, print the bot's reply, and repeat until the user leaves."""
        while True:
            try:
                user_text = input("user: ").strip()
            except (KeyboardInterrupt, EOFError):
                # ctrl+c or ctrl+d ends the session cleanly instead of a traceback
                self.stdout.write("\nbot: Goodbye!")
                break

            # ignore blank lines rather than sending empty text to the bot
            if not user_text:
                continue

            if user_text.lower() in EXIT_COMMANDS:
                self.stdout.write("bot: Goodbye!")
                break

            response = bot.get_response(user_text)
            self.stdout.write(f"bot: {response}")
