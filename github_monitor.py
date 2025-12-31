#!/usr/bin/env python3
"""GitHub Monitor - Repository Status Monitoring"""

from pathlib import Path
from git import Repo
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import sys

load_dotenv()

class GitHubMonitor:
    """Monitor repository status."""
    
    def __init__(self):
        self.local_path = os.getenv('LOCAL_REPO_PATH')
        if not self.local_path:
            print("ERROR: LOCAL_REPO_PATH not set in .env")
            sys.exit(1)
        
        try:
            self.repo = Repo(self.local_path)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    
    def get_status_summary(self):
        """Get comprehensive repository status."""
        try:
            return {
                'timestamp': datetime.now().isoformat(),
                'branch': self.repo.active_branch.name,
                'dirty': self.repo.is_dirty(),
                'untracked_files': len(self.repo.untracked_files),
                'total_commits': sum(1 for _ in self.repo.iter_commits()),
                'last_commit': self.repo.head.commit.message.strip()[:100],
                'last_commit_author': self.repo.head.commit.author.name,
                'remote_url': list(self.repo.remotes.origin.urls)[0] if self.repo.remotes else 'N/A'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_commit_history(self, limit=5):
        """Get recent commit history."""
        commits = []
        try:
            for commit in list(self.repo.iter_commits('HEAD', max_count=limit)):
                commits.append({
                    'hash': commit.hexsha[:7],
                    'date': datetime.fromtimestamp(commit.committed_date).isoformat(),
                    'message': commit.message.strip().split('\n')[0][:60],
                    'author': commit.author.name
                })
        except Exception as e:
            commits.append({'error': str(e)})
        
        return commits
    
    def get_branch_info(self):
        """Get information about all branches."""
        branches = []
        try:
            for head in self.repo.heads:
                current = head == self.repo.active_branch
                branches.append({
                    'name': head.name,
                    'current': current,
                    'commit': head.commit.hexsha[:7]
                })
        except Exception as e:
            branches.append({'error': str(e)})
        
        return branches
    
    def get_file_changes(self):
        """Get changed files."""
        changed = []
        try:
            if self.repo.is_dirty():
                for item in self.repo.untracked_files[:10]:
                    changed.append(f"  ? {item}")
                
                diff_index = self.repo.index.diff('HEAD')
                for diff in diff_index[:10]:
                    changed.append(f"  M {diff.a_path}")
        except Exception as e:
            changed.append(f"ERROR: {e}")
        
        return changed
    
    def print_status(self):
        """Print detailed status report."""
        status = self.get_status_summary()
        
        print("\n" + "="*70)
        print("GITHUB REPOSITORY MONITOR")
        print("="*70)
        
        print(f"\n📍 REPOSITORY INFO:")
        print(f"  Path: {self.local_path}")
        print(f"  Remote: {status.get('remote_url', 'N/A')}")
        print(f"  Timestamp: {status.get('timestamp', 'N/A')}")
        
        print(f"\n🔀 BRANCH INFO:")
        print(f"  Current Branch: {status.get('branch', 'N/A')}")
        print(f"  Total Commits: {status.get('total_commits', 0)}")
        print(f"  Status: {'🔴 Dirty (has changes)' if status.get('dirty') else '🟢 Clean'}")
        print(f"  Untracked Files: {status.get('untracked_files', 0)}")
        
        print(f"\n📝 LAST COMMIT:")
        print(f"  Author: {status.get('last_commit_author', 'N/A')}")
        print(f"  Message: {status.get('last_commit', 'N/A')}")
        
        print(f"\n📂 BRANCHES:")
        branches = self.get_branch_info()
        for branch in branches:
            marker = "▶ " if branch.get('current') else "  "
            print(f"  {marker}{branch.get('name', 'N/A')} ({branch.get('commit', 'N/A')})")
        
        print(f"\n📜 RECENT COMMITS:")
        commits = self.get_commit_history(5)
        for i, commit in enumerate(commits, 1):
            if 'error' not in commit:
                print(f"  {i}. {commit['hash']} - {commit['message']}")
                print(f"     {commit['author']} ({commit['date'][:10]})")
        
        changes = self.get_file_changes()
        if changes:
            print(f"\n📄 CHANGED FILES:")
            for change in changes:
                print(change)
        
        print("\n" + "="*70 + "\n")
    
    def export_json(self, filename='repo_status.json'):
        """Export status to JSON file."""
        try:
            data = {
                'summary': self.get_status_summary(),
                'history': self.get_commit_history(10),
                'branches': self.get_branch_info()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✓ Exported to {filename}")
            return True
        except Exception as e:
            print(f"ERROR exporting: {e}")
            return False
    
    def export_text(self, filename='repo_status.txt'):
        """Export status to text file."""
        try:
            with open(filename, 'w') as f:
                status = self.get_status_summary()
                f.write("GITHUB REPOSITORY STATUS\n")
                f.write("=" * 70 + "\n\n")
                
                f.write("SUMMARY:\n")
                for key, value in status.items():
                    f.write(f"  {key}: {value}\n")
                
                f.write("\n\nRECENT COMMITS:\n")
                for commit in self.get_commit_history(10):
                    f.write(f"  {commit['hash']} - {commit['message']}\n")
            
            print(f"✓ Exported to {filename}")
            return True
        except Exception as e:
            print(f"ERROR exporting: {e}")
            return False

def main():
    """Main entry point."""
    monitor = GitHubMonitor()
    monitor.print_status()
    
    export_json = input("Export to JSON? (y/n): ").strip().lower()
    if export_json == 'y':
        monitor.export_json()
    
    export_text = input("Export to text? (y/n): ").strip().lower()
    if export_text == 'y':
        monitor.export_text()

if __name__ == "__main__":
    main()
