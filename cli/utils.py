# cli/utils.py
import sys
import textwrap
import re

USE_COLOR = True
USE_EMOJI = True


def disable_color_and_emoji():
    global USE_COLOR, USE_EMOJI
    USE_COLOR = False
    USE_EMOJI = False


def error(msg):
    prefix = "❌ " if USE_EMOJI else ""
    if USE_COLOR:
        print(f"\033[31m{prefix}{msg}\033[0m", file=sys.stderr)
    else:
        print(f"{prefix}{msg}", file=sys.stderr)


def extract_examples(docstring: str):
    """Return a list of example command strings from a docstring."""
    if not docstring:
        return []
    lines = textwrap.dedent(docstring).splitlines()
    examples = []
    capture = False
    for line in lines:
        if re.match(r"^\s*Examples?:", line):
            capture = True
            continue
        if capture:
            if line.strip() == "" and examples and examples[-1] == "":
                break
            if line.strip():
                examples.append(line.strip())
    return examples
