import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="http://localhost:5000", help="pass custom url"
    )
    parser.addoption(
        "--local", action="store", default="0", help="if you are using a dev server and dont want a threaded server"
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def local(request):
    return request.config.getoption("--local")
