"""
Telecom Proposal Engine - LLM Engine (Gemini via LangChain)
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import GOOGLE_API_KEY, GEMINI_MODEL
from prompts import SYSTEM_PROMPT


def get_llm(task="chat"):
    """Get configured Gemini instance. Tasks: chat, agreement, extraction."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in .env")
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


def invoke_llm(prompt, task="chat", system=None):
    """Send prompt to Gemini with system message. Returns text."""
    try:
        msgs = [
            SystemMessage(content=system or SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
        return get_llm(task).invoke(msgs).content.strip()
    except Exception as e:
        return f"[LLM Error: {e}]"


def invoke_simple(prompt, task="chat"):
    """Simple invocation without system message."""
    try:
        return get_llm(task).invoke(prompt).content.strip()
    except Exception as e:
        return f"[LLM Error: {e}]"