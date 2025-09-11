"""Unit tests for AgentManager."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from core.agent_manager import AgentManager
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    client.health_check = AsyncMock(return_value=True)
    client.close = AsyncMock()
    return client


@pytest.fixture
def agent_manager(mock_ollama_client):
    """Agent manager with mocked dependencies."""
    with patch('core.agent_manager.OllamaClient', return_value=mock_ollama_client):
        manager = AgentManager()
    return manager


@pytest.mark.asyncio
async def test_initialize_success(agent_manager):
    """Test successful agent initialization."""
    await agent_manager.initialize()
    assert len(agent_manager.agents) == 14
    assert 'aiengineer' in agent_manager.agents
    assert 'uidesigner' in agent_manager.agents
    assert 'languagedetector' in agent_manager.agents
    assert 'brandguardian' in agent_manager.agents
    assert 'uxresearcher' in agent_manager.agents


@pytest.mark.asyncio
async def test_process_request_success(agent_manager):
    """Test successful request processing."""
    await agent_manager.initialize()
    
    # Mock agent response
    mock_agent = MagicMock()
    mock_agent.process = AsyncMock(return_value=AgentResponse(
        agent_type="aiengineer",
        response="Test response",
        success=True
    ))
    agent_manager.agents["aiengineer"] = mock_agent
    
    request = AgentRequest(agent_type="aiengineer", message="Test message")
    response = await agent_manager.process_request(request)
    
    assert response.success is True
    assert response.agent_type == "aiengineer"
    assert response.response == "Test response"


@pytest.mark.asyncio
async def test_process_request_agent_not_found(agent_manager):
    """Test request processing with non-existent agent."""
    await agent_manager.initialize()
    
    request = AgentRequest(agent_type="nonexistent", message="Test message")
    response = await agent_manager.process_request(request)
    
    assert response.success is False
    assert "Không tìm thấy agent: nonexistent" in response.error


@pytest.mark.asyncio
async def test_process_request_agent_exception(agent_manager):
    """Test request processing when agent throws exception."""
    await agent_manager.initialize()
    
    # Mock agent that throws exception
    mock_agent = MagicMock()
    mock_agent.process = AsyncMock(side_effect=Exception("Agent error"))
    agent_manager.agents["aiengineer"] = mock_agent
    
    request = AgentRequest(agent_type="aiengineer", message="Test message")
    response = await agent_manager.process_request(request)
    
    assert response.success is False
    assert "Agent processing error" in response.error


def test_get_agent_exists(agent_manager):
    """Test getting existing agent."""
    agent_manager.agents["test"] = "mock_agent"
    result = agent_manager.get_agent("test")
    assert result == "mock_agent"


def test_get_agent_not_exists(agent_manager):
    """Test getting non-existent agent."""
    result = agent_manager.get_agent("nonexistent")
    assert result is None


def test_list_agents(agent_manager):
    """Test listing agents."""
    agent_manager.agents = {"agent1": "mock1", "agent2": "mock2"}
    result = agent_manager.list_agents()
    assert result == ["agent1", "agent2"]


def test_register_agent(agent_manager):
    """Test registering new agent."""
    mock_agent = MagicMock()
    mock_agent.agent_type = "newagent"
    
    agent_manager.register_agent(mock_agent)
    assert "newagent" in agent_manager.agents
    assert agent_manager.agents["newagent"] == mock_agent


@pytest.mark.asyncio
async def test_health_check_success(agent_manager, mock_ollama_client):
    """Test successful health check."""
    await agent_manager.initialize()
    mock_ollama_client.health_check.return_value = True
    
    result = await agent_manager.health_check()
    
    assert result["agents_loaded"] == 14
    assert result["ollama_connected"] is True
    assert len(result["agent_types"]) == 14


@pytest.mark.asyncio
async def test_health_check_ollama_down(agent_manager, mock_ollama_client):
    """Test health check with Ollama down."""
    await agent_manager.initialize()
    mock_ollama_client.health_check.return_value = False
    
    result = await agent_manager.health_check()
    
    assert result["agents_loaded"] == 14
    assert result["ollama_connected"] is False


@pytest.mark.asyncio
async def test_cleanup_success(agent_manager, mock_ollama_client):
    """Test successful cleanup."""
    await agent_manager.cleanup()
    mock_ollama_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_cleanup_with_exception(agent_manager, mock_ollama_client):
    """Test cleanup when ollama client throws exception."""
    mock_ollama_client.close.side_effect = Exception("Close error")
    
    # Should not raise exception
    await agent_manager.cleanup()
    mock_ollama_client.close.assert_called_once()