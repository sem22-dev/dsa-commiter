#!/usr/bin/env python3
"""
File Operations for dsa-commiter
Handles file and directory creation with template support.
"""

import os
from rich.console import Console

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
            'html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>Hello</title>\n</head>\n<body>\n    <h1>Hello World!</h1>\n</body>\n</html>',
            'css': 'body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n}',
            'md': '# Hello World\n\nThis is a markdown file.',
            'txt': 'Hello World!\n\nThis is a text file.'
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