"""Test script để kiểm tra tích hợp agents."""
import asyncio
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_manager import AgentManager
from core.schemas import AgentRequest

logging.basicConfig(level=logging.INFO)

async def test_agents():
    """Test tất cả agents."""
    manager = AgentManager()
    await manager.initialize()
    
    # Test requests cho từng loại agent
    test_cases = [
        ("aiengineer", "Tích hợp AI chatbot vào ứng dụng web"),
        ("uidesigner", "Thiết kế giao diện đăng nhập hiện đại"),
        ("contentcreator", "Tạo content marketing cho app mobile"),
        ("backendarchitect", "Thiết kế API cho hệ thống e-commerce"),
        ("frontenddeveloper", "Xây dựng dashboard React responsive"),
        ("rapidprototyper", "Tạo MVP cho app chia sẻ ảnh"),
        ("growthhacker", "Chiến lược tăng trưởng user cho startup"),
        ("trendresearcher", "Xu hướng công nghệ 2024"),
        ("devopsautomator", "Setup CI/CD pipeline cho dự án"),
        ("testwriterfixer", "Viết unit test cho API endpoint"),
        ("projectshipper", "Kế hoạch launch sản phẩm mới")
    ]
    
    print(f"Testing {len(test_cases)} agents...")
    
    for agent_type, message in test_cases:
        print(f"\n--- Testing {agent_type} ---")
        request = AgentRequest(agent_type=agent_type, message=message)
        
        try:
            response = await manager.process_request(request)
            if response.success:
                print(f"✅ {agent_type}: OK")
                print(f"Response preview: {response.response[:100]}...")
            else:
                print(f"❌ {agent_type}: {response.error}")
        except Exception as e:
            logging.error(f"Agent {agent_type} exception: {e}", exc_info=True)
            print(f"❌ {agent_type}: Exception - {e}")
    
    await manager.cleanup()
    print(f"\nCompleted testing {len(test_cases)} agents")

if __name__ == "__main__":
    asyncio.run(test_agents())