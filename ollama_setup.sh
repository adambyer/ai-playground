#!/bin/sh
set -e  # Exit on error

echo "Starting Ollama..."
ollama serve &  # Start Ollama in the background

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until ollama list > /dev/null 2>&1; do
  echo "Ollama is not ready yet..."
  sleep 2
done

# Once ready, pull models
echo "Pulling models..."
ollama pull mistral
ollama pull all-minilm

echo "All models pulled. Keeping Ollama running..."
wait  # Keep Ollama running
