@echo off
echo Setting up Ollama models for Production...

echo Waiting for Ollama to start...
:wait_loop_prod
docker-compose -f docker-compose.prod.yml exec ollama ollama list >nul 2>&1
if errorlevel 1 (
    echo Waiting for Ollama service...
    timeout /t 2 /nobreak >nul
    goto wait_loop_prod
)

echo Ollama is ready. Installing production models...

echo Pulling llama2:13b model...
docker-compose -f docker-compose.prod.yml exec ollama ollama pull llama2:13b

echo Pulling codellama:13b model...
docker-compose -f docker-compose.prod.yml exec ollama ollama pull codellama:13b

echo Pulling deepseek-r1:7b model...
docker-compose -f docker-compose.prod.yml exec ollama ollama pull deepseek-r1:7b

echo Verifying installed models...
docker-compose -f docker-compose.prod.yml exec ollama ollama list

echo Production model setup complete!
echo You can now use the Agent Orchestrator at http://localhost:8000
pause