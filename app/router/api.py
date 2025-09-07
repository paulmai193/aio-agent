"""
API endpoints cho Agent Orchestrator.
"""
import logging
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from core.agent_manager import AgentManager
from core.task_orchestrator import TaskOrchestrator
from core.schemas import AgentRequest, AgentResponse, HealthResponse


logger = logging.getLogger(__name__)
router = APIRouter()


class UserRequest(BaseModel):
    """Request model cho user input."""
    message: str = Field(..., min_length=1, description="User message cannot be empty")
    context: Optional[Dict[str, Any]] = None

class TaskResponse(BaseModel):
    """Response model cho orchestrated tasks."""
    tasks: List[Dict[str, Any]]
    results: List[AgentResponse]
    success: bool
    error: Optional[str] = None

def get_agent_manager(request: Request) -> AgentManager:
    """Dependency để lấy agent manager."""
    return request.app.state.agent_manager


@router.post("/chat", response_model=AgentResponse)
async def chat_endpoint(
    request: AgentRequest,
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Endpoint chính để xử lý request từ user."""
    try:
        logger.info(f"Nhận request cho agent: {request.agent_type}, message: {request.message[:50]}...")
        
        # Detect language using LanguageDetectorAgent
        lang_request = AgentRequest(
            agent_type="languagedetector",
            message=request.message
        )
        lang_response = await agent_manager.process_request(lang_request)
        
        if lang_response.success:
            detected_lang = lang_response.response.strip()
            logger.info(f"Detected language: {detected_lang}")
            
            # Language instructions
            lang_instructions = {
                'vi': 'Hãy trả lời bằng tiếng Việt.',
                'en': 'Please respond in English.',
                'zh': '请用中文回答。',
                'ja': '日本語で回答してください。',
                'ko': '한국어로 답변해 주세요.',
                'fr': 'Veuillez répondre en français.',
                'de': 'Bitte antworten Sie auf Deutsch.',
                'es': 'Por favor responda en español.',
            }
            
            lang_instruction = lang_instructions.get(detected_lang, lang_instructions['en'])
            
            # Enhance request with language instruction
            enhanced_context = dict(request.context) if request.context else {}
            enhanced_context['language'] = detected_lang
            enhanced_message = f"{request.message}\n\n{lang_instruction}"
            
            enhanced_request = AgentRequest(
                agent_type=request.agent_type,
                message=enhanced_message,
                context=enhanced_context
            )
        else:
            enhanced_request = request
        
        response = await agent_manager.process_request(enhanced_request)
        
        if not response.success:
            logger.warning(f"Agent {request.agent_type} failed: {response.error}")
            raise HTTPException(status_code=400, detail=response.error)
        
        logger.info(f"Agent {request.agent_type} processed successfully")
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi xử lý request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents", response_model=List[str])
async def list_agents(
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Lấy danh sách các agent có sẵn."""
    logger.debug("Listing available agents")
    agents = agent_manager.list_agents()
    logger.debug(f"Found {len(agents)} agents")
    return agents


@router.get("/health", response_model=HealthResponse)
async def health_check(
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Health check endpoint."""
    try:
        logger.debug("Health check requested")
        health_data = await agent_manager.health_check()
        
        status = "healthy" if health_data["ollama_connected"] else "degraded"
        logger.debug(f"Health check status: {status}")
        
        return HealthResponse(
            status=status,
            agents_loaded=health_data["agents_loaded"],
            ollama_connected=health_data["ollama_connected"]
        )
    
    except Exception as e:
        logger.error(f"Lỗi health check: {e}")
        return HealthResponse(
            status="unhealthy",
            agents_loaded=0,
            ollama_connected=False
        )


@router.post("/process", response_model=TaskResponse)
async def process_user_request(
    request: UserRequest,
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    """Process user request with automatic task orchestration."""
    try:
        logger.info(f"Processing user request: {request.message[:50]}...")
        
        # Detect language using LanguageDetectorAgent
        lang_request = AgentRequest(
            agent_type="languagedetector",
            message=request.message
        )
        lang_response = await agent_manager.process_request(lang_request)
        
        detected_lang = 'en'  # Default
        lang_instruction = 'Please respond in English.'
        
        if lang_response.success:
            detected_lang = lang_response.response.strip()
            logger.info(f"Detected language: {detected_lang}")
            
            # Language instructions
            lang_instructions = {
                'vi': 'Hãy trả lời bằng tiếng Việt.',
                'en': 'Please respond in English.',
                'zh': '请用中文回答。',
                'ja': '日本語で回答してください。',
                'ko': '한국어로 답변해 주세요.',
                'fr': 'Veuillez répondre en français.',
                'de': 'Bitte antworten Sie auf Deutsch.',
                'es': 'Por favor responda en español.',
            }
            
            lang_instruction = lang_instructions.get(detected_lang, lang_instructions['en'])
        
        # Initialize task orchestrator
        orchestrator = TaskOrchestrator(agent_manager.ollama_client)
        
        # Analyze and split request into tasks
        tasks = await orchestrator.analyze_and_split_request(request.message)
        logger.info(f"Request split into {len(tasks)} tasks")
        
        # Execute tasks with dependency-based pipeline processing
        results = []
        task_outputs = {}
        completed_tasks = set()
        task_map = {i: task for i, task in enumerate(tasks)}
        
        while len(completed_tasks) < len(tasks):
            executed_in_round = False
            
            for i, task in task_map.items():
                if i in completed_tasks:
                    continue
                
                # Check if all dependencies are completed
                dependencies = task.get('dependencies', [])
                if not all(dep in completed_tasks for dep in dependencies):
                    continue
                
                # Build enhanced message with dependency outputs and language instruction
                enhanced_message = task['task_description']
                enhanced_context = dict(request.context) if request.context else {}
                enhanced_context['language'] = detected_lang
                
                if dependencies:
                    enhanced_context['previous_outputs'] = {
                        f"task_{dep}": task_outputs[dep] for dep in dependencies
                    }
                    
                    # Inject dependency outputs into message
                    for dep in dependencies:
                        enhanced_message += f"\n\n--- Output from previous task {dep} ---\n{task_outputs[dep]}"
                
                # Add language instruction to ensure consistent language
                enhanced_message += f"\n\n{lang_instruction}"
                
                # Create enhanced agent request
                agent_request = AgentRequest(
                    agent_type=task['agent_type'],
                    message=enhanced_message,
                    context=enhanced_context
                )
                
                # Process task
                logger.info(f"Executing task {i}: {task['agent_type']} (deps: {dependencies})")
                result = await agent_manager.process_request(agent_request)
                results.append(result)
                task_outputs[i] = result.response
                completed_tasks.add(i)
                executed_in_round = True
                
                if not result.success:
                    logger.warning(f"Task {i} failed: {result.error}")
            
            # Prevent infinite loop if no tasks can be executed
            if not executed_in_round:
                logger.error("Circular dependency detected or invalid task structure")
                break
        
        # Check overall success
        overall_success = all(r.success for r in results) and len(completed_tasks) == len(tasks)
        
        return TaskResponse(
            tasks=tasks,
            results=results,
            success=overall_success,
            error=None if overall_success else "Some tasks failed"
        )
        
    except Exception as e:
        logger.error(f"Error processing user request: {e}")
        return TaskResponse(
            tasks=[],
            results=[],
            success=False,
            error=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing user request: {e}")
        return TaskResponse(
            tasks=[],
            results=[],
            success=False,
            error=str(e)
        )