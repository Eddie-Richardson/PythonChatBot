# cli/commands.py

def cmd_view(args):
    """
    View conversation history for a given workspace and user.

    Examples:
      cli view my_workspace user123
      cli view prod_workspace alice

    This will display the active conversation history in a readable format.
    """
    print(f"Viewing history for {args.workspace}/{args.user_id}")


def cmd_workspaces(args):
    """
    List all workspaces.

    Shows every workspace currently stored in the system.
    """
    print("Listing all workspaces...")


def cmd_users(args):
    """
    List all users in a given workspace.

    Example:
      cli users my_workspace
    """
    print(f"Listing users in {args.workspace}")


def cmd_dump(args):
    """
    Dump archived messages to JSON for a given workspace and user.

    Example:
      cli dump my_workspace user123 > archive.json
    """
    print(f"Dumping archived messages for {args.workspace}/{args.user_id}")


def cmd_clear(args):
    """
    Clear active history for a given workspace and user.

    WARNING: This action is irreversible.
    """
    print(f"Clearing active history for {args.workspace}/{args.user_id}")


def cmd_merge(args):
    """
    Merge active + archived history into a TXT file.

    Useful for exporting a complete conversation log.
    """
    print(f"Merging history for {args.workspace}/{args.user_id}")


def cmd_config_show(args):
    """
    Show current MEMORY_CONFIG values.

    Displays all configuration keys and their current values.
    """
    print("Showing MEMORY_CONFIG...")


def cmd_config_set(args):
    """
    Set a MEMORY_CONFIG value and persist it to .env.

    Example:
      cli config set DB_PATH /tmp/memory.db
    """
    print(f"Setting {args.key} to {args.value}")
