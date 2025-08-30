"""
API endpoints cho Agent Orchestrator.
"""
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from core.agent_manager import AgentManager
from core.schemas import AgentRequest, AgentResponse, HealthResponse


logger = logging.getLogger(__name__)
router = APIRouter()


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