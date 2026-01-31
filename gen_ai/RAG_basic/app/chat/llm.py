"""
LLM module using Ollama (open-source, local LLM).
"""
import os
import requests
from typing import List

# Ollama API endpoint (default local installation)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def generate_response(query: str, context: List[str]) -> str:
    """Generate a response using Ollama with the given context."""
    
    # Build the prompt with context
    context_text = "\n\n".join(context) if context else "No relevant context found."
    
    prompt = f"""You are a helpful assistant. Answer the question based on the provided context.
If the context doesn't contain relevant information, say so and provide a general answer.

Context:
{context_text}

Question: {query}

Answer:"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "Failed to generate response.")
    
    except requests.exceptions.ConnectionError:
        return f"Error: Cannot connect to Ollama at {OLLAMA_BASE_URL}. Make sure Ollama is running."
    except requests.exceptions.Timeout:
        return "Error: Request to Ollama timed out."
    except Exception as e:
        return f"Error generating response: {str(e)}"


def check_ollama_health() -> bool:
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False
