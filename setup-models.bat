@echo off
echo Setting up Ollama models for Agent Orchestrator...

echo Waiting for Ollama to start...
:wait_loop
docker-compose exec ollama ollama list >nul 2>&1
if errorlevel 1 (
    echo Waiting for Ollama service...
    timeout /t 2 /nobreak >nul
    goto wait_loop
)

echo Ollama is ready. Installing models...

echo Pulling llama2 model...
docker-compose exec ollama ollama pull llama2

echo Pulling codellama model...
docker-compose exec ollama ollama pull codellama

echo Verifying installed models...
docker-compose exec ollama ollama list

echo Model setup complete!
echo You can now use the Agent Orchestrator at http://localhost:8000
pause