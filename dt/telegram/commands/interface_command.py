class Command:
    """Base class for commands."""

    def execute(self, callback_query):
        raise NotImplementedError(
            "Subclasses should implement this method."
        )
