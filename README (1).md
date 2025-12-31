# GitHub Automation Python Tools

Complete suite of Python applications for automating GitHub operations.

## Overview

4 independent applications for GitHub automation:

| Tool | Purpose | Command |
|------|---------|---------|
| **github_pusher.py** | Automated push | `python github_pusher.py` |
| **github_manager.py** | Interactive menu | `python github_manager.py` |
| **docs_pusher.py** | Build LaTeX & push | `python docs_pusher.py` |
| **github_monitor.py** | Status monitoring | `python github_monitor.py` |

## Quick Start

### Requirements
- Python 3.7+
- Git 2.x+
- GitHub personal access token

### Installation (2 minutes)

```bash
# 1. Run setup
python setup.py

# 2. Answer prompts
# - GitHub username
# - GitHub token
# - Repository name
# - Local path

# 3. Activate environment
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 4. Test
python github_monitor.py
```

## Getting GitHub Token

1. Visit: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select "repo" scope
4. Copy and paste in setup.py prompt

## Applications

### github_pusher.py
**Automated push** - One command pushes changes to GitHub

```bash
python github_pusher.py
```

Features:
- Auto file staging
- Pattern matching
- Tag creation
- Customizable commit messages

### github_manager.py
**Interactive menu** - Menu-driven repository management

```bash
python github_manager.py
```

Features:
- 11 menu options
- View status & history
- Create branches & tags
- Complete workflow automation

### docs_pusher.py
**Build and push** - Compile LaTeX to PDF and push

```bash
python docs_pusher.py
```

Requires pdflatex:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base

# macOS
brew install --cask mactex

# Windows
# Download from: https://miktex.org
```

### github_monitor.py
**Monitor status** - Check repository status

```bash
python github_monitor.py
```

Features:
- Detailed status report
- Commit history
- Branch information
- JSON/text export

## Configuration

### .env File

Created by setup.py. Contains:

```env
GITHUB_USERNAME=your_username
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_REPO=your_repo
LOCAL_REPO_PATH=./your_repo
COMMIT_MESSAGE=Update documentation
```

### Important

- ❌ **NEVER commit .env to Git**
- ✅ Already in .gitignore
- ✅ Protect your token
- ⚠️ Rotate token quarterly

## Customization

Edit `main()` functions in each script:

```python
def main():
    pusher = GitHubPusher()
    pusher.run_workflow(
        files=['*.py', '*.md'],           # Change file patterns
        commit_msg="Custom message"        # Change message
    )
```

## File Structure

```
github-automation/
├── github_pusher.py         (340 lines)
├── github_manager.py        (380 lines)
├── docs_pusher.py           (290 lines)
├── github_monitor.py        (320 lines)
├── setup.py                 (220 lines)
├── requirements.txt
├── .gitignore
├── .env.example
├── README.md
└── QUICKSTART.txt
```

## Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Missing environment variables"
```bash
rm .env
python setup.py
```

### "pdflatex not found"
Install TeX Live (macOS/Linux/Windows)

### "Permission denied"
```bash
chmod +x github_*.py setup.py
```

## Features

✅ **Production-ready** - Fully error-handled
✅ **Automated setup** - Zero configuration
✅ **Independent tools** - Use separately or together
✅ **Security** - Token protection built-in
✅ **Customizable** - Edit for your workflow
✅ **Well-documented** - Complete docstrings

## Security Best Practices

- ✅ Use personal access token (not password)
- ✅ Select "repo" scope only
- ✅ Never share .env file
- ✅ Rotate token quarterly
- ✅ Use in private repositories first
- ✅ Monitor .env permissions (600)

## Workflow Example

```bash
# 1. Check status
python github_monitor.py

# 2. Make changes locally

# 3. Push changes
python github_pusher.py

# 4. Or use interactive menu
python github_manager.py
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (check output) |
| 2 | Git error |

## Support

- See docstrings in Python files
- Check error messages in output
- Verify .env configuration
- Ensure Git is installed
- Check internet connection

## License

MIT License - Use freely

## Author

GitHub Automation Tools v1.0
Created: December 2024

## Changelog

### v1.0
- Initial release
- 4 tools
- Automated setup
- Full documentation

---

**Ready to automate your GitHub workflow?** 🚀

```bash
python setup.py
```
