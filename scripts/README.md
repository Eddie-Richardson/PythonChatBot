# 🛠 Admin Scripts Toolkit

This folder contains standalone maintenance and inspection scripts for your AI assistant’s memory system, plus a unified CLI for convenience. You can run individual scripts directly for quick, targeted tasks, or use the CLI as a single entry point for all commands. The CLI provides color‑coded and emoji‑enhanced output for instant visual feedback, which can be disabled with the `--no-color` flag for CI/CD or plain‑text logs. Tab‑completion is supported for commands, workspaces, and user IDs to speed up your workflow.

## 📂 Scripts Overview

| Script | Purpose | Example Usage |
|--------|---------|---------------|
| `view_conversation.py` | View full conversation history (active + archive) for a user, in compact and expanded formats. | `python scripts/view_conversation.py my_workspace user123` |
| `list_workspaces.py` | List all distinct workspaces in the database. | `python scripts/list_workspaces.py` |
| `list_users.py` | List all user IDs in a given workspace. | `python scripts/list_users.py my_workspace` |
| `dump_archive.py` | Export archived messages for a user to a JSON file. | `python scripts/dump_archive.py my_workspace user123` |
| `clear_active_history.py` | Clear active (non‑archived) history for a user. | `python scripts/clear_active_history.py my_workspace user123` |
| `merge_archive_active.py` | Merge active + archived history into a single timestamped `.txt` transcript. | `python scripts/merge_archive_active.py my_workspace user123` |
| **`cli.py`** | Unified command-line interface for all the above scripts, with ✅ success, ⚠️ warning, ❌ error, and 📄 info output. Supports `--no-color`, `--examples`, `--run-example`, and tab‑completion. | See usage below |

## 🚀 Using the Unified CLI

Instead of remembering each script name, run:

```bash
python scripts/cli.py <command> [args...] [--no-color] [--examples] [--run-example N]
```

**Available Commands**

| Command       | Purpose |
|---------------|---------|
| `view`        | View conversation history for a given workspace and user |
| `workspaces`  | List all workspaces |
| `users`       | List all users in a workspace |
| `dump`        | Dump archived messages to JSON |
| `clear`       | Clear active history for a user |
| `merge`       | Merge active + archived history into a single `.txt` transcript |
| `config show` | Show current MEMORY_CONFIG |
| `config set`  | Set a MEMORY_CONFIG value and persist to `.env` |

**Examples**

```bash
# View conversation history
python scripts/cli.py view my_workspace user123

# List all workspaces
python scripts/cli.py workspaces

# Dump archived messages to JSON
python scripts/cli.py dump my_workspace user123 > archive.json

# Show only usage examples for a command
python scripts/cli.py view --examples

# Run the second example from a command's docstring
python scripts/cli.py view --run-example 2
```

**🧠 Self‑Documenting Commands**  
Each `cmd_*` function in `cli/commands.py` has a docstring that serves as the short help text, the full description in `--help`, and the source for `--examples` and `--run-example`. This keeps usage instructions close to the code and ensures help output is always up to date.

**⚡ Tab Completion**  
We use [`argcomplete`](https://kislyuk.github.io/argcomplete/) for shell tab completion. Once installed and activated, you can tab‑complete command names, workspace IDs, and user IDs.

**🎨 Color & Emoji Output**  
Enabled by default for better readability. Disable with `--no-color` for CI/CD or plain‑text logs. Output helpers include ✅ success, ⚠️ warning, ❌ error, and 📄 info.

**👨‍💻 Adding a New Command**  
Add a `cmd_*` function in `cli/commands.py` with a docstring that includes usage examples.  
Create a `setup_*_args` function in `cli/main.py` to define arguments.  
Register it in `build_parser()` with `add_command(...)`.  
Test with:
```bash
python scripts/cli.py newcommand --examples
python scripts/cli.py newcommand --run-example 1
```

**🚀 Developer Quickstart**
```bash
git clone <repo-url>
cd <repo-folder>
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install argcomplete
activate-global-python-argcomplete  # optional
python scripts/cli.py workspaces
```
