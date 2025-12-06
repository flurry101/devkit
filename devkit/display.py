"""
Display utilities for DevKit
Handles intro display, loading indicators, and formatted output
"""

import sys
import time
from typing import Optional

# Try to import TerminalTextEffects for intro
try:
    from terminaltexteffects.effects.effect_print import Print
    TTE_AVAILABLE = True
except ImportError:
    TTE_AVAILABLE = False

# Also try BinaryPath for status command
try:
    from terminaltexteffects.effects.effect_binarypath import BinaryPath
    BINARYPATH_AVAILABLE = True
except ImportError:
    BINARYPATH_AVAILABLE = False

# Try to import Rich for markdown formatting
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from . import storage

# Intro text (using raw string to avoid escape sequence warnings)
INTRO_TEXT = r"""                                                         
                                                             
                                      ,-.            ___     
       ,---,                      ,--/ /|   ,--,   ,--.'|_   
     ,---.'|                    ,--. :/ | ,--.'|   |  | :,'  
     |   | :               .---.:  : ' /  |  |,    :  : ' :  
     |   | |   ,---.     /.  ./||  '  /   `--'_  .;__,'  /   
   ,--.__| |  /     \  .-' . ' |'  |  :   ,' ,'| |  |   |    
  /   ,'   | /    /  |/___/ \: ||  |   \  '  | | :__,'| :    
 .   '  /  |.    ' / |.   \  ' .'  : |. \ |  | :   '  : |__  
 '   ; |:  |'   ;   /| \   \   '|  | ' \ \'  : |__ |  | '.'| 
 |   | '/  ''   |  / |  \   \   '  : |--' |  | '.'|;  :    ; 
 |   :    :||   :    |   \   \ |;  |,'    ;  :    ;|  ,   /  
  \   \  /   \   \  /     '---" '--'      |  ,   /  ---`-'   
   `----'     `----'                       ---`-'            
                                                             

⌜AI-powered terminal assistant for developers⌟

DevKit is your smart companion for the command line. 
It helps you find the right commands without leaving your terminal, 
manage and reuse helpful snippets, write perfect git commits, 
and even turn back time when things go wrong. 
Spend less time searching and more time coding."""

# Global console instance
_console: Optional[Console] = None
_intro_shown = False


def get_console() -> Console:
    """Get or create Rich console instance"""
    global _console
    if _console is None:
        _console = Console()
    return _console


def show_intro_once():
    """Show intro with TerminalTextEffects on first use"""
    global _intro_shown
    
    if _intro_shown:
        return
    
    # Check if intro was already shown (stored in config)
    config = storage.load_config()
    if config.get('intro_shown', False):
        _intro_shown = True
        return
    
    # Show intro with TerminalTextEffects
    if TTE_AVAILABLE:
        try:
            effect = Print(INTRO_TEXT)
            with effect.terminal_output() as terminal:
                for frame in effect:
                    terminal.print(frame)
                    time.sleep(0.01)  # Small delay for animation
        except Exception:
            # Fallback to plain print
            print(INTRO_TEXT)
    else:
        # Fallback if TTE not available
        print(INTRO_TEXT)
    
    # Mark intro as shown
    config['intro_shown'] = True
    storage.save_config(config)
    _intro_shown = True
    
    # Add spacing
    print("\n" + "=" * 70 + "\n")


def show_loading_progress(task_description: str = "Processing..."):
    """Show a loading progress bar using Rich"""
    if not RICH_AVAILABLE:
        print(f"{task_description}...")
        return None
    
    console = get_console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(task_description, total=100)
        
        # Animate progress
        for i in range(0, 101, 5):
            progress.update(task, completed=i)
            time.sleep(0.02)
        
        progress.update(task, completed=100)
    
    return None


def format_ai_response(response: str, query: str, show_suggestions: bool = True) -> str:
    """Format AI response with suggestions, citations, and markdown"""
    if not RICH_AVAILABLE:
        # Fallback to plain text
        return response
    
    # Extract structured response parts
    lines = response.split('\n')
    command = None
    explanation = []
    detailed_notes = []
    citations = []
    
    current_section = None
    
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith('COMMAND:'):
            command = line.replace('COMMAND:', '').strip()
            current_section = None
        elif line_stripped.startswith('EXPLANATION:'):
            explanation.append(line.replace('EXPLANATION:', '').strip())
            current_section = 'explanation'
        elif line_stripped.startswith('DETAILED_NOTES:'):
            detailed_notes.append(line.replace('DETAILED_NOTES:', '').strip())
            current_section = 'notes'
        elif line_stripped.startswith('CITATIONS:'):
            citations.append(line.replace('CITATIONS:', '').strip())
            current_section = 'citations'
        elif current_section == 'explanation' and line_stripped:
            explanation.append(line_stripped)
        elif current_section == 'notes' and line_stripped:
            detailed_notes.append(line_stripped)
        elif current_section == 'citations' and line_stripped:
            citations.append(line_stripped)
        elif not current_section and line_stripped and not command:
            # Fallback: if no structured format, treat as explanation
            explanation.append(line_stripped)
    
    # Build markdown content with green styling for AI suggestions
    markdown_content = f"# AI Response for: `{query}`\n\n"
    
    if command and show_suggestions:
        # Highlight AI suggestions in green
        markdown_content += f"## <span style='color: green; font-weight: bold'>💡 AI Suggested Command</span>\n\n```bash\n{command}\n```\n\n"
    
    if explanation:
        explanation_text = ' '.join(explanation) if isinstance(explanation, list) else explanation
        # Fix numbered lists formatting
        explanation_text = format_numbered_lists(explanation_text)
        markdown_content += f"## 📝 Explanation\n\n{explanation_text}\n\n"
    
    if detailed_notes:
        notes_text = ' '.join(detailed_notes) if isinstance(detailed_notes, list) else detailed_notes
        markdown_content += f"### 💡 Additional Notes\n\n{notes_text}\n\n"
    
    # Add citations
    if citations:
        citations_text = ' '.join(citations) if isinstance(citations, list) else citations
        markdown_content += "---\n\n"
        markdown_content += f"### 📚 Official Documentation\n\n{citations_text}\n\n"
    
    # Add AI source citation
    markdown_content += "---\n\n"
    markdown_content += "*Source: AI-powered analysis using Google Gemini*\n"
    markdown_content += "*Powered by DevKit AI*"
    
    return markdown_content


