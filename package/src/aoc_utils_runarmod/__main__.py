import argparse

from .config import main as config
from .inputDownloader import main as all_inputs_downloader
from .start import main as start
from .updateStats import main as update_stats


def main():
    parser = argparse.ArgumentParser(description="AOC setup and download")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("start", add_help=False)
    subparsers.add_parser("updateStats", add_help=False)
    subparsers.add_parser("inputDownloader", add_help=False)
    subparsers.add_parser("config", add_help=False)

    args, unknown = parser.parse_known_args()

    if args.command == "inputDownloader":
        all_inputs_downloader(unknown)
    elif args.command == "updateStats":
        update_stats(unknown)
    elif args.command == "start":
        start(unknown)
    elif args.command == "config":
        config(unknown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
