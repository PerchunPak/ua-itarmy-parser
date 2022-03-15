"""Module for initialise and run DDOS."""
from datetime import datetime
from pathlib import Path
from subprocess import check_output
from typing import List, Literal

from ua_itarmy_parser.config import config
from ua_itarmy_parser.logging import log


class RunDDOS:
    """Main class to run DDOS attack.

    Attributes:
        targets: List with targets to attack.
        targets_str: All targets, but in string. Every target on new line.
        method: Method for DDOS to use. Can be "together" or "links" or "ipv4".
    """

    def __init__(self, targets: List[str], method: Literal["together", "links", "ipv4"]) -> None:
        """__init__ method.

        Args:
            targets: List with targets to attack.
            method: Method for DDOS to use. Can be "together" or "links" or "ipv4".

        Raises:
            KeyError: If argument ``method`` not "together" or "links" or "ipv4".
        """
        if method not in ["together", "links", "ipv4"]:
            raise KeyError("Argument `method` not 'together' or 'links' or 'ipv4'. We get: " + method)

        self.targets = targets
        self.targets_str = self.transform_targets_to_str()
        self.method = method

    def transform_targets_to_str(self) -> str:
        """Transform ``RunDDOS.targets`` in string. Every target on new line.

        Returns:
            All targets in string, every of them on new line.
        """
        targets_str = ""
        for target in self.targets:
            targets_str += target + "\n"
        return targets_str

    @classmethod
    async def init_ddos(
        cls,
        links: List[str],
        ips: List[str],
        links_and_ipv4_together: bool = config.getboolean("ddos.together", "links_and_ipv4_together"),
    ) -> None:
        """Initialise DDOS attack.

        Args:
            links: List with links, which we need DDOS.
            ips: List with IPv4, which we need DDOS.
            links_and_ipv4_together: Is ``links_and_ipv4_together`` activated? Do not specify, used only in tests.

        Raises:
            ValueError: When links or/and IPs not enabled, but ``links_and_ipv4_together`` was enabled.
        """
        if links_and_ipv4_together:
            log.debug("Links and IPs together.")
            if not await cls.check_enabled("together"):
                raise ValueError("Links and IPv4 must be enabled in config if `links_and_ipv4_together = true`")
            return await cls(links + ips, "together").run_ddos()

        if await cls.check_enabled("links"):
            await cls(links, "links").run_ddos()
        if await cls.check_enabled("ipv4"):
            await cls(ips, "ipv4").run_ddos()

    @staticmethod
    async def check_enabled(
        method: Literal["together", "links", "ipv4"],
        links_ddos_enabled: bool = config.getboolean("ddos.links", "enable"),
        ipv4_ddos_enabled: bool = config.getboolean("ddos.ipv4", "enable"),
    ) -> bool:
        """Check if method(s) enabled.

        Args:
            method: Method to check, can be "together" or "links" or "ipv4".
            links_ddos_enabled: Is ``ddos.links.enable`` activated? Do not specify, using this only in tests.
            ipv4_ddos_enabled: Is ``ddos.ipv4.enable`` activated? Do not specify, using this only in tests.

        Returns:
            bool, if it okay - True, else False.

        Raises:
            KeyError: If argument ``method`` not "together" or "links" or "ipv4".
        """
        if method not in ["together", "links", "ipv4"]:
            raise KeyError("Argument `method` not 'together' or 'links' or 'ipv4'. We get: " + method)

        log.debug("Check if enabled: " + method)
        return {
            "together": links_ddos_enabled and ipv4_ddos_enabled,
            "links": links_ddos_enabled,
            "ipv4": ipv4_ddos_enabled,
        }[method]

    async def run_ddos(self) -> None:
        """Run DDOS attack."""
        log.debug("Run ddos with method: " + self.method)
        if len(self.targets) == 0:
            log.debug("No targets specified.")
            return

        await self.handle_targets()
        await self.write_targets_to_file(config["ddos." + self.method]["file_to_write"])
        await self.actually_run_ddos(config["ddos." + self.method]["command"])

    async def handle_targets(
        self,
        remove_http_prefixes: bool = config.getboolean("ddos.links", "remove_http_before_pass_to_tool"),
    ) -> None:
        """Remove ``http(s)://`` prefixes in targets and same targets.

        Args:
            remove_http_prefixes: Is we need remove ``http(s)://`` prefixes in targets? Used only in tests,
              better not touch.
        """
        if remove_http_prefixes:
            log.debug("Remove 'http(s)://' prefixes...")
            custom_targets: List[str] = []
            for target in self.targets:
                custom_targets.append(target.replace("http://", "").replace("https://", ""))
            self.targets = custom_targets
            # Also update ``targets_str``, because we updated ``targets``
            self.targets_str = self.transform_targets_to_str()
            log.debug("Done. Removed all 'http(s)://' prefixes.")

        # It's removing duplicates from targets.
        self.targets = list(dict.fromkeys(self.targets))
        # Also update ``targets_str``, because we updated ``targets``
        self.targets_str = self.transform_targets_to_str()
        log.debug("Removed duplicates from targets.")

    async def write_targets_to_file(self, file_to_write: str) -> None:
        """Write ``RunDDOS.targets`` to file specified in config.

        Args:
            file_to_write: File to which we need write targets.
        """
        with open(file_to_write, "w") as opened_file:
            opened_file.write(self.targets_str)
            opened_file.flush()
        log.debug("Links for DDOS wrote in file: " + file_to_write)

    async def actually_run_ddos(self, ddos_command: str) -> None:
        """Actually run DDOS attack.

        Args:
            ddos_command: We recommend always specify ``config["ddos." + RunDDOS.method]["command"]`` in this parameter.
              Something another can be only in tests.
        """
        time_started = str(datetime.now())[:-7]
        log.info("Run DDOS...")
        log.debug("Run DDOS with command: " + ddos_command)
        try:
            self._run_command(ddos_command)
        except FileNotFoundError:
            log.critical("Command to DDOS (" + ddos_command + ") refers to non exists command.")
            exit(1)
        log.info("DDOS ended, started at " + time_started)

    @staticmethod
    def _run_command(ddos_command: str) -> bytes:
        """Run command with subprocess.check_output, created for tests.

        Args:
            ddos_command: Command for ddos.
        """
        return check_output(ddos_command.split(" "), shell=True)
