class Command:
    """Base class for commands."""

    def __init__(self, prefix: str = "/"):
        self.prefix = prefix

    def execute(self, callback_query):
        raise NotImplementedError(
            "Subclasses should implement this method."
        )
