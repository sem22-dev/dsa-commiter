#!/usr/bin/env python3
"""
Git Operations for dsa-commiter
Handles Git add, commit, and push operations with enhanced error handling.
"""
import os
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class GitOperations:
    """Handles Git-related operations with enhanced functionality."""
    
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
            
            # Set default branch to main if not already set
            try:
                subprocess.run(['git', 'branch', '-M', 'main'], cwd=self.current_dir, check=True, capture_output=True)
                console.print("[green]✅ Default branch set to 'main'[/green]")
            except subprocess.CalledProcessError:
                pass  # Branch might already exist
            
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Error initializing Git: {e.stderr.decode() if e.stderr else str(e)}[/red]")
            return False

    def git_add_commit_push(self, files, commit_message="Update files"):
        """Perform Git add, commit, and push for specified files."""
        try:
            # Git add
            for file in files:
                result = subprocess.run(['git', 'add', file], cwd=self.current_dir, 
                                      check=True, capture_output=True, text=True)
            console.print(f"[green]✅ Added files: {', '.join(files)}[/green]")
            
            # Git commit
            result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                  cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print(f"[green]✅ Committed with message: '{commit_message}'[/green]")
            
            # Git push
            result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                  cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print(f"[green]✅ Successfully pushed {', '.join(files)}[/green]")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            console.print(f"[red]❌ Git operation failed: {error_msg}[/red]")
            
            # Provide specific error handling
            if "no upstream branch" in error_msg.lower():
                console.print("[yellow]💡 Tip: You may need to set up an upstream branch[/yellow]")
                if Confirm.ask("[cyan]Try setting upstream and push again?[/cyan]"):
                    return self.set_upstream_and_push(files, commit_message)
            elif "no remote" in error_msg.lower():
                console.print("[yellow]💡 Tip: You may need to add a remote repository[/yellow]")
                remote_url = Prompt.ask("[cyan]Enter remote repository URL (or press Enter to skip)[/cyan]").strip()
                if remote_url:
                    if self.add_remote(remote_url):
                        return self.git_add_commit_push(files, commit_message)
            
            return False
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            return False

    def set_upstream_and_push(self, files, commit_message):
        """Set upstream branch and push."""
        try:
            # Try to push with upstream set
            result = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'], 
                                  cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print("[green]✅ Successfully set upstream and pushed[/green]")
            return True
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            console.print(f"[red]❌ Failed to set upstream: {error_msg}[/red]")
            return False

    def add_remote(self, remote_url, remote_name="origin"):
        """Add a remote repository."""
        try:
            # Check if remote already exists
            result = subprocess.run(['git', 'remote', 'get-url', remote_name], 
                                  cwd=self.current_dir, capture_output=True, text=True)
            if result.returncode == 0:
                console.print(f"[yellow]⚠️ Remote '{remote_name}' already exists[/yellow]")
                if Confirm.ask(f"[cyan]Replace existing remote '{remote_name}'?[/cyan]"):
                    subprocess.run(['git', 'remote', 'remove', remote_name], 
                                 cwd=self.current_dir, check=True, capture_output=True)
                else:
                    return False
            
            # Add the remote
            subprocess.run(['git', 'remote', 'add', remote_name, remote_url], 
                         cwd=self.current_dir, check=True, capture_output=True)
            console.print(f"[green]✅ Added remote '{remote_name}': {remote_url}[/green]")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            console.print(f"[red]❌ Error adding remote: {error_msg}[/red]")
            return False

    def run_git_diagnostics(self):
        """Run comprehensive Git diagnostics."""
        diagnostics = {
            'is_git_repo': False,
            'has_remote': False,
            'has_commits': False,
            'current_branch': None,
            'remote_url': None,
            'staged_files': [],
            'modified_files': [],
            'untracked_files': []
        }
        
        try:
            # Check if it's a Git repository
            diagnostics['is_git_repo'] = self.is_git_repository()
            
            if not diagnostics['is_git_repo']:
                return diagnostics
            
            # Get current branch
            try:
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      cwd=self.current_dir, capture_output=True, text=True, check=True)
                diagnostics['current_branch'] = result.stdout.strip()
            except subprocess.CalledProcessError:
                diagnostics['current_branch'] = 'unknown'
            
            # Check for remote
            try:
                result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                      cwd=self.current_dir, capture_output=True, text=True, check=True)
                diagnostics['has_remote'] = True
                diagnostics['remote_url'] = result.stdout.strip()
            except subprocess.CalledProcessError:
                diagnostics['has_remote'] = False
            
            # Check for commits
            try:
                result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                      cwd=self.current_dir, capture_output=True, text=True, check=True)
                diagnostics['has_commits'] = bool(result.stdout.strip())
            except subprocess.CalledProcessError:
                diagnostics['has_commits'] = False
            
            # Get file status
            try:
                result = subprocess.run(['git', 'status', '--porcelain'], 
                                      cwd=self.current_dir, capture_output=True, text=True, check=True)
                
                for line in result.stdout.strip().split('\n'):
                    if line:
                        status = line[:2]
                        filename = line[3:]
                        
                        if status[0] in 'MARC':  # Staged
                            diagnostics['staged_files'].append(filename)
                        if status[1] == 'M':  # Modified
                            diagnostics['modified_files'].append(filename)
                        if status == '??':  # Untracked
                            diagnostics['untracked_files'].append(filename)
                            
            except subprocess.CalledProcessError:
                pass
            
        except Exception as e:
            console.print(f"[red]❌ Error running diagnostics: {e}[/red]")
        
        return diagnostics

    def show_git_status(self):
        """Display comprehensive Git status."""
        try:
            result = subprocess.run(['git', 'status'], cwd=self.current_dir, 
                                  capture_output=True, text=True, check=True)
            
            console.print(Panel(result.stdout, title="[bold cyan]Git Status[/bold cyan]", border_style="blue"))
            
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Error getting Git status: {e.stderr.decode() if e.stderr else str(e)}[/red]")

    def get_file_git_status(self, filename):
        """Get Git status for a specific file."""
        try:
            result = subprocess.run(['git', 'status', '--porcelain', filename], 
                                  cwd=self.current_dir, capture_output=True, text=True, check=True)
            
            if not result.stdout.strip():
                return "✅ Clean"
            
            status_code = result.stdout[:2]
            if status_code == '??':
                return "❓ Untracked"
            elif 'M' in status_code:
                return "📝 Modified"
            elif 'A' in status_code:
                return "➕ Added"
            elif 'D' in status_code:
                return "🗑️  Deleted"
            else:
                return f"📋 {status_code.strip()}"
                
        except subprocess.CalledProcessError:
            return "❓ Unknown"

    def enhanced_git_push(self, files, commit_message):
        """Enhanced Git push with better error handling."""
        try:
            # First, try the standard approach
            return self.git_add_commit_push(files, commit_message)
            
        except Exception as e:
            console.print(f"[yellow]⚠️ Standard push failed: {e}[/yellow]")
            return False

    def troubleshoot_and_retry(self, files, commit_message):
        """Troubleshoot common Git issues and retry."""
        console.print("[cyan]🔧 Running troubleshooting...[/cyan]")
        
        diagnostics = self.run_git_diagnostics()
        issues_found = []
        
        # Check for common issues
        if not diagnostics['has_remote']:
            issues_found.append("No remote repository")
            console.print("[yellow]⚠️ Issue: No remote repository configured[/yellow]")
            remote_url = Prompt.ask("[cyan]Enter remote repository URL[/cyan]").strip()
            if remote_url and self.add_remote(remote_url):
                console.print("[green]✅ Remote added successfully[/green]")
        
        if not diagnostics['has_commits']:
            issues_found.append("No initial commit")
            console.print("[yellow]⚠️ Issue: No commits in repository[/yellow]")
            if Confirm.ask("[cyan]Create initial commit?[/cyan]"):
                try:
                    subprocess.run(['git', 'add', '.'], cwd=self.current_dir, check=True)
                    subprocess.run(['git', 'commit', '-m', 'Initial commit'], 
                                 cwd=self.current_dir, check=True)
                    console.print("[green]✅ Initial commit created[/green]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]❌ Failed to create initial commit: {e}[/red]")
        
        # Try different push strategies
        push_strategies = [
            (['git', 'push', 'origin', 'main'], "Standard push"),
            (['git', 'push', '--set-upstream', 'origin', 'main'], "Push with upstream"),
            (['git', 'push', '-u', 'origin', 'main'], "Push with -u flag"),
            (['git', 'push', 'origin', 'HEAD'], "Push HEAD to origin")
        ]
        
        for strategy, description in push_strategies:
            console.print(f"[cyan]🔄 Trying: {description}[/cyan]")
            try:
                # Add and commit first
                for file in files:
                    subprocess.run(['git', 'add', file], cwd=self.current_dir, check=True)
                
                subprocess.run(['git', 'commit', '-m', commit_message], 
                             cwd=self.current_dir, check=True)
                
                # Try the push strategy
                result = subprocess.run(strategy, cwd=self.current_dir, 
                                      check=True, capture_output=True, text=True)
                
                console.print(f"[green]✅ Success with: {description}[/green]")
                return True
                
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode() if e.stderr else str(e)
                console.print(f"[yellow]⚠️ Failed: {error_msg[:100]}...[/yellow]")
                continue
        
        # If all strategies fail, show final troubleshooting tips
        console.print("\n[red]❌ All push strategies failed. Here are some tips:[/red]")
        console.print("1. Check your network connection")
        console.print("2. Verify your Git credentials")
        console.print("3. Make sure the remote repository exists")
        console.print("4. Check if you have push permissions")
        console.print("5. Try running 'git status' to see current state")
        
        return False

    def show_git_log(self, limit=10):
        """Show Git commit history."""
        try:
            result = subprocess.run(['git', 'log', '--oneline', f'-{limit}'], 
                                  cwd=self.current_dir, capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                console.print(Panel(result.stdout, title="[bold cyan]Recent Commits[/bold cyan]", border_style="blue"))
            else:
                console.print("[yellow]⚠️ No commits found[/yellow]")
                
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠️ Unable to show Git log (repository may be empty)[/yellow]")

    def create_gitignore(self, templates=None):
        """Create a .gitignore file with common patterns."""
        if templates is None:
            templates = ['python', 'node', 'general']
        
        gitignore_patterns = {
            'python': [
                "# Python",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "*.egg-info/",
                "dist/",
                "build/",
                ".env",
                "venv/",
                ".venv/",
                ""
            ],
            'node': [
                "# Node.js",
                "node_modules/",
                "npm-debug.log*",
                "yarn-debug.log*",
                "yarn-error.log*",
                ".env",
                ""
            ],
            'general': [
                "# General",
                ".DS_Store",
                "Thumbs.db",
                "*.log",
                "*.tmp",
                "*.temp",
                ".vscode/",
                ".idea/",
                ""
            ]
        }
        
        try:
            gitignore_path = os.path.join(self.current_dir, '.gitignore')
            
            with open(gitignore_path, 'w') as f:
                f.write("# Generated .gitignore file\n\n")
                for template in templates:
                    if template in gitignore_patterns:
                        f.write('\n'.join(gitignore_patterns[template]) + '\n')
            
            console.print(f"[green]✅ Created .gitignore with templates: {', '.join(templates)}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error creating .gitignore: {e}[/red]")
            return False

    def git_pull(self):
        """Pull changes from remote repository."""
        try:
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  cwd=self.current_dir, check=True, capture_output=True, text=True)
            console.print("[green]✅ Successfully pulled changes[/green]")
            if result.stdout.strip():
                console.print(Panel(result.stdout, title="Pull Output", border_style="green"))
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str