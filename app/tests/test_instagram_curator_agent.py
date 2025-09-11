"""Unit tests for InstagramCuratorAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.instagram_curator_agent import InstagramCuratorAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def instagram_agent(mock_ollama_client):
    """InstagramCuratorAgent instance."""
    return InstagramCuratorAgent(mock_ollama_client)


def test_uses_correct_model(instagram_agent):
    """Test that agent uses the correct model based on its intended function."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_INSTAGRAMCURATOR = "llama3.2:3b"
        model = instagram_agent.get_model_name()
        assert model == "llama3.2:3b"


def test_system_prompt_matches_instruction_exactly(instagram_agent):
    """Test that agent's system_prompt matches the instruction exactly."""
    prompt = instagram_agent.get_system_prompt()
    
    # Verify key components from the instruction are present exactly
    assert "You are an Instagram Curator specializing in visual content strategy and platform growth." in prompt
    assert "Your expertise spans content creation, algorithm optimization, and community building on Instagram." in prompt
    assert "Core Responsibilities" in prompt
    assert "Visual Strategy Development" in prompt
    assert "Growth Optimization" in prompt
    assert "Content Production Planning" in prompt
    assert "Community Engagement" in prompt
    assert "Expertise Areas" in prompt
    assert "Algorithm Mastery" in prompt
    assert "Visual Storytelling" in prompt
    assert "Best Practices & Frameworks" in prompt
    assert "The AIDA Feed Structure" in prompt
    assert "The 3-3-3 Content Rule" in prompt
    assert "Integration with 6-Week Sprint Model" in prompt
    assert "Key Metrics to Track" in prompt
    assert "Platform-Specific Strategies" in prompt
    assert "Content Creation Approach" in prompt
    assert "Always optimize for mobile viewing experience" in prompt


def test_conforms_to_base_agent_schema(instagram_agent):
    """Test that agent conforms to the BaseAgent schema."""
    # Test standard schema structure
    schema = instagram_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "solution" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "technologies" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 4


@pytest.mark.asyncio
async def test_process_success(instagram_agent):
    """Test successful processing."""
    with patch.object(instagram_agent, 'call_ollama', return_value='{"solution": "test"}'):
        request = AgentRequest(agent_type="instagramcurator", message="Create content strategy")
        response = await instagram_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "instagramcurator"


@pytest.mark.asyncio
async def test_process_exception(instagram_agent):
    """Test processing with exception."""
    with patch.object(instagram_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="instagramcurator", message="Test message")
        response = await instagram_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_agent_type_mapping(instagram_agent):
    """Test agent type is correctly mapped."""
    assert instagram_agent.agent_type == "instagramcurator"


@pytest.mark.asyncio
async def test_system_initialize_agent_successfully():
    """Test system initializes agent successfully."""
    from core.agent_manager import AgentManager
    
    agent_manager = AgentManager()
    await agent_manager.initialize()
    
    # Verify agent is loaded in system
    assert "instagramcurator" in agent_manager.agents
    assert isinstance(agent_manager.agents["instagramcurator"], InstagramCuratorAgent)