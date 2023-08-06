from comala.workflows.models.workflowstate import WorkflowState
from comala.workflows.models.workflowtask import WorkflowTask
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PageWorkflow:
    """
    Encapsulates the entire information that Comala Workflow stores about a
    page in confluence.
    """
    def __init__(self, state: WorkflowState, tasks: Optional[List[WorkflowTask]]) -> None:
        self.state = state
        self.tasks = tasks
