# cli/completers.py
def workspace_completer(prefix, parsed_args, **kwargs):
    # return list of workspace names
    return ["default", "test", "prod"]

def user_completer(prefix, parsed_args, **kwargs):
    # return list of user IDs for the given workspace
    return ["user123", "user456"]
