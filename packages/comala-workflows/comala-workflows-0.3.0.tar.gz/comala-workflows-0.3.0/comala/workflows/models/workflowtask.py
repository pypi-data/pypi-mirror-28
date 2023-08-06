import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class WorkflowTask:
    """
    Represents a single task on a document as used by the Comala workflow
    engine for confluence.
    """

    def __init__(self, task_id: int, name: str, assignee: Optional[str]) -> None:
        self.task_id = task_id
        self.name = name
        self.assignee = assignee

    def __str__(self):
        return f'{self.task_id} | {self.name}'
