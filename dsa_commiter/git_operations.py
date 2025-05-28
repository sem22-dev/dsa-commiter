
#!/usr/bin/env python3
"""
Git Operations for dsa-commiter
Handles Git add, commit, and push operations.
"""

import os
import subprocess
from rich.console import Console

console = Console()

class GitOperations:
    """Handles Git-related operations."""
    
    def __init__(self):
        self.current_dir = os.getcwd()

    def is_git_repository(self):
        """Check if the current directory is a Git repository."""
        return os.path.exists(os.path.join(self.current_dir, '.git'))

    def initialize_git(self):
        """Initialize a Git repository in the current directory."""
        try:
            subprocess.run(['git', 'init'], cwd=self.current_dir, check=True, capture_output=True)
            console.print("[green]✅ Git repository initialized[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Error initializing Git: {e.stderr.decode()}[/red]")
            return False

    def git_add_commit_push(self, files, commit_message="Update files"):
        """Perform Git add, commit, and push for specified files."""
        try:
            # Git add
            for file in files:
                subprocess.run(['git', 'add', file], cwd=self.current_dir, check=True, capture_output=True)
            
            # Git commit
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.current_dir, check=True, capture_output=True)
            
            # Git push
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.current_dir, check=True, capture_output=True)
            console.print(f"[green]✅ Successfully pushed {', '.join(files)}[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Git operation failed: {e.stderr.decode()}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            return False