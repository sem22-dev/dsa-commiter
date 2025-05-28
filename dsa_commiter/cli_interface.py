
#!/usr/bin/env python3
"""
CLI Interface for dsa-commiter
Manages the user interface and coordinates file and Git operations.
"""

import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dsa_commiter.file_operations import FileOperations
from dsa_commiter.git_operations import GitOperations

console = Console()

class CLIInterface:
    """Main CLI interface for dsa-commiter."""
    
    def __init__(self):
        self.file_ops = FileOperations()
        self.git_ops = GitOperations()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the main menu with enhanced UI."""
        self.clear_screen()
        console.print(Panel.fit("[bold cyan]🚀 DSA Commiter CLI 🚀[/bold cyan]", border_style="blue"))
        table = Table(show_header=False, expand=True)
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")
        menu_items = [
            ("1", "📁 Create Directory/File", "Create a new directory and file with template"),
            ("2", "🔄 Git Add/Commit/Push", "Stage, commit, and push files to Git"),
            ("3", "📂 List Directory Contents", "Show files and directories in current location"),
            ("4", "👋 Exit", "Exit the application")
        ]
        for num, title, desc in menu_items:
            table.add_row(f"{num}. {title}", desc)
        console.print(table)
        console.print("[dim]💡 Use Ctrl+C to cancel any operation[/dim]")

    def create_directory_and_file(self):
        """Interactive directory and file creation."""
        console.print(Panel("[bold green]📁 Create Directory and File[/bold green]", border_style="green"))
        
        dir_name = Prompt.ask("[cyan]📁 Enter directory name (or press Enter to use current directory)[/cyan]").strip()
        console.print("\n[cyan]📝 Supported file extensions:[/cyan]")
        extensions = list(self.file_ops.default_contents.keys())
        console.print(", ".join(f".{ext}" for ext in extensions))
        
        filename = Prompt.ask("[cyan]📄 Enter file name with extension (e.g., main.py)[/cyan]").strip()
        if not filename:
            console.print("[red]❌ File name cannot be empty[/red]")
            return

        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        default_content = self.file_ops.default_contents.get(extension, "Hello World!")
        content = Prompt.ask(
            f"[cyan]📝 Enter file content (or press Enter for default {extension} template)[/cyan]",
            default=default_content, show_default=False
        ).strip() or default_content

        self.file_ops.create_directory_and_file(dir_name, filename, content)
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def git_push(self):
        """Interactive Git add, commit, and push."""
        console.print(Panel("[bold green]🔄 Git Add/Commit/Push[/bold green]", border_style="green"))
        
        if not self.git_ops.is_git_repository():
            console.print("[yellow]⚠️ This directory is not a Git repository[/yellow]")
            if Confirm.ask("[cyan]🔧 Initialize Git repository?[/cyan]"):
                if not self.git_ops.initialize_git():
                    return
            else:
                console.print("[yellow]⚠️ Git operation cancelled[/yellow]")
                return

        files, _ = self.file_ops.list_directory_contents()
        if not files:
            console.print("[yellow]⚠️ No files found in current directory[/yellow]")
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
            return

        console.print(f"\n[cyan]📂 Files in {self.file_ops.current_dir}:[/cyan]")
        table = Table(title="Available Files")
        table.add_column("No.", style="cyan")
        table.add_column("File", style="white")
        for i, file in enumerate(files, 1):
            table.add_row(str(i), file)
        console.print(table)

        choice = Prompt.ask("[cyan]Enter file number to push (or 'all' for all files, 'q' to cancel)[/cyan]").strip().lower()
        if choice == 'q':
            console.print("[yellow]⚠️ Git push cancelled[/yellow]")
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
            return

        if choice == 'all':
            files_to_push = files
        else:
            try:
                file_index = int(choice) - 1
                if 0 <= file_index < len(files):
                    files_to_push = [files[file_index]]
                else:
                    console.print("[red]❌ Invalid file number[/red]")
                    console.print("\n[dim]Press Enter to continue...[/dim]")
                    input()
                    return
            except ValueError:
                console.print("[red]❌ Invalid input[/red]")
                console.print("\n[dim]Press Enter to continue...[/dim]")
                input()
                return

        if not Confirm.ask(f"[cyan]Confirm push for {', '.join(files_to_push)}?[/cyan]"):
            console.print("[yellow]⚠️ Git push cancelled[/yellow]")
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
            return

        commit_message = Prompt.ask("[cyan]📝 Enter commit message[/cyan]", default="Update files")
        self.git_ops.git_add_commit_push(files_to_push, commit_message)
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def list_directory(self):
        """Display directory contents in a table."""
        console.print(Panel(f"[bold green]📂 Contents of {self.file_ops.current_dir}[/bold green]", border_style="green"))
        files, dirs = self.file_ops.list_directory_contents()
        
        table = Table()
        table.add_column("Type", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Size", style="yellow")
        
        for dir_name in dirs:
            table.add_row("📁 Dir", dir_name, "-")
        for file_name in files:
            size = os.path.getsize(os.path.join(self.file_ops.current_dir, file_name))
            table.add_row("📄 File", file_name, str(size))
        
        console.print(table)
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def run(self):
        """Main CLI loop."""
        while True:
            try:
                self.display_menu()
                choice = Prompt.ask("[cyan]🎯 Enter your choice (1-4)[/cyan]").strip()
                
                if choice == '1':
                    self.create_directory_and_file()
                elif choice == '2':
                    self.git_push()
                elif choice == '3':
                    self.list_directory()
                elif choice == '4':
                    console.print(Panel("[bold green]👋 Goodbye! Thanks for using DSA Commiter CLI![/bold green]", border_style="green"))
                    break
                else:
                    console.print("[red]❌ Invalid choice. Please enter 1-4.[/red]")
                    console.print("\n[dim]Press Enter to continue...[/dim]")
                    input()
                    
            except KeyboardInterrupt:
                console.print("\n[bold green]👋 Goodbye! Thanks for using DSA Commiter CLI![/bold green]")
                break
            except Exception as e:
                console.print(f"[red]❌ Unexpected error: {e}[/red]")
                console.print("\n[dim]Press Enter to continue...[/dim]")
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