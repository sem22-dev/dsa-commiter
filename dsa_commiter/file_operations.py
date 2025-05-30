#!/usr/bin/env python3
"""
File Operations for dsa-commiter
Handles file and directory creation with template support.
"""
import os
import shutil
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich.panel import Panel

console = Console()

class FileOperations:
    """Handles file and directory creation operations."""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.default_contents = {
            'js': "console.log('Hello World!');",
            'py': "print('Hello World!')",
            'go': 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello World!")\n}',
            'java': 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello World!");\n    }\n}',
            'cpp': '#include <iostream>\n\nint main() {\n    std::cout << "Hello World!" << std::endl;\n    return 0;\n}',
            'c': '#include <stdio.h>\n\nint main() {\n    printf("Hello World!\\n");\n    return 0;\n}',
            'html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>Hello</title>\n</head>\n<body>\n    <h1>Hello World!</h1>\n</body>\n</html>',
            'css': 'body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n}',
            'md': '# Hello World\n\nThis is a markdown file.',
            'txt': 'Hello World!\n\nThis is a text file.',
            'json': '{\n    "message": "Hello World!",\n    "status": "success"\n}',
            'xml': '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n    <message>Hello World!</message>\n</root>',
            'yml': 'message: Hello World!\nstatus: success\n',
            'yaml': 'message: Hello World!\nstatus: success\n'
        }

    def create_directory_and_file(self, dir_name, filename, content=None):
        """Create a directory (if specified) and a file with given or default content."""
        dir_path = os.path.join(self.current_dir, dir_name) if dir_name else self.current_dir
        
        if dir_name:
            try:
                os.makedirs(dir_path, exist_ok=True)
                console.print(f"[green]✅ Created directory: {dir_path}[/green]")
            except Exception as e:
                console.print(f"[red]❌ Error creating directory: {e}[/red]")
                return False
        
        if not filename:
            if dir_name:  # If only directory was created
                return True
            console.print("[red]❌ File name cannot be empty[/red]")
            return False
        
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        default_content = self.default_contents.get(extension, "Hello World!")
        file_content = content or default_content
        file_path = os.path.join(dir_path, filename)
        
        try:
            with open(file_path, 'w') as file:
                file.write(file_content)
            console.print(f"[green]✅ Created file: {os.path.abspath(file_path)}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error creating file: {e}[/red]")
            return False

    def create_file_in_directory(self, directory, filename, content=None):
        """Create a file inside a specific directory."""
        if not filename:
            console.print("[red]❌ File name cannot be empty[/red]")
            return False
        
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        default_content = self.default_contents.get(extension, "Hello World!")
        file_content = content or default_content
        
        dir_path = os.path.join(self.current_dir, directory)
        file_path = os.path.join(dir_path, filename)
        
        try:
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(file_content)
            console.print(f"[green]✅ Created file: {os.path.abspath(file_path)}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error creating file: {e}[/red]")
            return False

    def list_directory_contents(self):
        """List files and directories in the current directory."""
        try:
            items = os.listdir(self.current_dir)
            files = [f for f in items if os.path.isfile(os.path.join(self.current_dir, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(self.current_dir, d))]
            return files, dirs
        except Exception as e:
            console.print(f"[red]❌ Error listing directory: {e}[/red]")
            return [], []

    def delete_item(self, item_name, item_type):
        """Delete a file or directory."""
        item_path = os.path.join(self.current_dir, item_name)
        
        try:
            if item_type == "file":
                if os.path.isfile(item_path):
                    from rich.prompt import Confirm
                    if Confirm.ask(f"[red]Are you sure you want to delete file '{item_name}'?[/red]"):
                        os.remove(item_path)
                        console.print(f"[green]✅ Deleted file: {item_name}[/green]")
                    else:
                        console.print("[yellow]⚠️ File deletion cancelled[/yellow]")
                else:
                    console.print(f"[red]❌ File '{item_name}' not found[/red]")
            elif item_type == "directory":
                if os.path.isdir(item_path):
                    from rich.prompt import Confirm
                    if Confirm.ask(f"[red]Are you sure you want to delete directory '{item_name}' and all its contents?[/red]"):
                        shutil.rmtree(item_path)
                        console.print(f"[green]✅ Deleted directory: {item_name}[/green]")
                    else:
                        console.print("[yellow]⚠️ Directory deletion cancelled[/yellow]")
                else:
                    console.print(f"[red]❌ Directory '{item_name}' not found[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error deleting {item_type}: {e}[/red]")

    def rename_item(self, item_name, item_type):
        """Rename a file or directory."""
        from rich.prompt import Prompt
        
        item_path = os.path.join(self.current_dir, item_name)
        
        try:
            if (item_type == "file" and os.path.isfile(item_path)) or \
               (item_type == "directory" and os.path.isdir(item_path)):
                
                new_name = Prompt.ask(f"[cyan]Enter new name for {item_type} '{item_name}'[/cyan]").strip()
                if not new_name:
                    console.print("[red]❌ New name cannot be empty[/red]")
                    return
                
                new_path = os.path.join(self.current_dir, new_name)
                if os.path.exists(new_path):
                    console.print(f"[red]❌ {item_type.capitalize()} '{new_name}' already exists[/red]")
                    return
                
                os.rename(item_path, new_path)
                console.print(f"[green]✅ Renamed {item_type} '{item_name}' to '{new_name}'[/green]")
            else:
                console.print(f"[red]❌ {item_type.capitalize()} '{item_name}' not found[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error renaming {item_type}: {e}[/red]")

    def change_directory(self, dir_name):
        """Change to a specified directory."""
        new_path = os.path.join(self.current_dir, dir_name)
        
        try:
            if os.path.isdir(new_path):
                self.current_dir = os.path.abspath(new_path)
                console.print(f"[green]✅ Changed to directory: {self.current_dir}[/green]")
            else:
                console.print(f"[red]❌ Directory '{dir_name}' not found[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error changing directory: {e}[/red]")

    def go_to_parent_directory(self):
        """Go to the parent directory."""
        parent_dir = os.path.dirname(self.current_dir)
        if parent_dir != self.current_dir:  # Not at root
            self.current_dir = parent_dir
            console.print(f"[green]✅ Changed to parent directory: {self.current_dir}[/green]")
        else:
            console.print("[yellow]⚠️ Already at root directory[/yellow]")

    def display_directory_tree(self, max_depth=3):
        """Display directory structure as a tree."""
        def add_to_tree(tree_node, path, current_depth=0):
            if current_depth >= max_depth:
                return
            
            try:
                items = os.listdir(path)
                dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]
                files = [f for f in items if os.path.isfile(os.path.join(path, f))]
                
                # Add directories first
                for dir_name in sorted(dirs):
                    dir_path = os.path.join(path, dir_name)
                    dir_node = tree_node.add(f"📁 [bold blue]{dir_name}[/bold blue]")
                    add_to_tree(dir_node, dir_path, current_depth + 1)
                
                # Add files
                for file_name in sorted(files):
                    file_path = os.path.join(path, file_name)
                    file_size = os.path.getsize(file_path)
                    tree_node.add(f"📄 [white]{file_name}[/white] [dim]({file_size} bytes)[/dim]")
                    
            except PermissionError:
                tree_node.add("[red]❌ Permission denied[/red]")

        tree = Tree(f"📁 [bold cyan]{os.path.basename(self.current_dir) or self.current_dir}[/bold cyan]")
        add_to_tree(tree, self.current_dir)
        console.print(tree)

    def show_directory_statistics(self):
        """Show statistics about the current directory."""
        try:
            files, dirs = self.list_directory_contents()
            
            total_files = len(files)
            total_dirs = len(dirs)
            total_size = 0
            file_types = {}
            
            for file in files:
                file_path = os.path.join(self.current_dir, file)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                
                extension = file.split('.')[-1].lower() if '.' in file else 'no extension'
                file_types[extension] = file_types.get(extension, 0) + 1
            
            # Create statistics table
            table = Table(title=f"Directory Statistics: {os.path.basename(self.current_dir)}")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("📁 Total Directories", str(total_dirs))
            table.add_row("📄 Total Files", str(total_files))
            table.add_row("💾 Total Size", f"{total_size} bytes ({total_size/1024:.2f} KB)")
            table.add_row("📍 Current Path", self.current_dir)
            
            console.print(table)
            
            if file_types:
                console.print("\n[cyan]📊 File Types Distribution:[/cyan]")
                type_table = Table()
                type_table.add_column("Extension", style="yellow")
                type_table.add_column("Count", style="green")
                
                for ext, count in sorted(file_types.items()):
                    type_table.add_row(f".{ext}" if ext != 'no extension' else ext, str(count))
                
                console.print(type_table)
                
        except Exception as e:
            console.print(f"[red]❌ Error calculating statistics: {e}[/red]")

    def search_files(self, pattern="", extension=""):
        """Search for files by pattern or extension."""
        try:
            matching_files = []
            
            for root, dirs, files in os.walk(self.current_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.current_dir)
                    
                    # Check pattern match
                    pattern_match = not pattern or pattern.lower() in file.lower()
                    
                    # Check extension match
                    file_ext = file.split('.')[-1].lower() if '.' in file else ''
                    ext_match = not extension or file_ext == extension.lower()
                    
                    if pattern_match and ext_match:
                        matching_files.append((relative_path, os.path.getsize(file_path)))
            
            if matching_files:
                table = Table(title=f"Search Results (Pattern: '{pattern}', Extension: '{extension}')")
                table.add_column("File Path", style="white")
                table.add_column("Size", style="yellow")
                
                for file_path, size in matching_files:
                    table.add_row(file_path, f"{size} bytes")
                
                console.print(table)
            else:
                console.print("[yellow]⚠️ No matching files found[/yellow]")
                
        except Exception as e:
            console.print(f"[red]❌ Error searching files: {e}[/red]")

    def create_multiple_files(self, file_list):
        """Create multiple files at once."""
        success_count = 0
        
        for file_info in file_list:
            if isinstance(file_info, str):
                # Simple filename
                filename = file_info
                content = None
            elif isinstance(file_info, tuple) and len(file_info) == 2:
                # (filename, content) tuple
                filename, content = file_info
            else:
                console.print(f"[red]❌ Invalid file info: {file_info}[/red]")
                continue
            
            if self.create_directory_and_file("", filename, content):
                success_count += 1
        
        console.print(f"[green]✅ Successfully created {success_count} out of {len(file_list)} files[/green]")

    def backup_directory(self, backup_name=""):
        """Create a backup of the current directory."""
        try:
            if not backup_name:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{os.path.basename(self.current_dir)}_{timestamp}"
            
            backup_path = os.path.join(os.path.dirname(self.current_dir), backup_name)
            shutil.copytree(self.current_dir, backup_path)
            console.print(f"[green]✅ Backup created: {backup_path}[/green]")
            return backup_path
        except Exception as e:
            console.print(f"[red]❌ Error creating backup: {e}[/red]")
            return None

    def get_file_info(self, filename):
        """Get detailed information about a file."""
        file_path = os.path.join(self.current_dir, filename)
        
        try:
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                import datetime
                
                info_table = Table(title=f"File Information: {filename}")
                info_table.add_column("Property", style="cyan")
                info_table.add_column("Value", style="white")
                
                info_table.add_row("📄 Name", filename)
                info_table.add_row("📍 Full Path", os.path.abspath(file_path))
                info_table.add_row("💾 Size", f"{stat.st_size} bytes ({stat.st_size/1024:.2f} KB)")
                info_table.add_row("📅 Created", datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"))
                info_table.add_row("✏️ Modified", datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
                info_table.add_row("👁️ Accessed", datetime.datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S"))
                
                # File extension and type
                extension = filename.split('.')[-1].lower() if '.' in filename else 'no extension'
                info_table.add_row("🏷️ Extension", extension)
                
                console.print(info_table)
            else:
                console.print(f"[red]❌ File '{filename}' not found[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error getting file info: {e}[/red]")