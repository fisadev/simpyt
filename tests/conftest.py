import platform


def pytest_addoption(parser):
    """
    Add custom options for running pytest.
    """
    parser.addoption(
        "--windows",
        action="store_true",
        default=False,
        help="simulate Windows system (Linux by default)",
    )

def pytest_configure(config):
    if config.getoption("--windows"):
        system_name = "Windows"
    else:
        system_name = "Linux"

    platform.system = lambda: system_name
