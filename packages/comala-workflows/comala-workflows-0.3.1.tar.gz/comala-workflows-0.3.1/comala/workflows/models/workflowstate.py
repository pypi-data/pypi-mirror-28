import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class WorkflowState:
    """
    Represents a single Comala workflow state which a page can be in.
    """
    def __init__(self, name: str, description: str, initial: bool, final: bool) -> None:
        self.name = name
        self.description = description
        self.initial = initial
        self.final = final

    def __str__(self):
        return self.name
