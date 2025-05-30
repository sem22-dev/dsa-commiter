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
            'py': "print('Hello World!')",
            'js': "console.log('Hello World!');",
            'cpp': '#include <iostream>\n\nint main() {\n    std::cout << "Hello World!" << std::endl;\n    return 0;\n}',
            'java': 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello World!");\n    }\n}',
            'c': '#include <stdio.h>\n\nint main() {\n    printf("Hello World!\\n");\n    return 0;\n}',
            'txt': 'Hello World!'
        }

    def create_directory_and_file(self, dir_path, filename, content=None):
        """Create a directory path (if specified) and a file with given or default content."""
        dir_full_path = os.path.join(self.current_dir, dir_path) if dir_path else self.current_dir
        
        # Validate filename
        if not filename:
            console.print("[red]❌ File name cannot be empty[/red]")
            return False
        invalid_chars = '<>:"\\|?*'
        if any(char in filename for char in invalid_chars):
            console.print(f"[red]❌ Invalid characters in filename: {invalid_chars}[/red]")
            return False
        if len(filename) > 255:  # Typical filename length limit
            console.print("[red]❌ Filename too long (max 255 characters)[/red]")
            return False
        
        # Create directory path if specified
        if dir_path:
            try:
                os.makedirs(dir_full_path, exist_ok=True)
                console.print(f"[green]✅ Created or using directory: {dir_full_path}[/green]")
            except Exception as e:
                console.print(f"[red]❌ Error creating directory: {e}[/red]")
                return False
        
        # Create file
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        default_content = self.default_contents.get(extension, "Hello World!")
        file_content = content or default_content
        file_path = os.path.join(dir_full_path, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
            console.print(f"[green]✅ Created file: {os.path.abspath(file_path)}[/green]")
            return True
        except (UnicodeEncodeError, PermissionError, OSError) as e:
            console.print(f"[red]❌ Error creating file: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]❌ Unexpected error creating file: {e}[/red]")
            return False