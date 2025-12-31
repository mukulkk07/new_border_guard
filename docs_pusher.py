#!/usr/bin/env python3
"""Docs Pusher - Build LaTeX and Push to GitHub"""

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from git import Repo
import sys

load_dotenv()

class DocumentationPusher:
    """Build and push LaTeX documents."""
    
    def __init__(self):
        self.local_path = os.getenv('LOCAL_REPO_PATH')
        self.docs_dir = Path(self.local_path) / 'docs'
        try:
            self.repo = Repo(self.local_path)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        self.built_files = []
    
    def find_tex_files(self):
        if not self.docs_dir.exists():
            print(f"ERROR: Docs directory not found: {self.docs_dir}")
            return []
        return list(self.docs_dir.rglob('*.tex'))
    
    def build_latex(self, tex_file):
        try:
            print(f"\nBuilding: {tex_file.name}")
            original_dir = os.getcwd()
            os.chdir(tex_file.parent)
            
            for run in range(2):
                print(f"  Run {run+1}/2...")
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_file.name],
                    capture_output=True,
                    timeout=60,
                    text=True
                )
                if result.returncode != 0:
                    print(f"  ✗ Failed")
                    os.chdir(original_dir)
                    return False
            
            aux_extensions = ['.aux', '.log', '.out', '.toc']
            for ext in aux_extensions:
                aux_file = tex_file.with_suffix(ext)
                if aux_file.exists():
                    try:
                        aux_file.unlink()
                    except:
                        pass
            
            os.chdir(original_dir)
            pdf_file = tex_file.with_suffix('.pdf')
            
            if pdf_file.exists():
                size_mb = pdf_file.stat().st_size / (1024*1024)
                print(f"  ✓ Built: {pdf_file.name} ({size_mb:.2f} MB)")
                self.built_files.append(pdf_file)
                return True
            else:
                print(f"  ✗ PDF not created")
                return False
        
        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout")
            os.chdir(original_dir)
            return False
        except FileNotFoundError:
            print(f"  ✗ pdflatex not found. Install TeX Live or MiKTeX")
            os.chdir(original_dir)
            return False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            os.chdir(original_dir)
            return False
    
    def build_all_docs(self):
        print("\n" + "="*60)
        print("=== Building Documentation ===")
        print("="*60 + "\n")
        
        tex_files = self.find_tex_files()
        if not tex_files:
            print("No .tex files found")
            return False
        
        print(f"Found {len(tex_files)} .tex file(s)")
        
        success_count = 0
        for tex_file in tex_files:
            if self.build_latex(tex_file):
                success_count += 1
        
        print(f"\n✓ Built {success_count}/{len(tex_files)} files successfully")
        return success_count == len(tex_files)
    
    def push_to_github(self):
        try:
            print("\n" + "="*60)
            print("=== Pushing to GitHub ===")
            print("="*60 + "\n")
            
            print("Adding PDF files...")
            self.repo.git.add('*.pdf')
            self.repo.git.add('docs/**/*.pdf')
            
            if not self.repo.is_dirty():
                print("No changes to commit")
                return True
            
            message = f"Auto-build: Generated {len(self.built_files)} PDF(s)"
            print(f"Committing: {message}")
            self.repo.index.commit(message)
            
            print("Pushing to remote...")
            self.repo.remotes.origin.push('main')
            
            print("✓ Pushed successfully")
            return True
        
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    def generate_report(self):
        print("\n" + "="*60)
        print("=== Build Report ===")
        print("="*60 + "\n")
        
        if not self.built_files:
            print("No files built")
            return
        
        print(f"Built files ({len(self.built_files)}):")
        total_size = 0
        for pdf_file in self.built_files:
            size_mb = pdf_file.stat().st_size / (1024*1024)
            total_size += size_mb
            print(f"  - {pdf_file.name}")
            print(f"    Size: {size_mb:.2f} MB")
        
        print(f"\nTotal: {total_size:.2f} MB | {len(self.built_files)} files")
    
    def run(self, push_to_remote=True):
        print("Starting Documentation Pipeline...\n")
        
        if not self.build_all_docs():
            print("\n✗ Build failed!")
            return False
        
        self.generate_report()
        
        if push_to_remote and self.built_files:
            if not self.push_to_github():
                return False
        
        print("\n" + "="*60)
        print("✓ Pipeline completed successfully!")
        print("="*60 + "\n")
        return True

def main():
    pusher = DocumentationPusher()
    success = pusher.run(push_to_remote=True)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
