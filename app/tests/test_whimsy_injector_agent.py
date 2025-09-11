"""Unit tests for WhimsyInjectorAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.whimsy_injector_agent import WhimsyInjectorAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def whimsy_agent(mock_ollama_client):
    """WhimsyInjectorAgent instance."""
    return WhimsyInjectorAgent(mock_ollama_client)


def test_uses_correct_model(whimsy_agent):
    """Test that agent uses the correct model based on its intended function."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_WHIMSYINJECTOR = "mistral:7b"
        model = whimsy_agent.get_model_name()
        assert model == "mistral:7b"


def test_system_prompt_matches_instruction_exactly(whimsy_agent):
    """Test that agent's system_prompt matches the instruction exactly."""
    prompt = whimsy_agent.get_system_prompt()
    
    # Verify key components from the instruction are present exactly
    assert "You are a master of digital delight, an expert in transforming functional interfaces into joyful experiences that users can't help but share." in prompt
    assert "You understand that in a world of boring, utilitarian apps, whimsy is a competitive advantage." in prompt
    assert "Delight Opportunity Identification" in prompt
    assert "Micro-Interaction Design" in prompt
    assert "Emotional Journey Mapping" in prompt
    assert "Playful Copy Enhancement" in prompt
    assert "Shareable Moment Creation" in prompt
    assert "Performance-Conscious Delight" in prompt
    assert "Whimsy Injection Points" in prompt
    assert "Animation Principles" in prompt
    assert "Copy Personality Guidelines" in prompt
    assert "Emergency Delight Kit" in prompt
    assert "Your goal is to ensure no user interaction feels mundane or mechanical." in prompt
    assert "Remember: in the attention economy, boring is the only unforgivable sin." in prompt


def test_conforms_to_base_agent_schema(whimsy_agent):
    """Test that agent conforms to the BaseAgent schema."""
    # Test standard schema structure
    schema = whimsy_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "solution" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "technologies" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 4


@pytest.mark.asyncio
async def test_process_success(whimsy_agent):
    """Test successful processing."""
    with patch.object(whimsy_agent, 'call_ollama', return_value='{"solution": "test"}'):
        request = AgentRequest(agent_type="whimsyinjector", message="Add delight to loading state")
        response = await whimsy_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "whimsyinjector"


@pytest.mark.asyncio
async def test_process_exception(whimsy_agent):
    """Test processing with exception."""
    with patch.object(whimsy_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="whimsyinjector", message="Test message")
        response = await whimsy_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_agent_type_mapping(whimsy_agent):
    """Test agent type is correctly mapped."""
    assert whimsy_agent.agent_type == "whimsyinjector"