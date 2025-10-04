"""
Log analysis module for DevKit
AI-powered debugging and error analysis
"""

import sys
from pathlib import Path
from typing import Optional
import click

try:
    from . import ai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


def read_log_file(filepath: str) -> str:
    """Read log file content"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read log file: {e}")


def read_stdin() -> str:
    """Read log content from stdin"""
    if sys.stdin.isatty():
        raise RuntimeError("No input provided. Use: cat app.log | devkit logs analyze")
    
    return sys.stdin.read()


def truncate_log(log_content: str, max_lines: int = 500) -> tuple[str, bool]:
    """Truncate log to reasonable size for AI analysis"""
    lines = log_content.split('\n')
    
    if len(lines) <= max_lines:
        return log_content, False
    
    # Keep first 100 and last 400 lines (where errors usually are)
    truncated = '\n'.join(lines[:100] + ['... (truncated) ...'] + lines[-400:])
    return truncated, True


def analyze_log_with_ai(log_content: str, context: str = "") -> str:
    """Send log to AI for analysis"""
    if not AI_AVAILABLE:
        return "❌ AI features not available. Install google-generativeai."
    
    # Truncate if too long
    truncated_log, was_truncated = truncate_log(log_content)
    
    truncation_note = "\n(Note: Log was truncated to fit context window)" if was_truncated else ""
    
    prompt = f"""You are a senior software engineer debugging an application crash.

{context}

Analyze this log file and provide:

1. **Critical Errors**: Identify the main errors or exceptions
2. **Root Cause**: What likely caused the crash?
3. **Stack Trace**: Highlight the relevant stack trace lines
4. **Suggested Fix**: What should the developer do to fix this?
5. **Prevention**: How to prevent this in the future?

Log content:
```
{truncated_log}
```
{truncation_note}

Format your response clearly with sections. Be specific and actionable."""
    
    try:
        client = ai.get_client()
        if not client:
            return "❌ AI not configured. Set GEMINI_API_KEY."
        
        response = client.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"❌ AI analysis failed: {str(e)}"


def extract_error_patterns(log_content: str) -> dict:
    """Extract common error patterns from log"""
    patterns = {
        'exceptions': [],
        'errors': [],
        'warnings': [],
        'stack_traces': []
    }
    
    lines = log_content.split('\n')
    in_stack_trace = False
    current_stack = []
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Detect exceptions
        if 'exception' in line_lower or 'error:' in line_lower:
            patterns['exceptions'].append((i + 1, line.strip()))
            in_stack_trace = True
            current_stack = [line.strip()]
        
        # Detect errors
        elif 'error' in line_lower and 'exception' not in line_lower:
            patterns['errors'].append((i + 1, line.strip()))
        
        # Detect warnings
        elif 'warn' in line_lower:
            patterns['warnings'].append((i + 1, line.strip()))
        
        # Collect stack trace
        elif in_stack_trace:
            if line.strip().startswith('at ') or line.strip().startswith('File '):
                current_stack.append(line.strip())
            else:
                if current_stack:
                    patterns['stack_traces'].append(current_stack)
                    current_stack = []
                in_stack_trace = False
    
    return patterns


def format_analysis_output(analysis: str, patterns: dict) -> str:
    """Format the complete analysis output"""
    output = []
    
    output.append("\n" + "=" * 70)
    output.append("🔍 LOG ANALYSIS RESULTS")
    output.append("=" * 70 + "\n")
    
    # Quick stats
    output.append("📊 Quick Stats:")
    output.append(f"  - Exceptions found: {len(patterns['exceptions'])}")
    output.append(f"  - Errors found: {len(patterns['errors'])}")
    output.append(f"  - Warnings found: {len(patterns['warnings'])}")
    output.append(f"  - Stack traces: {len(patterns['stack_traces'])}\n")
    
    # Show first few exceptions
    if patterns['exceptions']:
        output.append("🔴 Key Exceptions:")
        for line_num, exception in patterns['exceptions'][:5]:
            output.append(f"  Line {line_num}: {exception[:100]}")
        output.append("")
    
    # AI Analysis
    output.append("🤖 AI Analysis:")
    output.append("-" * 70)
    output.append(analysis)
    output.append("-" * 70 + "\n")
    
    return '\n'.join(output)