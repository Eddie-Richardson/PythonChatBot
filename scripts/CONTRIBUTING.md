# 🤝 Contributing to Admin Scripts Toolkit

Thanks for your interest in improving the Admin Scripts Toolkit!  
This guide explains how to set up your environment, follow our coding style, and add new commands or scripts.

---

## 🛠 Local Setup

1. **Fork & Clone**
   ```bash
   git clone <your-fork-url>
   cd admin-scripts-toolkit
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install argcomplete
   ```

4. **(Optional) Enable Tab Completion**
   ```bash
   activate-global-python-argcomplete
   ```

---

## 📂 Project Structure

```
scripts/                # Standalone maintenance scripts
cli/                    # Unified CLI package
  ├── __init__.py
  ├── main.py            # Parser + dispatch
  ├── commands.py        # cmd_* implementations
  ├── completers.py      # Tab-completion helpers
  └── utils.py           # Shared helpers (color, emoji, error printing)
```

---

## 🧠 Adding a New CLI Command

1. **Create the Command Function** in `cli/commands.py`:
   ```python
   def cmd_newfeature(args):
       """
       Describe what this command does.

       Examples:
         cli newfeature arg1 arg2
       """
       # Your logic here
   ```

2. **Define Arguments** in `cli/main.py`:
   ```python
   def setup_newfeature_args(p):
       p.add_argument("arg1")
       p.add_argument("arg2")
   ```

3. **Register the Command** in `build_parser()`:
   ```python
   add_command(subparsers, "newfeature", cmd_newfeature, setup_newfeature_args)
   ```

4. **Test It**:
   ```bash
   python scripts/cli.py newfeature --examples
   python scripts/cli.py newfeature --run-example 1
   ```

---

## 🎨 Output & Style Guidelines

- Use `success()`, `warning()`, `error()`, and `info()` from `utils.py` for consistent output.
- Keep docstrings **clear and concise** — they power `--help`, `--examples`, and `--run-example`.
- Follow existing naming conventions (`cmd_*` for commands, `setup_*_args` for arg parsers).

---

## ✅ Pull Request Checklist

Before opening a PR:
- [ ] Code runs without errors
- [ ] New commands have docstrings with at least one example
- [ ] README.md updated if usage changes
- [ ] No hard‑coded secrets or credentials
- [ ] Code passes linting/formatting checks

---

## 💬 Communication

- Use clear commit messages (`feat:`, `fix:`, `docs:`, etc.).
- Keep PRs focused — one feature or fix per PR.
- If unsure about an approach, open a draft PR or start a discussion.

---

Happy coding! 🚀
