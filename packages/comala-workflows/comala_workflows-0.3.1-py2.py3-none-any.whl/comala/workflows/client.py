from comala.workflows.models.workflow import PageWorkflow
from comala.workflows.models.workflowstate import WorkflowState
from comala.workflows.models.workflowtask import WorkflowTask
import logging
import requests
from typing import Optional, Tuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ComalaWorkflowsClient:
    """
    This is the main interface into this API from external applications. It
    provides an abstraction over the REST API which comala workflows provides
    in Confluence.
    """
    def __init__(self, url: str, basic_auth: Tuple[str, str]) -> None:
        """
        :param url: The base URL on which you access the confluence instance
        in a web browser.
        :param basic_auth: A tuple of username/password which can access the
        Confluence instance.
        """
        self._url = url
        self._basic_auth = basic_auth
        self._base_api_url = f'{self._url}/rest/cw/1'
        self._client: requests.Session = None

    def __enter__(self):
        self._client = requests.session()
        self._client.auth = self._basic_auth

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            self._client.close()

    def status(self, page_id: int, expand: Optional[str] = None) -> PageWorkflow:
        """
        Get the status of a page as understood by Comala Workflows.

        c.f. http://bit.ly/2mGKv26 for the official docs.

        :param page_id: The confluence page ID.
        :param expand: An optional comma separated string of properties to
        expand. Valid values are: state, states, approvals, actions, tasks.

        :return: A PageWorkflow object containing information about the page.
        """
        url = f'{self._base_api_url}/content/{page_id}/status'
        params = {}

        if expand:
            params['expand'] = expand

        if self._client:
            result = self._client.get(url, params=params).json()
        else:
            result = requests.get(url, params=params, auth=self._basic_auth).json()

        state = WorkflowState(result['state']['name'], result['state']['description'], result['state']['initial'],
                              result['state']['final'])
        tasks = None
        if 'tasks' in result:
            tasks = [WorkflowTask(t['id'], t['name'], None if 'assignee' not in t else t['assignee']['name'])
                     for t in result['tasks']]

        return PageWorkflow(state, tasks)
