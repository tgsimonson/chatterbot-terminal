"""Builds and trains the ChatterBot instance used by the terminal client.

Keeping construction and training in one module means the chat and
train_bot management commands always configure the bot the same way.
"""
from pathlib import Path

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.conf import settings

# custom conversations that ship with this project, including the sample
# dialog from the assignment prompt
CUSTOM_CORPUS = Path(__file__).resolve().parent / "training_data" / "custom_conversations.yml"

# the english corpus bundled with the chatterbot-corpus package
ENGLISH_CORPUS = "chatterbot.corpus.english"


def build_chatbot(read_only=True):
    """Create a ChatBot that stores its knowledge through Django's ORM.

    Args:
        read_only: When True the bot answers from what it was trained on and
            does not save new input. When False it learns each exchange.

    Returns:
        A configured chatterbot.ChatBot instance.
    """
    return ChatBot(
        settings.CHATBOT_NAME,
        # store statements in the django database instead of a separate file
        storage_adapter="chatterbot.storage.DjangoStorageAdapter",
        logic_adapters=[
            {
                # bestmatch finds the known statement closest to the input
                # and returns a response that followed it in training data
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": settings.CHATBOT_DEFAULT_RESPONSE,
                # below this confidence the bot uses the default response
                # rather than guessing
                "maximum_similarity_threshold": 0.90,
            },
            # answers simple arithmetic like "what is 4 plus 4"
            "chatterbot.logic.MathematicalEvaluation",
        ],
        read_only=read_only,
    )


def train_chatbot(bot, show_progress=True):
    """Train the bot on the english corpus plus this project's conversations.

    Args:
        bot: The ChatBot instance to train.
        show_progress: Whether to print a progress bar for each corpus file.
    """
    trainer = ChatterBotCorpusTrainer(bot, show_training_progress=show_progress)
    # custom conversations go first: bestmatch returns the first stored
    # response to a matched statement, so where a prompt appears in both
    # files (for example "What are you?"), the project's own answer wins
    trainer.train(str(CUSTOM_CORPUS), ENGLISH_CORPUS)


def is_trained(bot):
    """Return True if the bot's database already holds training data."""
    return bot.storage.count() > 0
