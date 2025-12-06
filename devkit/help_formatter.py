"""
Custom help formatter for DevKit with Rich colors
"""

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def format_help_text(ctx, formatter):
    """Format help text with Rich colors"""
    if not RICH_AVAILABLE:
        # Fallback to default Click formatting
        return False
    
    console = Console()
    
    # Get command info
    command = ctx.command
    command_name = ctx.command_path if hasattr(ctx, 'command_path') else 'devkit'
    
    # Create a panel for the main help
    help_text = command.help or command.short_help or ""
    
    # Format usage
    # ctx.command_path already includes the full path from root, so use it directly
    usage_text = command_name
    if ctx.params:
        usage_text += " [OPTIONS]"
    if hasattr(command, 'params'):
        for param in command.params:
            if not param.is_flag and not param.default:
                usage_text += f" <{param.name}>"
    
    # Display usage in cyan
    console.print(f"\n[bold cyan]Usage:[/bold cyan] [bold white]{usage_text}[/bold white]")
    
    # Display description
    if help_text:
        console.print(f"\n[bold cyan]Description:[/bold cyan]")
        console.print(help_text)
    
    # Display options
    if ctx.params:
        console.print(f"\n[bold cyan]Options:[/bold cyan]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="bold yellow", width=20)
        table.add_column(style="dim")
        
        for param in ctx.params:
            opts = ", ".join(param.opts)
            table.add_row(opts, param.help or "")
        
        console.print(table)
    
    # Display commands (for groups)
    if hasattr(command, 'commands'):
        console.print(f"\n[bold cyan]Commands:[/bold cyan]")
        table = Table(
            show_header=False,
            box=box.SIMPLE,
            padding=(0, 2),
            border_style="cyan",
            show_lines=False
        )
        table.add_column(style="bold white", width=20, no_wrap=True)
        table.add_column(style="white", width=60, overflow="fold")
        
        for cmd_name, cmd in sorted(command.commands.items()):
            short_help = cmd.short_help or cmd.help or ""
            # Get first line of help text
            if '\n' in short_help:
                short_help = short_help.split('\n')[0]
            # Truncate if too long
            if len(short_help) > 55:
                short_help = short_help[:52] + "..."
            table.add_row(cmd_name, short_help)
        
        console.print(table)
    
    console.print()
    return True


