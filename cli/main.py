# cli/main.py
import argparse
import argcomplete
import sys
import textwrap
import shlex

from .completers import workspace_completer, user_completer
from .commands import (
    cmd_view, cmd_workspaces, cmd_users, cmd_dump,
    cmd_clear, cmd_merge, cmd_config_show, cmd_config_set
)
from .utils import error, disable_color_and_emoji, extract_examples


# --- Argument setup functions ---
def setup_view_args(p):
    p.add_argument("workspace").completer = workspace_completer
    p.add_argument("user_id").completer = user_completer

def setup_users_args(p):
    p.add_argument("workspace").completer = workspace_completer

def setup_dump_args(p):
    p.add_argument("workspace").completer = workspace_completer
    p.add_argument("user_id").completer = user_completer

def setup_clear_args(p):
    p.add_argument("workspace").completer = workspace_completer
    p.add_argument("user_id").completer = user_completer

def setup_merge_args(p):
    p.add_argument("workspace").completer = workspace_completer
    p.add_argument("user_id").completer = user_completer

def setup_config_set_args(p):
    p.add_argument("key")
    p.add_argument("value")


# --- Helper to add commands ---
def add_command(subparsers, name, func, args_setup=None):
    """Add a subcommand with help/description from the function docstring."""
    doc = func.__doc__ or ""
    doc = textwrap.dedent(doc).strip("\n")
    short_help = doc.splitlines()[0] if doc else None
    parser = subparsers.add_parser(name, help=short_help, description=doc)
    parser.add_argument("--examples", action="store_true", help="Show only usage examples for this command")
    parser.add_argument("--run-example", type=int, metavar="N", help="Run the Nth example from the docstring")
    if args_setup:
        args_setup(parser)
    parser.set_defaults(func=func, _doc=doc, _name=name)
    return parser


def build_parser():
    parser = argparse.ArgumentParser(description="Admin CLI for AI assistant memory.")
    parser.add_argument("--no-color", action="store_true", help="Disable colors and emojis in output")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_command(subparsers, "view", cmd_view, setup_view_args)
    add_command(subparsers, "workspaces", cmd_workspaces)
    add_command(subparsers, "users", cmd_users, setup_users_args)
    add_command(subparsers, "dump", cmd_dump, setup_dump_args)
    add_command(subparsers, "clear", cmd_clear, setup_clear_args)
    add_command(subparsers, "merge", cmd_merge, setup_merge_args)

    p_config = subparsers.add_parser("config", help="View or update MEMORY_CONFIG values")
    config_sub = p_config.add_subparsers(dest="config_cmd", required=True)
    add_command(config_sub, "show", cmd_config_show)
    add_command(config_sub, "set", cmd_config_set, setup_config_set_args)

    return parser


def main():
    parser = build_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.no_color:
        disable_color_and_emoji()

    # Handle --examples
    if getattr(args, "examples", False):
        examples = extract_examples(getattr(args, "_doc", ""))
        print("\n".join(examples) if examples else "No examples available.")
        sys.exit(0)

    # Handle --run-example
    if getattr(args, "run_example", None) is not None:
        examples = extract_examples(getattr(args, "_doc", ""))
        idx = args.run_example - 1
        if idx < 0 or idx >= len(examples):
            error(f"Example {args.run_example} not found.")
            sys.exit(1)
        example_cmd = examples[idx]
        if example_cmd.startswith("cli "):
            example_cmd = example_cmd[len("cli "):]
        example_args = parser.parse_args(shlex.split(example_cmd))
        if example_args.no_color:
            disable_color_and_emoji()
        example_args.func(example_args)
        sys.exit(0)

    try:
        args.func(args)
    except Exception as e:
        error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
