"""
AI module for DevKit
Handles all Gemini API interactions
"""

import google.generativeai as genai
from typing import Optional
from .storage import get_api_key


def get_client() -> Optional[genai.GenerativeModel]:
    """Get Gemini client with API key"""
    api_key = get_api_key()
    
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')


def ask_command(query: str) -> str:
    """Ask AI to suggest a command for a query"""
    client = get_client()
    
    if not client:
        return "❌ API key not configured. Set GEMINI_API_KEY environment variable."
    
    prompt = f"""You are a terminal command expert. The user wants to: {query}

Respond with ONLY the command they should run, followed by a brief explanation.

Format:
COMMAND: <the actual command>
EXPLANATION: <brief 1-line explanation>

Be concise and practical. Assume they're on a Unix-like system (Linux/Mac)."""
    
    try:
        response = client.generate_content(prompt)
        return response.text
    
    except Exception as e:
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str:
            return "⏱️ Rate limit reached. Wait a moment and try again."
        elif "api_key" in error_str or "authentication" in error_str:
            return "🔑 Invalid API key. Run: devkit config --api-key <key>"
        elif "quota" in error_str:
            return "💳 API quota exceeded. Check your Google AI Studio account."
        else:
            return f"❌ API error: {str(e)}"


def explain_command(command: str) -> str:
    """Explain what a command does"""
    client = get_client()
    
    if not client:
        return "❌ API key not configured. Set GEMINI_API_KEY environment variable."
    
    prompt = f"""Explain this terminal command in simple terms:

{command}

Break it down part by part and explain what each part does. Be concise but clear.
If there are any potential risks or important notes, mention them."""
    
    try:
        response = client.generate_content(prompt)
        return response.text
    
    except Exception as e:
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str:
            return "⏱️ Rate limit reached. Wait a moment and try again."
        elif "api_key" in error_str or "authentication" in error_str:
            return "🔑 Invalid API key. Run: devkit config --api-key <key>"
        elif "quota" in error_str:
            return "💳 API quota exceeded. Check your Google AI Studio account."
        else:
            return f"❌ API error: {str(e)}"


def generate_commit_message(diff: str) -> str:
    """Generate a commit message from git diff"""
    client = get_client()
    
    if not client:
        return "❌ API key not configured. Set GEMINI_API_KEY environment variable."
    
    prompt = f"""You are a git commit message expert. Analyze this git diff and generate a conventional commit message.

Git diff:
{diff[:3000]}  

Generate a commit message in this format:
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore
Keep the description concise (under 50 chars).

Respond with ONLY the commit message, nothing else."""
    
    try:
        response = client.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str:
            return "⏱️ Rate limit reached. Wait a moment and try again."
        elif "api_key" in error_str or "authentication" in error_str:
            return "🔑 Invalid API key. Run: devkit config --api-key <key>"
        elif "quota" in error_str:
            return "💳 API quota exceeded. Check your Google AI Studio account."
        else:
            return f"❌ API error: {str(e)}"


def analyze_history(history: list) -> str:
    """Analyze command history to find issues (time-travel debugging)"""
    client = get_client()
    
    if not client:
        return "❌ API key not configured. Set GEMINI_API_KEY environment variable."
    
    # Format history for AI
    formatted_history = "\n".join([
        f"{i+1}. {entry['command']} (exit code: {entry['exit_code']})"
        for i, entry in enumerate(history[-10:])  # Last 10 commands
    ])
    
    prompt = f"""You are debugging a terminal session. Here are the last commands run:

{formatted_history}

Analyze this sequence and:
1. Identify any failed commands (non-zero exit codes)
2. Explain what likely went wrong
3. Suggest how to fix it
4. Point out if earlier commands caused the issue

Be concise and actionable."""
    
    try:
        response = client.generate_content(prompt)
        return response.text
    
    except Exception as e:
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str:
            return "⏱️ Rate limit reached. Wait a moment and try again."
        elif "api_key" in error_str or "authentication" in error_str:
            return "🔑 Invalid API key. Run: devkit config --api-key <key>"
        elif "quota" in error_str:
            return "💳 API quota exceeded. Check your Google AI Studio account."
        else:
            return f"❌ API error: {str(e)}"


def suggest_rollback(dangerous_commands: list) -> str:
    """Suggest rollback commands for dangerous operations"""
    client = get_client()
    
    if not client:
        return "❌ API key not configured. Set GEMINI_API_KEY environment variable."
    
    formatted_commands = "\n".join([
        f"- {cmd['command']} ({cmd['timestamp']})"
        for cmd in dangerous_commands
    ])
    
    prompt = f"""These potentially dangerous commands were just run:

{formatted_commands}

For each command, suggest how to rollback/undo it safely.
Be specific with exact commands to run.

Format your response as:
ROLLBACK STEPS:
1. <command> - <explanation>
2. <command> - <explanation>
etc.

Be practical and safe. If rollback is risky, warn about it."""
    
    try:
        response = client.generate_content(prompt)
        return response.text
    
    except Exception as e:
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str:
            return "⏱️ Rate limit reached. Wait a moment and try again."
        elif "api_key" in error_str or "authentication" in error_str:
            return "🔑 Invalid API key. Run: devkit config --api-key <key>"
        elif "quota" in error_str:
            return "💳 API quota exceeded. Check your Google AI Studio account."
        else:
            return f"❌ API error: {str(e)}"