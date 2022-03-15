"""Main point to run program."""
from ua_itarmy_parser.logging import log
from ua_itarmy_parser.main import client, main


def run() -> None:
    """Main function to run all."""
    with client:
        client.loop.run_until_complete(main())


if __name__ == "__main__":
    log.info("Hello World!")
    run()
