import argparse
import json
import os

from colorama import Fore
from colorama import init as colorama_init

colorama_init(autoreset=True)

BASE_PATH = os.path.join(os.path.expanduser("~"), "aoc_utils")
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)

CONFIG_PATH = os.path.join(BASE_PATH, "config.json")

CONFIG_KEYS = ["cookie", "repo_path", "template_path"]


def create_config() -> bool:
    if os.path.exists(CONFIG_PATH):
        print(f"{Fore.RED}Config file already exists.")
        return False

    with open(CONFIG_PATH, "w") as f:
        json.dump({}, f, indent=4)

    return True


def read_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        print(f"{Fore.RED}Config file not found. Creating one.")
        create_config()
        return {}

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    return config


def get_cookie() -> str | None:
    config = read_config()
    if "cookie" not in config:
        raise Exception("cookie not found in config.json")
    return config["cookie"]


def set_cookie(cookie: str) -> bool:
    config = read_config()
    config["cookie"] = cookie
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    return True


def get_repo_path() -> str:
    config = read_config()
    if "repo_path" not in config:
        raise Exception("repo_path not found in config.json")
    return config["repo_path"]


def set_repo_path(repo_path: str) -> bool:
    config = read_config()
    config["repo_path"] = repo_path
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    return True


def get_template_path() -> str:
    config = read_config()
    if "template_path" not in config:
        raise Exception("template_path not found in config.json")
    return config["template_path"]


def set_template_path(template_path: str) -> bool:
    config = read_config()
    config["template_path"] = template_path
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    return True


def missing_config() -> list[str]:
    config = read_config()
    missing = []
    for key in CONFIG_KEYS:
        if key not in config:
            missing.append(key)
    return missing


def main(args: list[str] = None):
    parser = argparse.ArgumentParser(description="Modify/see config settings")
    parser.add_argument(
        "-m",
        "--see_missing",
        action="store_true",
        help="See missing config settings",
    )
    parser.add_argument(
        "-c",
        "--cookie",
        type=str,
        help="Set the cookie used to download the inputs",
    )
    parser.add_argument(
        "-r",
        "--repo_path",
        type=str,
        help="Set the path to the repository where the solutions are stored",
    )
    parser.add_argument(
        "-t",
        "--template_path",
        type=str,
        help="Set the path to the template file",
    )

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    missing = missing_config()
    if args.repo_path:
        set_repo_path(args.repo_path)
        print(f"{Fore.GREEN}repo_path set to {args.repo_path}")
    elif args.template_path:
        set_template_path(args.template_path)
        print(f"{Fore.GREEN}template_path set to {args.template_path}")
    elif args.cookie:
        set_cookie(args.cookie)
        print(f"{Fore.GREEN}cookie set to {args.cookie}")
    elif args.see_missing or len(missing) > 0:
        if len(missing) == 0:
            print(f"{Fore.GREEN}No missing config settings.")
        else:
            print(f"{Fore.RED}Missing config settings:")
            for key in missing:
                print(key)
    else:
        parser.print_help()
