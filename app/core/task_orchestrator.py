"""
Task orchestrator để phân tích và chia nhỏ request thành các tasks.
"""
import json
import logging
from typing import List, Dict, Any, Optional

from agents.base import BaseAgent
from core.ollama_client import OllamaClient
from core.schemas import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)


class TaskOrchestrator(BaseAgent):
    """Orchestrator để phân tích và chia nhỏ tasks."""
    
    def __init__(self, ollama_client: OllamaClient):
        super().__init__(ollama_client)
        self.agent_type = "taskorchestrator"
    
    async def process(self, request: AgentRequest) -> AgentResponse:
        """Xử lý request từ user."""
        try:
            tasks = await self.analyze_and_split_request(request.message)
            return AgentResponse(
                agent_type=self.agent_type,
                response=json.dumps(tasks, indent=2),
                success=True
            )
        except Exception as e:
            return AgentResponse(
                agent_type=self.agent_type,
                response="",
                success=False,
                error=str(e)
            )
    
    def get_system_prompt(self) -> str:
        """Lấy system prompt cho agent."""
        return """You are a task orchestrator that analyzes user requests and breaks them down into specific tasks for specialized agents.

Available agents and their capabilities:
- aiengineer: AI/ML features, LLM integration, computer vision, recommendation systems, general programming
- backendarchitect: API design, database architecture, server systems, scalability
- frontenddeveloper: UI/UX implementation, React/Vue, responsive design, frontend performance
- rapidprototyper: MVP development, quick prototypes, proof of concepts
- devopsautomator: CI/CD, Docker, Kubernetes, infrastructure automation
- testwriterfixer: Unit tests, integration tests, test automation, quality assurance
- contentcreator: Blog posts, marketing content, social media, SEO content
- growthhacker: User acquisition, viral mechanics, growth experiments, analytics
- uidesigner: Interface design, design systems, user experience, visual design
- trendresearcher: Market trends, viral opportunities, consumer behavior analysis
- projectshipper: Project management, launch planning, delivery coordination

Analyze the user request and break it down into specific tasks. For each task, select the most appropriate agent.

Return a JSON array of tasks in this format with out any explanation or extra text.
IMPORTANT: You must respond with a valid JSON array only, no other text. The response must be parseable by json.loads().

Example response format:
[
  {
    "task_description": "Clear description of what needs to be done",
    "agent_type": "most_suitable_agent",
    "priority": 1,
    "dependencies": []
  }
]

Priority: 1 (highest) to 5 (lowest)
Dependencies: Array of task indices (0-based) that must complete first. Use dependencies when:
- Task needs output/results from previous tasks as input
- Task builds upon work done by another task
- Sequential workflow is required

The system will automatically pass outputs from dependency tasks as context to dependent tasks."""
    
    def get_model_name(self) -> str:
        """Lấy tên model Ollama sử dụng."""
        from config import settings
        return settings.MODEL_TASKORCHESTRATOR
    
    async def analyze_and_split_request(self, user_request: str) -> List[Dict[str, Any]]:
        """Phân tích request và chia thành các tasks với agent phù hợp."""
        try:
            response = await self.call_ollama(user_request)
            logger.debug(f"Task analysis response: {response}")
            
            # Extract JSON from response (handle markdown code blocks)
            response_clean = response.strip()
            if "```json" in response_clean:
                start = response_clean.find("```json") + 7
                end = response_clean.find("```", start)
                response_clean = response_clean[start:end].strip()
            elif "```" in response_clean:
                start = response_clean.find("```") + 3
                end = response_clean.find("```", start)
                response_clean = response_clean[start:end].strip()
            
            # Find JSON array in response
            if "[" in response_clean and "]" in response_clean:
                start = response_clean.find("[")
                end = response_clean.rfind("]") + 1
                json_str = response_clean[start:end]
            else:
                json_str = response_clean
            
            tasks = json.loads(json_str)
            logger.info(f"Analyzed request into {len(tasks)} tasks")
            
            # Validate and fix task dependencies
            validated_tasks = self._validate_dependencies(tasks)
            return validated_tasks
            
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error analyzing request: {e}, response: {response[:200] if 'response' in locals() else 'No response'}")
            # Fallback to single aiengineer task
            return [{
                "task_description": user_request,
                "agent_type": "aiengineer",
                "priority": 1,
                "dependencies": []
            }]
    
    def _validate_dependencies(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and fix task dependencies."""
        for i, task in enumerate(tasks):
            dependencies = task.get('dependencies', [])
            # Remove invalid dependencies (self-reference, out of range)
            valid_deps = [dep for dep in dependencies if isinstance(dep, int) and 0 <= dep < len(tasks) and dep != i]
            task['dependencies'] = valid_deps
            
            # Ensure required fields exist
            task.setdefault('priority', 3)
            task.setdefault('agent_type', 'aiengineer')
        
        return tasks