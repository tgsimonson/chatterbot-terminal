"""App configuration for the terminal chat app."""
from django.apps import AppConfig


class ChatConfig(AppConfig):
    """Registers the chat app, which provides the train_bot and chat commands."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"
    verbose_name = "Terminal Chat"
