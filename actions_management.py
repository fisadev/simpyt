import actions

class ActionNotFound(Exception):
    ...


def get_available_actions():
    """
    Get available actions

    Returns:
        - a list with all the available Action's subclasses.
    """
    available_actions = []
    for obj_name in dir(actions):
        obj = getattr(actions, obj_name)
        if (
            isinstance(obj, type)
            and issubclass(obj, actions.Action)
            and obj is not actions.Action
        ):
            available_actions.append(obj)

    return available_actions


def get_action_by_key(config_key):
    """
    Get the action that match the given config_key.
    """
    for action in get_available_actions():
        if action.CONFIG_KEY == config_key:
            return action
    raise ActionNotFound(f"Invalid action name '{config_key}'")


def get_actions_list(raw_config):
    """
    Get the list of Action instances defined in the given raw_config.
    """
    actions_in_config = []

    for action_dict in raw_config["actions"]:
        # the config of an action is represented as a dict with a single key/value
        (action_key, action_config), = action_dict.items()

        action_class = get_action_by_key(action_key)
        action = action_class.deserialize(action_config)
        actions_in_config.append(action)

    return actions_in_config
