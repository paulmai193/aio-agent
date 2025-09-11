"""Unit tests for FeedbackSynthesizerAgent."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
from agents.feedback_synthesizer_agent import FeedbackSynthesizerAgent
from core.schemas import AgentRequest, AgentResponse


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = MagicMock()
    return client


@pytest.fixture
def feedback_agent(mock_ollama_client):
    """FeedbackSynthesizerAgent instance."""
    return FeedbackSynthesizerAgent(mock_ollama_client)


def test_uses_correct_model(feedback_agent):
    """Test that agent uses the correct model based on its intended function."""
    with patch('config.settings') as mock_settings:
        mock_settings.MODEL_FEEDBACKSYNTHESIZER = "llama3.2:3b"
        model = feedback_agent.get_model_name()
        assert model == "llama3.2:3b"


def test_system_prompt_matches_instruction_exactly(feedback_agent):
    """Test that agent's system_prompt matches the instruction exactly."""
    prompt = feedback_agent.get_system_prompt()
    
    # Verify key components from the instruction are present exactly
    assert "You are a user feedback virtuoso who transforms the chaos of user opinions into crystal-clear product direction." in prompt
    assert "Your superpower is finding signal in the noise, identifying patterns humans miss, and translating user emotions into specific, actionable improvements." in prompt
    assert "You understand that users often can't articulate what they want, but their feedback reveals what they need." in prompt
    assert "Multi-Source Feedback Aggregation" in prompt
    assert "Pattern Recognition & Theme Extraction" in prompt
    assert "Sentiment Analysis & Urgency Scoring" in prompt
    assert "Actionable Insight Generation" in prompt
    assert "Feedback Loop Optimization" in prompt
    assert "Stakeholder Communication" in prompt
    assert "Feedback Categories to Track" in prompt
    assert "Analysis Techniques" in prompt
    assert "Urgency Scoring Matrix" in prompt
    assert "Insight Quality Checklist" in prompt
    assert "Common Feedback Patterns" in prompt
    assert "Synthesis Deliverables" in prompt
    assert "Anti-Patterns to Avoid" in prompt
    assert "Integration with 6-Week Cycles" in prompt
    assert "Your goal is to be the voice of the user inside the studio" in prompt
    assert "You understand that feedback is a gift, and your role is to unwrap it, understand it, and transform it into product improvements that delight users and drive growth." in prompt


def test_conforms_to_base_agent_schema(feedback_agent):
    """Test that agent conforms to the BaseAgent schema."""
    # Test standard schema structure
    schema = feedback_agent.get_standard_schema()
    assert schema["type"] == "object"
    assert "solution" in schema["properties"]
    assert "implementation" in schema["properties"]
    assert "technologies" in schema["properties"]
    assert "considerations" in schema["properties"]
    assert len(schema["required"]) == 4


@pytest.mark.asyncio
async def test_process_success(feedback_agent):
    """Test successful processing."""
    with patch.object(feedback_agent, 'call_ollama', return_value='{"solution": "test"}'):
        request = AgentRequest(agent_type="feedbacksynthesizer", message="Analyze user feedback")
        response = await feedback_agent.process(request)
        
        assert response.success is True
        assert response.agent_type == "feedbacksynthesizer"


@pytest.mark.asyncio
async def test_process_exception(feedback_agent):
    """Test processing with exception."""
    with patch.object(feedback_agent, 'call_ollama', side_effect=Exception("Ollama error")):
        request = AgentRequest(agent_type="feedbacksynthesizer", message="Test message")
        response = await feedback_agent.process(request)
        
        assert response.success is False
        assert "Ollama error" in response.error


def test_agent_type_mapping(feedback_agent):
    """Test agent type is correctly mapped."""
    assert feedback_agent.agent_type == "feedbacksynthesizer"


@pytest.mark.asyncio
async def test_system_initialize_agent_successfully():
    """Test system initializes agent successfully."""
    from core.agent_manager import AgentManager
    
    agent_manager = AgentManager()
    await agent_manager.initialize()
    
    # Verify agent is loaded in system
    assert "feedbacksynthesizer" in agent_manager.agents
    assert isinstance(agent_manager.agents["feedbacksynthesizer"], FeedbackSynthesizerAgent)