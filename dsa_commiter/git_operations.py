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

    def get_current_branch(self):
        """Get the name of the current Git branch."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.current_dir,
                check=True,
                capture_output=True,
                text=True
            )
            branch = result.stdout.strip()
            if branch:
                return branch
            console.print("[yellow]⚠️ No current branch detected (possibly in detached HEAD state)[/yellow]")
            return None
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            console.print(f"[red]❌ Failed to detect current branch: {error_msg}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]❌ Unexpected error detecting branch: {e}[/red]")
            return None

    def auto_commit_and_push(self, filename):
        """Automatically add, commit, and push the specified file."""
        try:
            # Check if it's a Git repository
            if not self.is_git_repository():
                console.print("[red]❌ Not a Git repository. Please initialize with 'git init'.[/red]")
                return False
            
            # Get the current branch
            branch = self.get_current_branch()
            if not branch:
                console.print("[red]❌ Cannot proceed without a valid branch.[/red]")
                console.print("[yellow]💡 Tip: Create a branch with 'git checkout -b main' or 'git checkout -b master'[/yellow]")
                return False
            
            # Git add
            subprocess.run(['git', 'add', filename], cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print(f"[green]✅ Added file: {filename}[/green]")
            
            # Git commit
            commit_message = f"{filename} solution"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print(f"[green]✅ Committed with message: '{commit_message}'[/green]")
            
            # Git push
            subprocess.run(['git', 'push', 'origin', branch], cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print(f"[green]✅ Pushed file: {filename} to branch '{branch}'[/green]")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            console.print(f"[red]❌ Git operation failed: {error_msg}[/red]")
            console.print("[yellow]💡 Tips:[/yellow]")
            console.print("- Ensure remote 'origin' is set with 'git remote add origin <url>'")
            console.print(f"- Verify branch '{branch}' exists on the remote repository")
            console.print("- Check network connection and repository permissions")
            return False
        except Exception as e:
            console.print(f"[red]❌ Unexpected error during Git operation: {e}[/red]")
            return False