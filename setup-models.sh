#!/bin/bash

echo "Setting up Ollama models for Agent Orchestrator..."

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until docker-compose exec ollama ollama list > /dev/null 2>&1; do
    echo "Waiting for Ollama service..."
    sleep 2
done

echo "Ollama is ready. Installing models..."

# Pull required models
echo "Pulling llama2 model..."
docker-compose exec ollama ollama pull llama2

echo "Pulling codellama model..."
docker-compose exec ollama ollama pull codellama

echo "Pulling deepseek-r1:1.5b model..."
docker-compose exec ollama ollama pull deepseek-r1:1.5b

# Verify installation
echo "Verifying installed models..."
docker-compose exec ollama ollama list

echo "Model setup complete!"
echo "You can now use the Agent Orchestrator at http://localhost:8000"