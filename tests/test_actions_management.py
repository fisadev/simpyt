import pytest

from actions import OpenApp, PressKeys, Wait, Action
from actions_management import get_available_actions, get_action_by_key, get_actions_list


def test_available_actions(mocker):
    mock_actions_module = mocker.MagicMock(
        # objects expected to be ignored:
        some_str_attr="some_str",
        some_dir_attr={"a": 1},
        some_obj_attr=mocker.MagicMock(),
        Action=Action,
        # expected actions:
        OpenApp=OpenApp,
        PressKeys=PressKeys,
        Wait=Wait,
    )
    mocker.patch("actions_management.actions", mock_actions_module)
    assert get_available_actions() == [OpenApp, PressKeys, Wait]


@pytest.mark.parametrize(
    "config_key,expected_action",
    [("press", PressKeys), ("open", OpenApp), ("wait", Wait)],
)
def test_get_action_by_key(config_key, expected_action):
    assert get_action_by_key(config_key) == expected_action


def test_get_actions_list():
    control_config = {
        "some_random_config": 42,
        "actions": [
            {"press": "a b ctrl+a"},
            {"wait": 1.5},
            {"open": "/path/to/executable.exe"},
            {"press": "Esc"},
        ]
    }
    press_action, wait_action, open_action, press_action2 = get_actions_list(control_config)
    assert isinstance(press_action, PressKeys)
    assert press_action.keys_to_press == ["a", "b", "ctrl+a"]

    assert isinstance(wait_action, Wait)
    assert wait_action.seconds_to_wait == 1.5

    assert isinstance(open_action, OpenApp)
    assert open_action.app_path == "/path/to/executable.exe"

    assert isinstance(press_action2, PressKeys)
    assert press_action2.keys_to_press == ["Esc"]
