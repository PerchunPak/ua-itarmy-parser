from asyncio import get_event_loop_policy

from pytest import fixture


@fixture
def event_loop():
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_sessionfinish(session, exitstatus):
    get_event_loop_policy().new_event_loop().close()
