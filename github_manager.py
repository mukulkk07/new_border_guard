#!/usr/bin/env python3
"""GitHub Manager - Interactive Menu-Driven GitHub Operations"""

import os
from pathlib import Path
from dotenv import load_dotenv
from git import Repo, GitCommandError
import sys

load_dotenv()

class GitHubManager:
    """Interactive GitHub repository manager."""
    
    def __init__(self):
        self.username = os.getenv('GITHUB_USERNAME')
        self.local_path = os.getenv('LOCAL_REPO_PATH')
        self.repo = None
        self.running = True
    
    def setup_repo(self):
        try:
            if Path(self.local_path).exists():
                self.repo = Repo(self.local_path)
                print(f"✓ Connected to {self.local_path}")
                return True
            else:
                print(f"ERROR: Repository not found")
                return False
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    def display_menu(self):
        print("\n" + "="*60)
        print("GitHub Repository Manager")
        print("="*60)
        print("\n1. View Status")
        print("2. View History")
        print("3. Add Files")
        print("4. Commit")
        print("5. Push")
        print("6. Pull")
        print("7. Create Branch")
        print("8. Switch Branch")
        print("9. Create Tag")
        print("10. List Branches")
        print("11. Complete Workflow")
        print("0. Exit")
    
    def view_status(self):
        print("\n--- Status ---")
        try:
            print(f"Branch: {self.repo.active_branch.name}")
            print(f"Dirty: {self.repo.is_dirty()}")
            print(f"Untracked: {len(self.repo.untracked_files)}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def view_history(self):
        print("\n--- Commit History ---")
        try:
            commits = list(self.repo.iter_commits('HEAD', max_count=5))
            for i, commit in enumerate(commits, 1):
                print(f"{i}. {commit.hexsha[:7]} - {commit.message.strip()[:50]}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def add_files(self):
        try:
            self.repo.git.add(A=True)
            print("✓ Files added")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def commit_changes(self):
        msg = input("Commit message: ").strip()
        if not msg:
            print("ERROR: Message cannot be empty")
            return
        try:
            self.repo.index.commit(msg)
            print("✓ Committed")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def push_changes(self):
        try:
            self.repo.remotes.origin.push('main')
            print("✓ Pushed")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def pull_changes(self):
        try:
            self.repo.remotes.origin.pull('main')
            print("✓ Pulled")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def create_branch(self):
        name = input("Branch name: ").strip()
        if not name:
            print("ERROR: Name cannot be empty")
            return
        try:
            self.repo.create_head(name)
            print(f"✓ Branch created: {name}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def switch_branch(self):
        name = input("Branch name: ").strip()
        if not name:
            print("ERROR: Name cannot be empty")
            return
        try:
            self.repo.heads[name].checkout()
            print(f"✓ Switched to {name}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def create_tag(self):
        name = input("Tag name: ").strip()
        if not name:
            print("ERROR: Name cannot be empty")
            return
        try:
            self.repo.create_tag(name)
            print(f"✓ Tag created: {name}")
            push = input("Push tag? (y/n): ").strip().lower()
            if push == 'y':
                self.repo.remotes.origin.push(name)
                print("✓ Tag pushed")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def list_branches(self):
        print("\n--- Branches ---")
        try:
            for head in self.repo.heads:
                current = " (current)" if head == self.repo.active_branch else ""
                print(f"  {head.name}{current}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def complete_workflow(self):
        print("\n--- Complete Workflow ---")
        msg = input("Commit message: ").strip()
        if not msg:
            print("ERROR: Message cannot be empty")
            return
        
        try:
            print("\n1. Adding files...")
            self.repo.git.add(A=True)
            print("   ✓ Added")
            
            print("2. Committing...")
            self.repo.index.commit(msg)
            print("   ✓ Committed")
            
            print("3. Pushing...")
            self.repo.remotes.origin.push('main')
            print("   ✓ Pushed")
            
            print("\n✓ Workflow complete!")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def run(self):
        if not self.setup_repo():
            return
        
        while self.running:
            self.display_menu()
            choice = input("Option: ").strip()
            
            if choice == '1':
                self.view_status()
            elif choice == '2':
                self.view_history()
            elif choice == '3':
                self.add_files()
            elif choice == '4':
                self.commit_changes()
            elif choice == '5':
                self.push_changes()
            elif choice == '6':
                self.pull_changes()
            elif choice == '7':
                self.create_branch()
            elif choice == '8':
                self.switch_branch()
            elif choice == '9':
                self.create_tag()
            elif choice == '10':
                self.list_branches()
            elif choice == '11':
                self.complete_workflow()
            elif choice == '0':
                self.running = False
            else:
                print("ERROR: Invalid option")
            
            if choice != '0':
                input("Press Enter to continue...")

def main():
    manager = GitHubManager()
    manager.run()

if __name__ == "__main__":
    main()
