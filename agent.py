"""
Core agent module for the Legacy Code Documentation Agent.
Handles communication with the LLM.
"""

import os
from dotenv import load_dotenv
import litellm

from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Load environment variables
load_dotenv()

# Get the default model from .env
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

# Cost per 1K tokens (approximate, as of 2024)
# Update these as pricing changes
COST_PER_1K_TOKENS = {
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gemini/gemini-1.5-flash": {"input": 0.000075, "output": 0.0003},
    "gemini/gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
    "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
    "claude-opus-4-20250514": {"input": 0.015, "output": 0.075},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the estimated cost for an API call.

    Args:
        model: The model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in USD
    """
    if model not in COST_PER_1K_TOKENS:
        return 0.0  # Unknown model, can't estimate

    pricing = COST_PER_1K_TOKENS[model]
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]

    return input_cost + output_cost


def generate_documentation(filename: str, language: str, code_content: str) -> dict:
    """
    Send code to the LLM and get documentation back.

    Args:
        filename: Name of the code file
        language: Programming language (SQL, Python, etc.)
        code_content: The actual code to document

    Returns:
        Dictionary with keys: 'success', 'documentation', 'error', 'model_used', 'usage'
    """
    result = {
        "success": False,
        "documentation": None,
        "error": None,
        "model_used": DEFAULT_MODEL,
        "usage": {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "estimated_cost": 0.0
        }
    }

    # Build the user message from our template
    user_message = USER_PROMPT_TEMPLATE.format(
        language=language,
        filename=filename,
        code_content=code_content
    )

    try:
        # Make the API call using litellm
        response = litellm.completion(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the documentation from the response
        result["documentation"] = response.choices[0].message.content
        result["success"] = True

        # Capture token usage
        if hasattr(response, 'usage') and response.usage:
            result["usage"]["input_tokens"] = response.usage.prompt_tokens
            result["usage"]["output_tokens"] = response.usage.completion_tokens
            result["usage"]["total_tokens"] = response.usage.total_tokens
            result["usage"]["estimated_cost"] = calculate_cost(
                DEFAULT_MODEL,
                response.usage.prompt_tokens,
                response.usage.completion_tokens
            )

    except Exception as e:
        result["error"] = f"LLM API error: {str(e)}"

    return result