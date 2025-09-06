"""
Unit tests cho agents.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from agents.ai_engineer_agent import AiEngineerAgent
from agents.ui_designer_agent import UiDesignerAgent
from core.schemas import AgentRequest


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    client.generate = AsyncMock(return_value=MagicMock(response="Test response"))
    return client


@pytest.mark.asyncio
async def test_ai_engineer_agent_process(mock_ollama_client):
    """Test AiEngineerAgent process method."""
    agent = AiEngineerAgent(mock_ollama_client)
    request = AgentRequest(agent_type="aiengineer", message="Hello")
    
    response = await agent.process(request)
    
    assert response.success is True
    assert response.agent_type == "aiengineer"
    assert "Test response" in response.response


@pytest.mark.asyncio
async def test_ui_designer_agent_process(mock_ollama_client):
    """Test UiDesignerAgent process method."""
    agent = UiDesignerAgent(mock_ollama_client)
    request = AgentRequest(
        agent_type="uidesigner", 
        message="Design a login form"
    )
    
    response = await agent.process(request)
    
    assert response.success is True
    assert response.agent_type == "uidesigner"