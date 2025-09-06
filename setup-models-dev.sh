#!/bin/bash

echo "Setting up Ollama models for Development..."

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until docker-compose -f docker-compose.dev.yml exec ollama ollama list > /dev/null 2>&1; do
    echo "Waiting for Ollama service..."
    sleep 2
done

echo "Ollama is ready. Installing development models..."

# Pull lightweight models for development
echo "Pulling llama2:7b model..."
docker-compose -f docker-compose.dev.yml exec ollama ollama pull llama2:7b

echo "Pulling codellama:7b model..."
docker-compose -f docker-compose.dev.yml exec ollama ollama pull codellama:7b

echo "Pulling deepseek-r1:1.5b model..."
docker-compose -f docker-compose.dev.yml exec ollama ollama pull deepseek-r1:1.5b

# Verify installation
echo "Verifying installed models..."
docker-compose -f docker-compose.dev.yml exec ollama ollama list

echo "Development model setup complete!"
echo "You can now use the Agent Orchestrator at http://localhost:8000"