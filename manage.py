#!/usr/bin/env python
"""Django's command-line utility for the ChatterBot terminal client.

Usage:
    python manage.py migrate     # create the database tables
    python manage.py train_bot   # train the bot (optional, chat trains on first run)
    python manage.py chat        # start the terminal chat session
"""
import os
import sys


def main():
    """Point Django at this project's settings and run the requested command."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Is it installed and is the virtual "
            "environment activated? Run: pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
