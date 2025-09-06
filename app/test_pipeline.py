"""
Test script để kiểm tra pipeline processing với dependencies.
"""
import asyncio
import json
from core.task_orchestrator import TaskOrchestrator
from core.ollama_client import OllamaClient

async def test_pipeline_processing():
    """Test pipeline processing với sample tasks."""
    
    # Sample tasks với dependencies
    sample_tasks = [
        {
            "task_description": "Research target audience for AI startup",
            "agent_type": "trendresearcher",
            "priority": 1,
            "dependencies": []
        },
        {
            "task_description": "Create marketing content based on research findings",
            "agent_type": "contentcreator", 
            "priority": 2,
            "dependencies": [0]  # Depends on task 0
        },
        {
            "task_description": "Design landing page using the marketing content",
            "agent_type": "uidesigner",
            "priority": 3, 
            "dependencies": [1]  # Depends on task 1
        }
    ]
    
    print("Sample pipeline tasks:")
    print(json.dumps(sample_tasks, indent=2))
    
    # Test dependency validation
    ollama_client = OllamaClient()
    orchestrator = TaskOrchestrator(ollama_client)
    
    validated_tasks = orchestrator._validate_dependencies(sample_tasks)
    print("\nValidated tasks:")
    print(json.dumps(validated_tasks, indent=2))
    
    await ollama_client.close()

if __name__ == "__main__":
    asyncio.run(test_pipeline_processing())