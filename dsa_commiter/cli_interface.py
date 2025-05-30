#!/usr/bin/env python3
"""
Simplified CLI Interface for dsa-commiter
Handles user interaction for creating directories/files and auto-pushing to Git.
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from dsa_commiter.file_operations import FileOperations
from dsa_commiter.git_operations import GitOperations

console = Console()

def get_multiline_input(prompt, default=None):
    """Get multiline input from the user, ending with Ctrl+D or two blank lines."""
    console.print(prompt)
    lines = []
    blank_line_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                blank_line_count += 1
                if blank_line_count >= 2 and lines:
                    break
            else:
                blank_line_count = 0
                lines.append(line)
        except EOFError:  # Ctrl+D
            break
        except KeyboardInterrupt:
            console.print("[yellow]⚠️ Input cancelled[/yellow]")
            return None
    
    content = "\n".join(lines).strip()
    return content if content else default

class CLIInterface:
    """Simplified CLI interface for DSA Commiter."""
    
    def __init__(self):
        self.file_ops = FileOperations()
        self.git_ops = GitOperations()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        """Main CLI loop."""
        while True:
            try:
                self.clear_screen()
                console.print(Panel("[bold cyan]🚀 DSA Commiter CLI 🚀[/bold cyan]", border_style="blue"))
                console.print("[cyan]Create a directory and file, add content, and auto-push to Git.[/cyan]")
                console.print("[dim]💡 Press Ctrl+C to exit, Ctrl+D or two blank lines to end content input[/dim]\n")
                
                # Get directory name
                dir_name = Prompt.ask("[cyan]📁 Enter directory name (or press Enter for current directory)[/cyan]").strip()
                
                # Get file name
                console.print("\n[cyan]📝 Supported file extensions:[/cyan]")
                extensions = list(self.file_ops.default_contents.keys())
                console.print(", ".join(f".{ext}" for ext in extensions))
                filename = Prompt.ask("[cyan]📄 Enter file name with extension (e.g., solution.py)[/cyan]").strip()
                
                # Validate filename
                if not filename:
                    console.print("[red]❌ File name cannot be empty[/red]")
                    console.print("\n[dim]Press Enter to continue...[/dim]")
                    input()
                    continue
                invalid_chars = '<>:"/\\|?*'
                if any(char in filename for char in invalid_chars):
                    console.print(f"[red]❌ Invalid characters in filename: {invalid_chars}[/red]")
                    console.print("\n[dim]Press Enter to continue...[/dim]")
                    input()
                    continue
                
                # Get file content
                extension = filename.split('.')[-1].lower() if '.' in filename else ''
                default_content = self.file_ops.default_contents.get(extension, "Hello World!")
                prompt = f"[cyan]📝 Enter file content (Ctrl+D or two blank lines to end, Enter for default {extension} template):[/cyan]"
                content = get_multiline_input(prompt, default=default_content)
                if content is None:
                    console.print("\n[dim]Press Enter to try again...[/dim]")
                    input()
                    continue
                
                # Create directory and file
                success = self.file_ops.create_directory_and_file(dir_name, filename, content)
                if not success:
                    console.print("\n[dim]Press Enter to try again...[/dim]")
                    input()
                    continue
                
                # Auto commit and push
                file_path = os.path.join(dir_name, filename) if dir_name else filename
                self.git_ops.auto_commit_and_push(file_path)
                
                console.print("\n[dim]Press Enter to create another file or Ctrl+C to exit...[/dim]")
                input()
                
            except KeyboardInterrupt:
                console.print("\n[bold green]👋 Goodbye! Thanks for using DSA Commiter CLI![/bold green]")
                break
            except Exception as e:
                console.print(f"[red]❌ Unexpected error: {e}[/red]")
                console.print("\n[dim]Press Enter to try again...[/dim]")
                input()

def main():
    """Main entry point for the CLI application."""
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n[bold green]👋 Application terminated by user. Goodbye![/bold green]")
    except Exception as e:
        console.print(f"[red]❌ Fatal error occurred: {e}[/red]")

if __name__ == "__main__":
    main()