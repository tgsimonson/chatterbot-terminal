"""Django settings for the ChatterBot terminal client.

This project has no web interface. Django provides the ORM, the database
migrations for ChatterBot's Statement and Tag tables, and the management
command framework that runs the terminal chat loop.
"""
import os
from pathlib import Path

# project root: the folder that contains manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# read the secret key from the environment; the fallback is only for local
# development since this project never serves web requests
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-key-not-used-for-web-traffic",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # chatterbot's django integration supplies the Statement and Tag models
    "chatterbot.ext.django_chatterbot",
    # this project's app, which holds the bot factory and the chat command
    "chat",
]

# a local sqlite file stores everything the bot has learned
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

# settings read by chat/bot.py when it builds the chatbot
CHATBOT_NAME = "Terminal Bot"
CHATBOT_DEFAULT_RESPONSE = "I'm sorry, I don't understand. Could you rephrase that?"

# keep chatterbot and spacy quiet so the terminal only shows the conversation
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
