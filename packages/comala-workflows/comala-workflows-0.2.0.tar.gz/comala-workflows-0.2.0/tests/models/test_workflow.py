from comala.workflows.models.workflow import PageWorkflow
from comala.workflows.models.workflowstate import WorkflowState
from comala.workflows.models.workflowtask import WorkflowTask
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_workflow_creation_without_tasks():
    pw = PageWorkflow(state=WorkflowState("name", "desc", False, False), tasks=None)
    assert pw.tasks is None
    assert pw.state.name == "name"
    assert pw.state.description == "desc"
    assert not pw.state.final
    assert not pw.state.initial


def test_workflow_creation_with_empty_tasks():
    pw = PageWorkflow(state=WorkflowState("name", "desc", False, False), tasks=[])
    assert len(pw.tasks) == 0


def test_workflow_creation_with_non_empty_tasks():
    pw = PageWorkflow(state=WorkflowState("name", "desc", False, False), tasks=[WorkflowTask(1, "name", assignee=None)])
    assert len(pw.tasks) == 1
    assert pw.tasks[0].task_id == 1
    assert pw.tasks[0].name == "name"
    assert pw.tasks[0].assignee is None
