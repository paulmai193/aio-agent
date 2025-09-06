@echo off
echo Setting up Ollama models for Development...

echo Waiting for Ollama to start...
:wait_loop_dev
docker-compose -f docker-compose.dev.yml exec ollama ollama list >nul 2>&1
if errorlevel 1 (
    echo Waiting for Ollama service...
    timeout /t 2 /nobreak >nul
    goto wait_loop_dev
)

echo Ollama is ready. Installing development models...

echo Pulling llama2:7b model...
docker-compose -f docker-compose.dev.yml exec ollama ollama pull llama2:7b

echo Pulling codellama:7b model...
docker-compose -f docker-compose.dev.yml exec ollama ollama pull codellama:7b

echo Pulling deepseek-r1:1.5b model...
docker-compose -f docker-compose.dev.yml exec ollama ollama pull deepseek-r1:1.5b

echo Verifying installed models...
docker-compose -f docker-compose.dev.yml exec ollama ollama list

echo Development model setup complete!
echo You can now use the Agent Orchestrator at http://localhost:8000
pause