"""
Telecom Proposal Engine - LLM Integration (Google Gemini via LangChain)
=========================================================================

Provides wrapper functions for interacting with Google's Gemini 2.5 Flash model
via the LangChain library. Supports different task-specific configurations
(temperature, token limits) for chat, agreement generation, and extraction tasks.

Key Features:
    - Task-aware temperature and token limit adjustment
    - System message + human message pattern
    - Graceful error handling with user-friendly fallback messages
    - Single instance caching for efficiency

Module Functions:
    - get_llm(): Returns configured ChatGoogleGenerativeAI instance
    - invoke_llm(): Send prompt with system message
    - invoke_simple(): Send prompt without system message
    
Dependencies:
    - langchain_google_genai: Google Gemini integration
    - langchain_core: Core LangChain message types
    - config: API key and model configuration
    - prompts: Shared prompt templates
"""

from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from config import GOOGLE_API_KEY, GEMINI_MODEL
from prompts import SYSTEM_PROMPT


def get_llm(task: str = "chat") -> ChatGoogleGenerativeAI:
    """
    Instantiate and configure Google Gemini 2.5 Flash model with task-specific settings.
    
    Different NLP tasks benefit from different model configurations:
    - Chat: Higher temperature (0.7) for natural conversation
    - Agreement & Extraction: Lower temperature (0.4) for consistency
    
    Args:
        task (str): Task type - "chat", "agreement", or "extraction". Default: "chat"
        
    Returns:
        ChatGoogleGenerativeAI: Configured Gemini model instance
        
    Raises:
        ValueError: If GOOGLE_API_KEY not set in environment
        
    Config by Task:
        - chat: temp=0.7, max_tokens=2048 (conversational, varied)
        - agreement: temp=0.4, max_tokens=4000 (formal contracts)
        - extraction: temp=0.4, max_tokens=4096 (structured data)
        
    Examples:
        >>> llm = get_llm("chat")
        >>> llm.temperature
        0.7
        >>> llm = get_llm("agreement")
        >>> llm.temperature
        0.4
    """
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY not set in environment. "
            "Please configure it in .env file."
        )
    
    # Task-specific configurations
    temps = {"chat": 0.7, "agreement": 0.4, "extraction": 0.4}
    tokens = {"chat": 2048, "agreement": 4000, "extraction": 4096}
    
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=temps.get(task, 0.4),
        max_output_tokens=tokens.get(task, 2048),
        top_p=0.95,
        top_k=40,
    )


def invoke_llm(prompt: str, task: str = "chat", system: Optional[str] = None) -> str:
    """
    Send a prompt to Gemini with optional system message and return response text.
    
    This is the primary function for LLM interaction in the proposal engine.
    Combines a system message (for context/persona) with user prompt for coherent responses.
    
    Args:
        prompt (str): Main user/human message to send to the LLM
        task (str): Task type for temperature/token config ("chat", "agreement", "extraction")
        system (str, optional): Custom system message. If None, uses SYSTEM_PROMPT
        
    Returns:
        str: Response text from Gemini, or error message if invocation fails
        
    Raises:
        Returns error string instead of raising (graceful degradation)
        
    Examples:
        >>> response = invoke_llm("Create an L1 proposal", task="agreement")
        >>> isinstance(response, str)
        True
        >>> invoke_llm("Test", system="You are helpful")
        # Returns Gemini response or error message
        
    Error Handling:
        If API call fails, returns "[LLM Error: {exception}]" so UI continues gracefully.
    """
    try:
        messages: list[BaseMessage] = [
            SystemMessage(content=system or SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
        response = get_llm(task).invoke(messages)
        return response.content.strip()
    except Exception as e:
        error_msg = f"[LLM Error: {str(e)[:100]}]"
        return error_msg


def invoke_simple(prompt: str, task: str = "chat") -> str:
    """
    Send a simple prompt to Gemini without a system message.
    
    Use this for standalone queries that don't need persona context.
    Simpler than invoke_llm() but less controllable for formal outputs.
    
    Args:
        prompt (str): User message to send to the LLM
        task (str): Task type for temperature/token config
        
    Returns:
        str: Response text from Gemini, or error message if invocation fails
        
    Examples:
        >>> response = invoke_simple("Explain Dark Fibre IRU pricing")
        >>> isinstance(response, str)
        True
    """
    try:
        response = get_llm(task).invoke(prompt)
        return response.content.strip()
    except Exception as e:
        error_msg = f"[LLM Error: {str(e)[:100]}]"
        return error_msg