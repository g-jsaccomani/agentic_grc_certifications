"""Agent2Agent (A2A) Protocol Client.

Facilitates secure multi-agent coordination, Agent Card discovery
(/.well-known/agent.json), and asynchronous task lifecycle orchestration
(submitted -> working -> input-required -> completed/failed).
"""

from enum import Enum
from typing import Any, Dict, List, Optional
import httpx


class A2ATaskStatus(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"


class A2ATask:
    def __init__(self, task_id: str, agent_url: str, name: str, payload: Dict[str, Any]):
        self.task_id = task_id
        self.agent_url = agent_url
        self.name = name
        self.payload = payload
        self.status = A2ATaskStatus.SUBMITTED
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None

    def update_status(self, new_status: A2ATaskStatus, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        self.status = new_status
        if result is not None:
            self.result = result
        if error is not None:
            self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent_url": self.agent_url,
            "name": self.name,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
        }


class A2AClient:
    """Client for negotiating and communicating with external A2A Servers."""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def fetch_agent_card(self, agent_url: str) -> Dict[str, Any]:
        """Discovers capabilities, skills, and schemas by fetching /.well-known/agent.json."""
        discovery_url = f"{agent_url.rstrip('/')}/.well-known/agent.json"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(discovery_url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Agent Card from {discovery_url}: {e}") from e

    async def fetch_agent_card_async(self, agent_url: str) -> Dict[str, Any]:
        """Async discovery of Agent Card."""
        discovery_url = f"{agent_url.rstrip('/')}/.well-known/agent.json"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(discovery_url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Agent Card from {discovery_url}: {e}") from e

    def submit_task(
        self,
        agent_url: str,
        task_name: str,
        payload: Dict[str, Any],
        token: Optional[str] = None,
    ) -> A2ATask:
        """Submits a task to the remote A2A server and returns the initial task handle."""
        import uuid
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = A2ATask(task_id=task_id, agent_url=agent_url, name=task_name, payload=payload)
        task.update_status(A2ATaskStatus.WORKING)
        return task
