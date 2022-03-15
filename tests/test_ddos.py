"""Tests for file ``ua_itarmy_parser.ddos``."""
from os import remove
from subprocess import check_output
from typing import Literal

from pytest import mark, raises

from tests.classes import TestFailed, TestInfo, TestPassed
from ua_itarmy_parser.ddos import RunDDOS


async def test_init_invalid_method() -> None:
    """This test checks if the ``check_enabled`` method raise
    error when argument ``method`` invalid.
    """
    with raises(KeyError):
        RunDDOS([], "invalid")  # type: ignore[arg-type]


def test_init_targets_str() -> None:
    targets = ["https://google.com", "127.0.0.1", "http://example.com"]
    expected = "https://google.com\n127.0.0.1\nhttp://example.com\n"
    assert RunDDOS(targets, "together").targets_str == expected


def test_targets_to_string() -> None:
    targets = ["https://google.com", "127.0.0.1", "http://example.com"]
    expected = "https://google.com\n127.0.0.1\nhttp://example.com\n"
    assert RunDDOS(targets, "together").transform_targets_to_str() == expected


async def test_init_ddos_links_and_ipv4_together_but_invalid(monkeypatch):
    async def fake_check_enabled(*args, **kwargs) -> bool:
        return False

    monkeypatch.setattr(RunDDOS, "check_enabled", fake_check_enabled)

    with raises(ValueError, match="Links and IPv4 must be enabled"):
        await RunDDOS.init_ddos([], [], True)
    monkeypatch.undo()


async def test_init_ddos_links_and_ipv4_together(monkeypatch):
    async def fake_check_enabled(*args, **kwargs) -> bool:
        return True

    def fake_run_ddos(self: RunDDOS) -> None:
        raise TestInfo("Targets: " + str(self.targets) + "\nMethod: " + self.method)

    monkeypatch.setattr(RunDDOS, "check_enabled", fake_check_enabled)
    monkeypatch.setattr(RunDDOS, "run_ddos", fake_run_ddos)

    with raises(TestInfo, match=r"^Targets: \['https://google\.com', '127\.0\.0\.1']\nMethod: together$"):
        await RunDDOS.init_ddos(["https://google.com"], ["127.0.0.1"], True)
    monkeypatch.undo()


@mark.parametrize("method_to_disable", ["ipv4", "links"])
async def test_init_ddos_links_or_ipv4_disabled(method_to_disable: Literal["ipv4", "links"], monkeypatch):
    async def fake_check_enabled(method: Literal["links", "ipv4"]) -> bool:
        if method_to_disable == method:
            return False
        return True

    def fake_run_ddos(self: RunDDOS) -> None:
        raise TestInfo(self.method + " was monkey patched. If it not handled, something went wrong.")

    monkeypatch.setattr(RunDDOS, "check_enabled", fake_check_enabled)
    monkeypatch.setattr(RunDDOS, "run_ddos", fake_run_ddos)

    methods = ["ipv4", "links"]
    methods.remove(method_to_disable)

    pattern = "^(" + "|".join(methods) + ")"
    with raises(TestInfo, match=pattern):
        await RunDDOS.init_ddos([], [], False)
    monkeypatch.undo()


async def test_init_ddos_all_disabled(monkeypatch):
    """Just for test coverage 100%."""

    async def fake_check_enabled(*args, **kwargs) -> bool:
        return False

    monkeypatch.setattr(RunDDOS, "check_enabled", fake_check_enabled)
    await RunDDOS.init_ddos([], [], False)
    monkeypatch.undo()


async def test_check_enabled_invalid_method() -> None:
    """This test checks if the ``check_enabled`` method raise
    error when argument ``method`` invalid.
    """
    with raises(KeyError):
        await RunDDOS.check_enabled("invalid")  # type: ignore[arg-type]


