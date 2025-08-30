"""
API endpoints cho Agent Orchestrator.
"""
import logging
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from core.agent_manager import AgentManager
from core.task_orchestrator import TaskOrchestrator
from core.schemas import AgentRequest, AgentResponse, HealthResponse


logger = logging.getLogger(__name__)
router = APIRouter()


class UserRequest(BaseModel):
    """Request model cho user input."""
    message: str
    context: Optional[Dict[str, Any]] = None

class TaskResponse(BaseModel):
    """Response model cho orchestrated tasks."""
    tasks: List[Dict[str, Any]]
    results: List[AgentResponse]
    success: bool
    error: Optional[str] = None

def get_agent_manager(request: Request) -> AgentManager:
    """Dependency để lấy agent manager."""
    return request.app.state.agent_manager


@router.post("/chat", response_model=AgentResponse)
async def chat_endpoint(
    request: AgentRequest,
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Endpoint chính để xử lý request từ user."""
    try:
        logger.info(f"Nhận request cho agent: {request.agent_type}, message: {request.message[:50]}...")
        response = await agent_manager.process_request(request)
        
        if not response.success:
            logger.warning(f"Agent {request.agent_type} failed: {response.error}")
            raise HTTPException(status_code=400, detail=response.error)
        
        logger.info(f"Agent {request.agent_type} processed successfully")
        return response
    
    except Exception as e:
        logger.error(f"Lỗi xử lý request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents", response_model=List[str])
async def list_agents(
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Lấy danh sách các agent có sẵn."""
    logger.debug("Listing available agents")
    agents = agent_manager.list_agents()
    logger.debug(f"Found {len(agents)} agents")
    return agents


@router.get("/health", response_model=HealthResponse)
async def health_check(
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Health check endpoint."""
    try:
        logger.debug("Health check requested")
        health_data = await agent_manager.health_check()
        
        status = "healthy" if health_data["ollama_connected"] else "degraded"
        logger.debug(f"Health check status: {status}")
        
        return HealthResponse(
            status=status,
            agents_loaded=health_data["agents_loaded"],
            ollama_connected=health_data["ollama_connected"]
        )
    
    except Exception as e:
        logger.error(f"Lỗi health check: {e}")
        return HealthResponse(
            status="unhealthy",
            agents_loaded=0,
            ollama_connected=False
        )


@router.post("/process", response_model=TaskResponse)
async def process_user_request(
    request: UserRequest,
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Process user request with automatic task orchestration."""
    try:
        logger.info(f"Processing user request: {request.message[:50]}...")
        
        # Initialize task orchestrator
        orchestrator = TaskOrchestrator(agent_manager.ollama_client)
        
        # Analyze and split request into tasks
        tasks = await orchestrator.analyze_and_split_request(request.message)
        logger.info(f"Request split into {len(tasks)} tasks")
        
        # Execute tasks in order of priority and dependencies
        results = []
        task_outputs = {}
        
        # Sort tasks by priority
        sorted_tasks = sorted(tasks, key=lambda x: x.get('priority', 1))
        
        for i, task in enumerate(sorted_tasks):
            # Check dependencies
            dependencies = task.get('dependencies', [])
            if dependencies:
                # Wait for dependencies (simplified - assumes sequential execution)
                logger.debug(f"Task {i} has dependencies: {dependencies}")
            
            # Create agent request
            agent_request = AgentRequest(
                agent_type=task['agent_type'],
                message=task['task_description'],
                context=request.context
            )
            
            # Process task
            logger.info(f"Executing task {i+1}/{len(tasks)}: {task['agent_type']}")
            result = await agent_manager.process_request(agent_request)
            results.append(result)
            task_outputs[i] = result.response
            
            if not result.success:
                logger.warning(f"Task {i} failed: {result.error}")
        
        # Check overall success
        overall_success = all(r.success for r in results)
        
        return TaskResponse(
            tasks=tasks,
            results=results,
            success=overall_success,
            error=None if overall_success else "Some tasks failed"
        )
        
    except Exception as e:
        logger.error(f"Error processing user request: {e}")
        return TaskResponse(
            tasks=[],
            results=[],
            success=False,
            error=str(e)
        )