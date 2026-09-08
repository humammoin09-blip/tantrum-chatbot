"""
llm.py - OpenRouter API Client for Tantrum Chatbot.

Provides a reusable function `get_ai_response` to communicate with LLM models
via OpenRouter, with robust error handling and environment configuration.
"""

import os
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")


class LLMError(Exception):
    """Custom exception raised for LLM API errors."""
    pass


def get_ai_response(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.85,
    max_tokens: int = 600,
    timeout: int = 30
) -> str:
    """
    Sends a chat completion request to the OpenRouter API.

    Args:
        messages: A list of message dictionaries (e.g., [{"role": "user", "content": "..."}]).
        model: OpenRouter model identifier (defaults to OPENROUTER_MODEL env or free Llama 3.3).
        temperature: Sampling temperature for creativity / emotional range (default: 0.85).
        max_tokens: Maximum tokens in the generated response (default: 600).
        timeout: Request timeout in seconds (default: 30).

    Returns:
        The generated response string from the AI.

    Raises:
        LLMError: If the API key is missing, network fails, or the API returns an error.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key or api_key.strip() == "" or api_key.strip() == "your_openrouter_api_key_here":
        raise LLMError(
            "OPENROUTER_API_KEY is not configured. Please set your key in the .env file."
        )

    selected_model = model or DEFAULT_MODEL

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/tantrum-chatbot",
        "X-Title": "Tantrum Chatbot"
    }

    payload = {
        "model": selected_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=timeout
        )

        # Handle common HTTP status codes
        if response.status_code == 401:
            raise LLMError("Authentication failed: Invalid OpenRouter API Key.")
        elif response.status_code == 402:
            raise LLMError("Payment required: Insufficient credits on OpenRouter account.")
        elif response.status_code == 429:
            raise LLMError("Rate limit exceeded: Too many requests sent to OpenRouter.")
        elif response.status_code >= 500:
            raise LLMError(f"OpenRouter server error (HTTP {response.status_code}). Please try again later.")

        response.raise_for_status()
        data = response.json()

        # Parse response choices
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            message = choice.get("message", {})
            content = message.get("content", "")
            if content:
                return content.strip()
            else:
                raise LLMError("Received empty response from the AI model.")
        elif "error" in data:
            err_msg = data["error"].get("message", "Unknown error from OpenRouter.")
            raise LLMError(f"OpenRouter Error: {err_msg}")
        else:
            raise LLMError(f"Unexpected response structure from OpenRouter: {data}")

    except requests.exceptions.Timeout:
        raise LLMError(f"Request timed out after {timeout} seconds.")
    except requests.exceptions.ConnectionError:
        raise LLMError("Failed to connect to OpenRouter API. Check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise LLMError(f"Network request error: {str(e)}")
    except ValueError as e:
        raise LLMError(f"Failed to parse JSON response: {str(e)}")
