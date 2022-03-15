"""Some exception classes for testing."""


class TestException(Exception):
    """Base class for custom exceptions, which using in tests."""

    __test__ = False


class TestPassed(TestException):
    """Exception which raising when test passed. Using for handling something in tests."""


class TestFailed(TestException):
    """Exception which raising when test failed. Using for handling something in tests."""


class TestInfo(TestException):
    """Exception which raising when test try to get information from monkeypatch."""
