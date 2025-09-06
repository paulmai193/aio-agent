"""Unit tests for Pydantic schemas."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import ValidationError
from core.schemas import AgentRequest, AgentResponse, OllamaRequest, OllamaResponse, HealthResponse


def test_agent_request_valid():
    """Test valid AgentRequest creation."""
    request = AgentRequest(
        agent_type="aiengineer",
        message="Test message",
        context={"key": "value"},
        parameters={"param": "value"}
    )
    
    assert request.agent_type == "aiengineer"
    assert request.message == "Test message"
    assert request.context == {"key": "value"}
    assert request.parameters == {"param": "value"}


def test_agent_request_minimal():
    """Test AgentRequest with minimal required fields."""
    request = AgentRequest(
        agent_type="aiengineer",
        message="Test message"
    )
    
    assert request.agent_type == "aiengineer"
    assert request.message == "Test message"
    assert request.context is None
    assert request.parameters is None


def test_agent_request_empty_agent_type():
    """Test AgentRequest with empty agent_type."""
    with pytest.raises(ValidationError) as exc_info:
        AgentRequest(agent_type="", message="Test message")
    
    assert "agent_type" in str(exc_info.value)


def test_agent_request_empty_message():
    """Test AgentRequest with empty message."""
    with pytest.raises(ValidationError) as exc_info:
        AgentRequest(agent_type="aiengineer", message="")
    
    assert "message" in str(exc_info.value)


def test_agent_request_missing_fields():
    """Test AgentRequest with missing required fields."""
    with pytest.raises(ValidationError):
        AgentRequest()


def test_agent_response_success():
    """Test successful AgentResponse creation."""
    response = AgentResponse(
        agent_type="aiengineer",
        response="Test response",
        metadata={"model": "test-model"},
        success=True
    )
    
    assert response.agent_type == "aiengineer"
    assert response.response == "Test response"
    assert response.metadata == {"model": "test-model"}
    assert response.success is True
    assert response.error is None


def test_agent_response_error():
    """Test error AgentResponse creation."""
    response = AgentResponse(
        agent_type="aiengineer",
        response="",
        success=False,
        error="Test error"
    )
    
    assert response.agent_type == "aiengineer"
    assert response.response == ""
    assert response.success is False
    assert response.error == "Test error"


def test_agent_response_defaults():
    """Test AgentResponse with default values."""
    response = AgentResponse(
        agent_type="aiengineer",
        response="Test response"
    )
    
    assert response.success is True  # Default
    assert response.error is None  # Default
    assert response.metadata is None  # Default


def test_ollama_request_minimal():
    """Test minimal OllamaRequest creation."""
    request = OllamaRequest(
        model="test-model",
        prompt="Test prompt"
    )
    
    assert request.model == "test-model"
    assert request.prompt == "Test prompt"
    assert request.stream is False  # Default
    assert request.options is None  # Default


def test_ollama_request_full():
    """Test full OllamaRequest creation."""
    request = OllamaRequest(
        model="test-model",
        prompt="Test prompt",
        stream=True,
        options={"temperature": 0.7}
    )
    
    assert request.model == "test-model"
    assert request.prompt == "Test prompt"
    assert request.stream is True
    assert request.options == {"temperature": 0.7}


def test_ollama_response_minimal():
    """Test minimal OllamaResponse creation."""
    response = OllamaResponse(
        model="test-model",
        response="Test response",
        done=True
    )
    
    assert response.model == "test-model"
    assert response.response == "Test response"
    assert response.done is True


def test_ollama_response_full():
    """Test full OllamaResponse creation."""
    response = OllamaResponse(
        model="test-model",
        response="Test response",
        done=True,
        context=[1, 2, 3],
        total_duration=1000,
        load_duration=100,
        prompt_eval_count=10,
        prompt_eval_duration=200,
        eval_count=20,
        eval_duration=300
    )
    
    assert response.model == "test-model"
    assert response.response == "Test response"
    assert response.done is True
    assert response.context == [1, 2, 3]
    assert response.total_duration == 1000
    assert response.load_duration == 100
    assert response.prompt_eval_count == 10
    assert response.prompt_eval_duration == 200
    assert response.eval_count == 20
    assert response.eval_duration == 300


def test_health_response():
    """Test HealthResponse creation."""
    response = HealthResponse(
        status="healthy",
        agents_loaded=11,
        ollama_connected=True
    )
    
    assert response.status == "healthy"
    assert response.agents_loaded == 11
    assert response.ollama_connected is True


def test_health_response_unhealthy():
    """Test unhealthy HealthResponse creation."""
    response = HealthResponse(
        status="unhealthy",
        agents_loaded=0,
        ollama_connected=False
    )
    
    assert response.status == "unhealthy"
    assert response.agents_loaded == 0
    assert response.ollama_connected is False