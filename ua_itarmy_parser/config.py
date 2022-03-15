"""Config file. Global variables here (suck haters)."""
from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from os import environ
from pathlib import Path
from typing import Union

from ua_itarmy_parser.logging import log

# Config object, use ``from config import config``.
config = ConfigParser()

# Base dir, same to folder where ``README.md``.
# Absolute path, but not hard-coded.
BASE_DIR = Path(__file__).parent.parent


class ConfigGenerator:
    """Collection of methods for config generation.

    Attributes:
        config: ConfigParser object with main config.
    """

    def __init__(self, config: ConfigParser) -> None:
        """__init__ method.

        Args:
            config: ConfigParser object.
        """
        self.config: ConfigParser = config

    @classmethod
    def init_config(cls, config: ConfigParser) -> ConfigGenerator:
        """Initialize and configure config.

        Args:
            config: Clear ConfigParser object.

        Returns:
            Initialized and configured config.
        """
        log.debug("Loading config from file")
        config.read(BASE_DIR / environ.get("ITARMY_CONFIG_PATH", "config.ini"))

        default_config = ConfigParser()
        default_config.read_string(
            """
[app]
id = 12345
hash = abcd...
phone = +3809999999...
[ddos.together]
links_and_ipv4_together = false
file_to_write = ./ddos.txt
command = ddos-tool start --targets=/home/app/ddos.txt
[ddos.links]
enable = true
file_to_write = ./links.txt
command = ddos-tool start --sites=/home/app/links.txt
remove_http_before_pass_to_tool = true
[ddos.ipv4]
enable = true
file_to_write = ./ipv4.txt
command = ddos-tool start --ips=/home/app/ipv4.txt
"""
        )

        my_cls = cls(config)
        log.debug("Config class initialised. Configuring it...")
        my_cls.add_default_values(my_cls.config, default_config)
        my_cls.overwrite_with_env(my_cls.config)
        my_cls._write_config_to_file()

        log.debug("Config configuring done.")
        return my_cls

    def add_default_values(
        self,
        config: Union[ConfigParser, SectionProxy],
        default_config: Union[ConfigParser, SectionProxy],
    ) -> None:
        """Recursively add default values to config object, if it not exists.

        Args:
            config: Main config object.
            default_config: Default values for config in dict.
        """
        log.debug("Recursively run 'config.add_default_values'.")
        log.debug("Types: [{0}, {1}]".format(type(config), type(default_config)))
        for level in default_config:
            if level not in config:
                config[level] = default_config[level]  # type: ignore[assignment]
                log.debug(level + " wasn't in config, added.")

            if type(config[level]) is SectionProxy:
                self.add_default_values(config[level], default_config[level])  # type: ignore[arg-type]

    def _write_config_to_file(self) -> None:
        """Write ``ConfigGenerator.config`` to file with name``config.ini``."""
        with open(BASE_DIR / environ.get("ITARMY_CONFIG_PATH", "config.ini"), "w") as config_file:
            log.debug("Writing config to file...")
            self.config.write(config_file)

    def overwrite_with_env(self, config: Union[ConfigParser, SectionProxy]) -> None:
        """Overwrite config values with ENV variables, if they set.

        Args:
            config: Main config object.
        """
        log.debug("Recursively run 'config.overwrite_with_env'")
        for level in config:
            if type(config[level]) is SectionProxy:
                self.overwrite_with_env(config[level])  # type: ignore[arg-type]
            else:
                log.debug("Try to overwrite value in config with ENV variable...")
                env_variable = "ITARMY_{0}_{1}".format(config.name.upper(), level.upper())  # type: ignore[union-attr]
                config[level] = environ.get(env_variable, str(config[level]))  # type: ignore[assignment]
                if environ.get(env_variable) is not None:
                    log.info(
                        "Overwrite '{0}' with value '{1}' (ENV variable '{2}').".format(
                            level, environ[env_variable], env_variable
                        )
                    )


ConfigGenerator.init_config(config)
