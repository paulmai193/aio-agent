"""Simple test without Unicode issues."""
import asyncio
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_manager import AgentManager
from core.schemas import AgentRequest

# Configure logging for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

async def test_basic_functionality():
    """Test basic functionality without Ollama dependency."""
    print("Testing Agent Manager initialization...")
    
    try:
        manager = AgentManager()
        await manager.initialize()
        print(f"SUCCESS: Initialized {len(manager.agents)} agents")
        
        # Test agent listing
        agents = manager.list_agents()
        print(f"Available agents: {agents}")
        
        # Test health check (will fail without Ollama but shouldn't crash)
        health = await manager.health_check()
        print(f"Health check result: {health}")
        
        # Test invalid agent handling
        request = AgentRequest(agent_type="nonexistent", message="test")
        response = await manager.process_request(request)
        print(f"Invalid agent test: success={response.success}")
        
        await manager.cleanup()
        print("SUCCESS: All basic tests passed")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())