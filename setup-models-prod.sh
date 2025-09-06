#!/bin/bash

echo "Setting up Ollama models for Production..."

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until docker-compose -f docker-compose.prod.yml exec ollama ollama list > /dev/null 2>&1; do
    echo "Waiting for Ollama service..."
    sleep 2
done

echo "Ollama is ready. Installing production models..."

# Pull full models for production
echo "Pulling llama2:13b model..."
docker-compose -f docker-compose.prod.yml exec ollama ollama pull llama2:13b

echo "Pulling codellama:13b model..."
docker-compose -f docker-compose.prod.yml exec ollama ollama pull codellama:13b

echo "Pulling deepseek-r1:7b model..."
docker-compose -f docker-compose.prod.yml exec ollama ollama pull deepseek-r1:7b

# Verify installation
echo "Verifying installed models..."
docker-compose -f docker-compose.prod.yml exec ollama ollama list

echo "Production model setup complete!"
echo "You can now use the Agent Orchestrator at http://localhost:8000"