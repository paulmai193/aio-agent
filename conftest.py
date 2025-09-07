"""Pytest configuration and shared fixtures."""
import pytest
import sys
import os

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for Windows compatibility."""
    import asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


@pytest.fixture(autouse=True)
def mock_logging():
    """Mock logging to avoid Unicode issues in tests."""
    import logging
    from unittest.mock import patch
    
    with patch.object(logging, 'basicConfig'):
        yield