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
            ("4", "🔍 Show Files and Options", "Display files with detailed options"),
            ("5", "📋 Choose Directory to Create", "Select or create a specific directory"),
            ("6", "📁 Show Directory and Options", "Display directory structure with options"),
            ("7", "🗂️ Create Directory/Files Inside It", "Create nested directories and files"),
            ("8", "🔧 Git Push (Still Failed? Fix It)", "Enhanced Git push with error handling"),
            ("9", "👋 Exit", "Exit the application")
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

    def show_files_and_options(self):
        """Display files with detailed options and actions."""
        console.print(Panel("[bold green]🔍 Files and Options[/bold green]", border_style="green"))
        
        files, dirs = self.file_ops.list_directory_contents()
        if not files and not dirs:
            console.print("[yellow]⚠️ No files or directories found[/yellow]")
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
            return
        
        # Display files and directories with options
        table = Table(title="Files and Directories with Options")
        table.add_column("No.", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Name", style="white")
        table.add_column("Size/Items", style="green")
        table.add_column("Actions", style="magenta")
        
        all_items = []
        for i, dir_name in enumerate(dirs, 1):
            items_count = len(os.listdir(os.path.join(self.file_ops.current_dir, dir_name)))
            table.add_row(str(i), "📁 Dir", dir_name, f"{items_count} items", "Enter, Delete, Rename")
            all_items.append(("dir", dir_name))
        
        for i, file_name in enumerate(files, len(dirs) + 1):
            size = os.path.getsize(os.path.join(self.file_ops.current_dir, file_name))
            table.add_row(str(i), "📄 File", file_name, f"{size} bytes", "Edit, Delete, Rename, Git Push")
            all_items.append(("file", file_name))
        
        console.print(table)
        
        choice = Prompt.ask("[cyan]Enter item number for options (or 'q' to go back)[/cyan]").strip().lower()
        if choice == 'q':
            return
        
        try:
            item_index = int(choice) - 1
            if 0 <= item_index < len(all_items):
                item_type, item_name = all_items[item_index]
                self.handle_item_options(item_type, item_name)
            else:
                console.print("[red]❌ Invalid item number[/red]")
        except ValueError:
            console.print("[red]❌ Invalid input[/red]")
        
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def handle_item_options(self, item_type, item_name):
        """Handle options for selected file or directory."""
        console.print(f"\n[bold cyan]Options for {item_type}: {item_name}[/bold cyan]")
        
        if item_type == "file":
            options = ["1. Edit content", "2. Delete file", "3. Rename file", "4. Git push this file", "5. Back"]
        else:
            options = ["1. Enter directory", "2. Delete directory", "3. Rename directory", "4. Back"]
        
        for option in options:
            console.print(f"[cyan]{option}[/cyan]")
        
        choice = Prompt.ask("[cyan]Enter your choice[/cyan]").strip()
        
        if item_type == "file":
            if choice == "1":
                self.edit_file_content(item_name)
            elif choice == "2":
                self.file_ops.delete_item(item_name, "file")
            elif choice == "3":
                self.file_ops.rename_item(item_name, "file")
            elif choice == "4":
                commit_message = Prompt.ask("[cyan]Enter commit message[/cyan]", default="Update file")
                self.git_ops.git_add_commit_push([item_name], commit_message)
        else:
            if choice == "1":
                self.file_ops.change_directory(item_name)
            elif choice == "2":
                self.file_ops.delete_item(item_name, "directory")
            elif choice == "3":
                self.file_ops.rename_item(item_name, "directory")

    def edit_file_content(self, filename):
        """Edit file content interactively."""
        file_path = os.path.join(self.file_ops.current_dir, filename)
        try:
            with open(file_path, 'r') as f:
                current_content = f.read()
            
            console.print(f"\n[cyan]Current content of {filename}:[/cyan]")
            console.print(Panel(current_content, border_style="blue"))
            
            new_content = Prompt.ask("[cyan]Enter new content (or press Enter to keep current)[/cyan]", default=current_content)
            
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            console.print(f"[green]✅ File {filename} updated successfully[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error editing file: {e}[/red]")

    def choose_directory_to_create(self):
        """Interactive directory selection and creation."""
        console.print(Panel("[bold green]📋 Choose Directory to Create[/bold green]", border_style="green"))
        
        files, dirs = self.file_ops.list_directory_contents()
        
        console.print(f"[cyan]Current directory: {self.file_ops.current_dir}[/cyan]")
        console.print("[cyan]Available directories:[/cyan]")
        
        table = Table()
        table.add_column("No.", style="cyan")
        table.add_column("Directory", style="white")
        
        for i, dir_name in enumerate(dirs, 1):
            table.add_row(str(i), dir_name)
        
        console.print(table)
        console.print("[cyan]Options:[/cyan]")
        console.print("• Enter directory number to navigate into it")
        console.print("• Type 'new' to create a new directory")
        console.print("• Type 'back' to go to parent directory")
        console.print("• Type 'q' to quit")
        
        choice = Prompt.ask("[cyan]Enter your choice[/cyan]").strip().lower()
        
        if choice == 'q':
            return
        elif choice == 'new':
            new_dir = Prompt.ask("[cyan]Enter new directory name[/cyan]").strip()
            if new_dir:
                self.file_ops.create_directory_and_file(new_dir, "", "")
        elif choice == 'back':
            self.file_ops.go_to_parent_directory()
        else:
            try:
                dir_index = int(choice) - 1
                if 0 <= dir_index < len(dirs):
                    self.file_ops.change_directory(dirs[dir_index])
                else:
                    console.print("[red]❌ Invalid directory number[/red]")
            except ValueError:
                console.print("[red]❌ Invalid input[/red]")
        
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def show_directory_and_options(self):
        """Display directory structure with enhanced options."""
        console.print(Panel("[bold green]📁 Directory Structure and Options[/bold green]", border_style="green"))
        
        self.file_ops.display_directory_tree()
        
        console.print("\n[cyan]Directory Options:[/cyan]")
        options = [
            "1. Navigate to subdirectory",
            "2. Create new directory here",
            "3. Create file in current directory", 
            "4. Go to parent directory",
            "5. Show directory statistics",
            "6. Back to main menu"
        ]
        
        for option in options:
            console.print(f"[cyan]{option}[/cyan]")
        
        choice = Prompt.ask("[cyan]Enter your choice[/cyan]").strip()
        
        if choice == "1":
            self.navigate_to_subdirectory()
        elif choice == "2":
            dir_name = Prompt.ask("[cyan]Enter new directory name[/cyan]").strip()
            if dir_name:
                self.file_ops.create_directory_and_file(dir_name, "", "")
        elif choice == "3":
            filename = Prompt.ask("[cyan]Enter filename with extension[/cyan]").strip()
            if filename:
                self.file_ops.create_directory_and_file("", filename)
        elif choice == "4":
            self.file_ops.go_to_parent_directory()
        elif choice == "5":
            self.file_ops.show_directory_statistics()
        
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def navigate_to_subdirectory(self):
        """Navigate to a subdirectory."""
        files, dirs = self.file_ops.list_directory_contents()
        if not dirs:
            console.print("[yellow]⚠️ No subdirectories found[/yellow]")
            return
        
        console.print("[cyan]Available directories:[/cyan]")
        for i, dir_name in enumerate(dirs, 1):
            console.print(f"[cyan]{i}. {dir_name}[/cyan]")
        
        choice = Prompt.ask("[cyan]Enter directory number[/cyan]").strip()
        try:
            dir_index = int(choice) - 1
            if 0 <= dir_index < len(dirs):
                self.file_ops.change_directory(dirs[dir_index])
            else:
                console.print("[red]❌ Invalid directory number[/red]")
        except ValueError:
            console.print("[red]❌ Invalid input[/red]")

    def create_nested_structure(self):
        """Create directories and files inside them."""
        console.print(Panel("[bold green]🗂️ Create Nested Directory Structure[/bold green]", border_style="green"))
        
        parent_dir = Prompt.ask("[cyan]Enter parent directory name[/cyan]").strip()
        if not parent_dir:
            console.print("[red]❌ Parent directory name cannot be empty[/red]")
            return
        
        # Create parent directory
        success = self.file_ops.create_directory_and_file(parent_dir, "", "")
        if not success:
            return
        
        # Ask for nested structure
        while True:
            console.print(f"\n[cyan]Creating structure inside: {parent_dir}[/cyan]")
            console.print("[cyan]Options:[/cyan]")
            console.print("1. Create subdirectory")
            console.print("2. Create file")
            console.print("3. Finish and go back")
            
            choice = Prompt.ask("[cyan]Enter your choice[/cyan]").strip()
            
            if choice == "1":
                subdir_name = Prompt.ask("[cyan]Enter subdirectory name[/cyan]").strip()
                if subdir_name:
                    nested_path = os.path.join(parent_dir, subdir_name)
                    self.file_ops.create_directory_and_file(nested_path, "", "")
            elif choice == "2":
                filename = Prompt.ask("[cyan]Enter filename with extension[/cyan]").strip()
                if filename:
                    self.file_ops.create_file_in_directory(parent_dir, filename)
            elif choice == "3":
                break
            else:
                console.print("[red]❌ Invalid choice[/red]")
        
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    def enhanced_git_push(self):
        """Enhanced Git push with better error handling and diagnostics."""
        console.print(Panel("[bold green]🔧 Enhanced Git Push (Troubleshooting)[/bold green]", border_style="green"))
        
        # Run diagnostics first
        console.print("[cyan]🔍 Running Git diagnostics...[/cyan]")
        diagnostics = self.git_ops.run_git_diagnostics()
        
        if not diagnostics['is_git_repo']:
            console.print("[yellow]⚠️ Not a Git repository[/yellow]")
            if Confirm.ask("[cyan]Initialize Git repository?[/cyan]"):
                if not self.git_ops.initialize_git():
                    return
            else:
                return
        
        # Check for common issues
        if not diagnostics['has_remote']:
            console.print("[yellow]⚠️ No remote repository configured[/yellow]")
            remote_url = Prompt.ask("[cyan]Enter remote repository URL[/cyan]").strip()
            if remote_url:
                self.git_ops.add_remote(remote_url)
        
        if not diagnostics['has_commits']:
            console.print("[yellow]⚠️ No commits found[/yellow]")
            console.print("[cyan]You need to make an initial commit first[/cyan]")
        
        # Show current status
        self.git_ops.show_git_status()
        
        # Proceed with push
        files, _ = self.file_ops.list_directory_contents()
        if not files:
            console.print("[yellow]⚠️ No files found[/yellow]")
            return
        
        console.print(f"\n[cyan]📂 Files in {self.file_ops.current_dir}:[/cyan]")
        table = Table(title="Available Files")
        table.add_column("No.", style="cyan")
        table.add_column("File", style="white")
        table.add_column("Status", style="yellow")
        
        for i, file in enumerate(files, 1):
            status = self.git_ops.get_file_git_status(file)
            table.add_row(str(i), file, status)
        console.print(table)

        choice = Prompt.ask("[cyan]Enter file number to push (or 'all' for all files, 'q' to cancel)[/cyan]").strip().lower()
        if choice == 'q':
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
                    return
            except ValueError:
                console.print("[red]❌ Invalid input[/red]")
                return

        commit_message = Prompt.ask("[cyan]📝 Enter commit message[/cyan]", default="Update files")
        
        # Enhanced push with retry logic
        success = self.git_ops.enhanced_git_push(files_to_push, commit_message)
        if not success:
            console.print("[yellow]⚠️ Push failed. Trying alternative methods...[/yellow]")
            self.git_ops.troubleshoot_and_retry(files_to_push, commit_message)
        
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
                choice = Prompt.ask("[cyan]🎯 Enter your choice (1-9)[/cyan]").strip()
                
                if choice == '1':
                    self.create_directory_and_file()
                elif choice == '2':
                    self.git_push()
                elif choice == '3':
                    self.list_directory()
                elif choice == '4':
                    self.show_files_and_options()
                elif choice == '5':
                    self.choose_directory_to_create()
                elif choice == '6':
                    self.show_directory_and_options()
                elif choice == '7':
                    self.create_nested_structure()
                elif choice == '8':
                    self.enhanced_git_push()
                elif choice == '9':
                    console.print(Panel("[bold green]👋 Goodbye! Thanks for using DSA Commiter CLI![/bold green]", border_style="green"))
                    break
                else:
                    console.print("[red]❌ Invalid choice. Please enter 1-9.[/red]")
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