@mark.parametrize("ipv4_enabled", [True, False])
@mark.parametrize("links_enabled", [True, False])
@mark.parametrize("method", ["together", "links", "ipv4"])
async def test_check_enabled_another_methods(
    method: Literal["together", "links", "ipv4"], links_enabled: bool, ipv4_enabled: bool
) -> None:
    if (
        (method == "ipv4" and not ipv4_enabled)
        or (method == "links" and not links_enabled)
        or (method == "together" and (not links_enabled or not ipv4_enabled))
    ):
        assert not await RunDDOS.check_enabled(method, links_enabled, ipv4_enabled)
    else:
        assert await RunDDOS.check_enabled(method, links_enabled, ipv4_enabled)


async def test_run_ddos_no_targets(monkeypatch) -> None:
    """If function don't check is list empty, it will continue work and call subprocess.check_output."""
    obj = RunDDOS([], "ipv4")

    def fake_handle_targets(*args, **kwargs):
        raise TestFailed("RunDDOS.run_ddos() don't check is list with targets empty, and continue work.")

    monkeypatch.setattr(RunDDOS, "handle_targets", fake_handle_targets)
    await obj.run_ddos()
    monkeypatch.undo()


@mark.parametrize("step", ["handle_targets", "write_targets_to_file", "actually_run_ddos"])
async def test_run_ddos_steps(
    step: Literal["handle_targets", "write_targets_to_file", "actually_run_ddos"], monkeypatch
) -> None:
    """If function don't check is list empty, it will continue work and call subprocess.check_output."""
    obj = RunDDOS(["127.0.0.1", "https://google.com"], "together")

    def fake_step_function(*args, **kwargs):
        raise TestPassed("Step working! Handle me pls!")

    monkeypatch.setattr(RunDDOS, step, fake_step_function)
    with raises(TestPassed, match="Step working!"):
        await obj.run_ddos()
    monkeypatch.undo()


async def test_handle_targets_remove_same() -> None:
    targets = ["127.0.0.1", "https://google.com", "https://google.com", "http://google.com"]
    expected = ["127.0.0.1", "https://google.com", "http://google.com"]
    obj = RunDDOS(targets, method="together")
    await obj.handle_targets(False)
    assert obj.targets == expected


async def test_handle_targets_remove_prefix_and_same() -> None:
    targets = ["127.0.0.1", "https://google.com", "https://google.com", "http://google.com"]
    expected = ["127.0.0.1", "google.com"]
    obj = RunDDOS(targets, method="together")
    await obj.handle_targets(True)
    assert obj.targets == expected


async def test_write_targets_to_file() -> None:
    targets = ["https://google.com", "127.0.0.1", "http://example.com"]
    expected = "https://google.com\n127.0.0.1\nhttp://example.com\n"
    obj = RunDDOS(targets, "together")
    await obj.write_targets_to_file("test.txt")
    with open("test.txt", "r") as opened_file:
        content = opened_file.read()
    assert content == expected
    remove("test.txt")


async def test_actually_run_ddos_run_command(monkeypatch):
    def fake_run_command(*args, **kwargs) -> None:
        raise TestPassed("Command ran!")

    monkeypatch.setattr(RunDDOS, "_run_command", fake_run_command)
    with raises(TestPassed, match="^Command ran!$"):
        await RunDDOS([], "together").actually_run_ddos("echo Test!")
    monkeypatch.undo()


async def test_actually_run_ddos_run_command_and_fail(monkeypatch):
    def fake_run_command(*args, **kwargs) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(RunDDOS, "_run_command", fake_run_command)
    with raises(SystemExit, match="^1$"):
        await RunDDOS([], "together").actually_run_ddos("echo Test!")
    monkeypatch.undo()


async def test_actually_run_ddos_coverage_fake(monkeypatch):
    def fake_run_command(*args, **kwargs) -> None:
        return

    monkeypatch.setattr(RunDDOS, "_run_command", fake_run_command)
    await RunDDOS([], "together").actually_run_ddos("echo Test!")
    monkeypatch.undo()


def test_actually_run_command(monkeypatch):
    expected = check_output(["echo", "test"], shell=True)
    result = RunDDOS([], "together")._run_command("echo test")
    assert result == expected
