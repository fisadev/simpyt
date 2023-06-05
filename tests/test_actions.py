import pytest

import actions


class TestAction:
    @staticmethod
    def test_actions_by_prefix():
        """
        Check that all the existing actions were added to the actions dict.

        This test is just a sanity check for actions config. Please, update it if you
        create new actions.
        """
        assert actions.Action.ACTIONS_BY_PREFIX == {
            "keys": actions.KeysAction,
            "write": actions.Write,
            "wait": actions.Wait,
            "run": actions.RunCommand,
            "joystick": actions.JoystickAction,
            "quit": actions.Quit,
        }

    @staticmethod
    def test_action_find_and_deserialize_happy_path(mocker):
        CustomActionMock = mocker.MagicMock()
        mocker.patch("actions.Action.ACTIONS_BY_PREFIX", {"test_action": CustomActionMock})

        actions.Action.find_and_deserialize("test_action some-config")

        CustomActionMock.deserialize.assert_called_once_with("some-config")

    @staticmethod
    def test_action_find_and_deserialize_invalid_action():
        # pre-condition
        assert "test_action" not in actions.Action.ACTIONS_BY_PREFIX

        with pytest.raises(actions.ImproperlyConfiguredException, match="Unknown action"):
            actions.Action.find_and_deserialize("test_action some-config")

    @staticmethod
    def test_actionfind_and_deserialize_has_no_argument_happy_path():
        pass


    @staticmethod
    def test_actionfind_and_deserialize_has_no_argument_but_should_have():
        pass

    @staticmethod
    def test_actionfind_and_deserialize_has_arguments_but_should_not_have():
        pass
