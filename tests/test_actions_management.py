from actions import OpenApp, PressKeys, Wait, Action
from actions_management import get_available_actions

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

