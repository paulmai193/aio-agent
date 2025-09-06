"""Unit tests for OllamaClient."""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, MagicMock, patch
import aiohttp
from core.ollama_client import OllamaClient
from core.schemas import OllamaRequest, OllamaResponse


@pytest.fixture
def ollama_client():
    """OllamaClient instance."""
    return OllamaClient()


@pytest.fixture
def mock_session():
    """Mock aiohttp session."""
    session = MagicMock()
    session.closed = False
    return session


@pytest.mark.asyncio
async def test_get_session_new(ollama_client):
    """Test creating new session."""
    session = await ollama_client._get_session()
    assert session is not None
    assert isinstance(session, aiohttp.ClientSession)


@pytest.mark.asyncio
async def test_get_session_reuse(ollama_client):
    """Test reusing existing session."""
    session1 = await ollama_client._get_session()
    session2 = await ollama_client._get_session()
    assert session1 is session2


@pytest.mark.asyncio
async def test_generate_success(ollama_client):
    """Test successful generation."""
    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value={
        "model": "test-model",
        "response": "Test response",
        "done": True
    })
    mock_response.raise_for_status = MagicMock()
    
    mock_session = MagicMock()
    mock_session.post.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.post.return_value.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(ollama_client, '_get_session', return_value=mock_session):
        request = OllamaRequest(model="test-model", prompt="Test prompt")
        response = await ollama_client.generate(request)
        
        assert isinstance(response, OllamaResponse)
        assert response.model == "test-model"
        assert response.response == "Test response"
        assert response.done is True


@pytest.mark.asyncio
async def test_generate_connection_error(ollama_client):
    """Test generation with connection error."""
    mock_session = MagicMock()
    mock_session.post.side_effect = aiohttp.ClientConnectorError(
        connection_key=MagicMock(), os_error=Exception("Connection failed")
    )
    
    with patch.object(ollama_client, '_get_session', return_value=mock_session):
        request = OllamaRequest(model="test-model", prompt="Test prompt")
        
        with pytest.raises(aiohttp.ClientConnectorError):
            await ollama_client.generate(request)


@pytest.mark.asyncio
async def test_list_models_success(ollama_client):
    """Test successful model listing."""
    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value={
        "models": [{"name": "model1"}, {"name": "model2"}]
    })
    mock_response.raise_for_status = MagicMock()
    
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(ollama_client, '_get_session', return_value=mock_session):
        result = await ollama_client.list_models()
        
        assert "models" in result
        assert len(result["models"]) == 2


@pytest.mark.asyncio
async def test_list_models_error(ollama_client):
    """Test model listing with error."""
    mock_session = MagicMock()
    mock_session.get.side_effect = aiohttp.ClientError("Request failed")
    
    with patch.object(ollama_client, '_get_session', return_value=mock_session):
        with pytest.raises(aiohttp.ClientError):
            await ollama_client.list_models()


@pytest.mark.asyncio
async def test_health_check_success(ollama_client):
    """Test successful health check."""
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(ollama_client, '_get_session', return_value=mock_session):
        result = await ollama_client.health_check()
        assert result is True


@pytest.mark.asyncio
async def test_health_check_failure(ollama_client):
    """Test health check failure."""
    mock_session = MagicMock()
    mock_session.get.side_effect = Exception("Connection failed")
    
    with patch.object(ollama_client, '_get_session', return_value=mock_session):
        result = await ollama_client.health_check()
        assert result is False


@pytest.mark.asyncio
async def test_close_session_exists(ollama_client):
    """Test closing existing session."""
    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.close = AsyncMock()
    ollama_client._session = mock_session
    
    await ollama_client.close()
    mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_close_no_session(ollama_client):
    """Test closing when no session exists."""
    ollama_client._session = None
    # Should not raise exception
    await ollama_client.close()


@pytest.mark.asyncio
async def test_close_session_already_closed(ollama_client):
    """Test closing already closed session."""
    mock_session = MagicMock()
    mock_session.closed = True
    mock_session.close = AsyncMock()
    ollama_client._session = mock_session
    
    await ollama_client.close()
    mock_session.close.assert_not_called()