#!/usr/bin/env python3
"""Setup Script for GitHub Automation Tools"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_python():
    """Check Python version."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        print(f"   You have: Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def check_git():
    """Check if Git is installed."""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ Git not found. Install Git first.")
        return False

def create_venv():
    """Create virtual environment."""
    venv_path = Path('venv')
    if venv_path.exists():
        print("✓ Virtual environment exists")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
        print("✓ Virtual environment created")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def install_deps():
    """Install Python dependencies."""
    print("\nInstalling dependencies...")
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        if sys.platform == 'win32':
            pip_path = Path('venv/Scripts/pip')
        else:
            pip_path = Path('venv/bin/pip')
        
        if not pip_path.exists():
            print("❌ pip not found in venv")
            return False
        
        print("   Installing packages...")
        result = subprocess.run(
            [str(pip_path), 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Dependencies installed")
            return True
        else:
            print(f"❌ Installation failed:\n{result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def create_env_file():
    """Create .env configuration file."""
    env_file = Path('.env')
    if env_file.exists():
        print("✓ .env file exists")
        overwrite = input("  Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            return True
    
    print("\n" + "="*70)
    print("GITHUB CONFIGURATION")
    print("="*70 + "\n")
    print("Enter your GitHub credentials:")
    print("(Get token at: https://github.com/settings/tokens)\n")
    
    username = input("1. GitHub username: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return False
    
    token = input("2. GitHub token (personal access token): ").strip()
    if not token:
        print("❌ Token cannot be empty")
        return False
    
    repo = input("3. Repository name: ").strip()
    if not repo:
        repo = "technical-docs"
        print(f"   Using default: {repo}")
    
    local_path = input("4. Local repository path: ").strip()
    if not local_path:
        local_path = f"./{repo}"
        print(f"   Using default: {local_path}")
    
    content = f"""# GitHub Automation Configuration
# Created by setup.py

# REQUIRED - GitHub credentials
GITHUB_USERNAME={username}
GITHUB_TOKEN={token}
GITHUB_REPO={repo}
LOCAL_REPO_PATH={local_path}

# OPTIONAL
COMMIT_MESSAGE=Update documentation

# ============================================
# SECURITY WARNING:
# This file contains your GitHub token!
# NEVER commit this to version control!
# It is already in .gitignore
# ============================================
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(content)
        
        # Set permissions (Unix only)
        if sys.platform != 'win32':
            os.chmod('.env', 0o600)
        
        print("\n✓ .env file created")
        return True
    
    except Exception as e:
        print(f"❌ ERROR creating .env: {e}")
        return False

def verify_installation():
    """Verify all dependencies are installed."""
    print("\nVerifying installation...")
    
    required_modules = ['git', 'dotenv']
    
    if sys.platform == 'win32':
        python_path = Path('venv/Scripts/python')
    else:
        python_path = Path('venv/bin/python')
    
    try:
        for module in required_modules:
            result = subprocess.run(
                [str(python_path), '-c', f'import {module}'],
                capture_output=True
            )
            if result.returncode == 0:
                print(f"  ✓ {module}")
            else:
                print(f"  ❌ {module} not found")
                return False
        
        print("✓ All dependencies verified")
        return True
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def print_next_steps():
    """Print next steps instructions."""
    print("\n" + "="*70)
    print("SETUP COMPLETE!")
    print("="*70 + "\n")
    
    print("📚 NEXT STEPS:\n")
    
    if sys.platform == 'win32':
        print("1. Activate virtual environment:")
        print("   venv\\Scripts\\activate\n")
    else:
        print("1. Activate virtual environment:")
        print("   source venv/bin/activate\n")
    
    print("2. Test the tools:")
    print("   python github_monitor.py\n")
    
    print("3. Use the tools:")
    print("   - python github_monitor.py    (Check status)")
    print("   - python github_manager.py    (Interactive menu)")
    print("   - python github_pusher.py     (Auto push)")
    print("   - python docs_pusher.py       (Build LaTeX)\n")
    
    print("📖 See README.md for detailed documentation\n")

def main():
    """Main setup flow."""
    print_header("GitHub Automation Tools - Setup")
    
    print("\n1️⃣  Checking requirements...")
    check_python()
    if not check_git():
        sys.exit(1)
    
    print("\n2️⃣  Setting up environment...")
    if not create_venv():
        sys.exit(1)
    
    print("\n3️⃣  Installing dependencies...")
    if not install_deps():
        print("⚠️  Some packages may not have installed")
    
    print("\n4️⃣  Configuring credentials...")
    if not create_env_file():
        sys.exit(1)
    
    print("\n5️⃣  Verifying installation...")
    if not verify_installation():
        print("⚠️  Some verification issues - may still work")
    
    print_next_steps()

if __name__ == "__main__":
    main()