def format_numbered_lists(text: str) -> str:
    """Format numbered lists properly for markdown"""
    import re
    # Fix patterns like "1. " or "1)" at start of lines
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        # Match numbered lists: 1. 2. 3. or 1) 2) 3)
        if re.match(r'^\s*\d+[.)]\s+', line):
            # Ensure proper markdown list format
            line = re.sub(r'^(\s*)(\d+)([.)])\s+', r'\1\2\3 ', line)
        formatted_lines.append(line)
    return '\n'.join(formatted_lines)


def display_ai_output(content: str, title: Optional[str] = None):
    """Display AI output with Rich markdown formatting and green AI suggestions"""
    if not RICH_AVAILABLE:
        # Fallback to plain text
        print(content)
        return
    
    console = get_console()
    
    # Parse and display markdown
    markdown = Markdown(content)
    
    if title:
        # Display in a panel with green title for AI suggestions
        panel = Panel(
            markdown,
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(panel)
    else:
        # Display markdown with green styling for AI suggestions
        # Highlight "Suggested Command" sections in green
        console.print(markdown)
    
    # Add spacing
    console.print()


def display_command_explanation(command: str, explanation: str):
    """Display command explanation with citations"""
    if not RICH_AVAILABLE:
        print("=" * 70)
        print(explanation)
        print("=" * 70)
        return
    
    console = get_console()
    
    # Parse structured response
    lines = explanation.split('\n')
    main_explanation = []
    detailed_notes = []
    citations = []
    
    current_section = 'explanation'
    
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith('EXPLANATION:'):
            main_explanation.append(line.replace('EXPLANATION:', '').strip())
            current_section = 'explanation'
        elif line_stripped.startswith('DETAILED_NOTES:'):
            detailed_notes.append(line.replace('DETAILED_NOTES:', '').strip())
            current_section = 'notes'
        elif line_stripped.startswith('CITATIONS:'):
            citations.append(line.replace('CITATIONS:', '').strip())
            current_section = 'citations'
        elif current_section == 'explanation' and line_stripped:
            main_explanation.append(line_stripped)
        elif current_section == 'notes' and line_stripped:
            detailed_notes.append(line_stripped)
        elif current_section == 'citations' and line_stripped:
            citations.append(line_stripped)
        elif not any(line_stripped.startswith(s) for s in ['EXPLANATION:', 'DETAILED_NOTES:', 'CITATIONS:']):
            # Fallback: treat as explanation if no structure
            if not main_explanation:
                main_explanation.append(line_stripped)
    
    # Build markdown content
    markdown_content = f"# Command Explanation\n\n## `{command}`\n\n"
    
    if main_explanation:
        explanation_text = ' '.join(main_explanation) if isinstance(main_explanation, list) else main_explanation
        # Fix numbered lists formatting
        explanation_text = format_numbered_lists(explanation_text)
        markdown_content += f"{explanation_text}\n\n"
    
    if detailed_notes:
        notes_text = ' '.join(detailed_notes) if isinstance(detailed_notes, list) else detailed_notes
        markdown_content += f"### 💡 Additional Notes\n\n{notes_text}\n\n"
    
    if citations:
        citations_text = ' '.join(citations) if isinstance(citations, list) else citations
        markdown_content += "---\n\n"
        markdown_content += f"### 📚 Official Documentation\n\n{citations_text}\n\n"
    
    markdown_content += "---\n\n*Source: AI-powered analysis using Google Gemini*"
    
    markdown = Markdown(markdown_content)
    
    panel = Panel(
        markdown,
        title="[cyan]🔍 Command Explanation[/cyan]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(panel)
    console.print()


def display_analysis(analysis: str, title: str = "AI Analysis"):
    """Display AI analysis with formatting"""
    if not RICH_AVAILABLE:
        print("=" * 70)
        print(analysis)
        print("=" * 70)
        return
    
    console = get_console()
    
    markdown_content = f"# {title}\n\n{analysis}\n\n---\n\n*Source: AI-powered analysis using Google Gemini*"
    markdown = Markdown(markdown_content)
    
    panel = Panel(
        markdown,
        title=f"[yellow]{title}[/yellow]",
        border_style="yellow",
        box=box.ROUNDED
    )
    console.print(panel)
    console.print()

