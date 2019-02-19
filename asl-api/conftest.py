import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="http://localhost:5000", help="pass custom url"
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
