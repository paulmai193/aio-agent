"""
Unit tests cho agents.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from agents.chat_agent import ChatAgent
from agents.code_agent import CodeAgent
from core.schemas import AgentRequest


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    client.generate = AsyncMock(return_value=MagicMock(response="Test response"))
    return client


@pytest.mark.asyncio
async def test_chat_agent_process(mock_ollama_client):
    """Test ChatAgent process method."""
    agent = ChatAgent(mock_ollama_client)
    request = AgentRequest(agent_type="chat", message="Hello")
    
    response = await agent.process(request)
    
    assert response.success is True
    assert response.agent_type == "chat"
    assert "Test response" in response.response


@pytest.mark.asyncio
async def test_code_agent_process(mock_ollama_client):
    """Test CodeAgent process method."""
    agent = CodeAgent(mock_ollama_client)
    request = AgentRequest(
        agent_type="code", 
        message="Write a Python function",
        context={"language": "python"}
    )
    
    response = await agent.process(request)
    
    assert response.success is True
    assert response.agent_type == "code"
    assert response.metadata["language"] == "python"