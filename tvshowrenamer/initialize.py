import argparse
import configparser
import json
import os
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__


here = os.path.abspath(os.path.dirname(__file__))


def init():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "config",
        help="""Config.ini file, containing search and output directories,
            API Key, and templates. Any arguments in the config override
            the cmd-line arguments.
            See README.md for full outline.
            """,
        type=str,
    )

    parser.add_argument(
        "-f", "--target_file", help="File to rename.", type=str, default=None,
    )

    parser.add_argument(
        "-s",
        "--search_dir",
        help="""Directory to search for files to rename.
            This option overrides the -f tag.
            """,
        type=str,
        default=None,
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        help="""The root TV Show directory to move the file to when renamed.
            If configured, the folder structure will be built according to
            the templates in the config file.
            """,
        type=str,
        default=None,
    )

    parser.add_argument(
        "-d",
        "--dryrun",
        help="Outputs suggested filename changes without implementing.",
        type=bool,
        default=False,
    )

    parser.add_argument(
        "-l", "--log_level", help="Log level for debug.", type=int, default=0,
    )

    parser.add_argument(
        "-a",
        "--auto_delete",
        help="Deletes files which are not videos or subtitles.",
        type=bool,
        default=False,
    )

    parser.add_argument(
        "-ws",
        "--winsafe",
        help="""Ensures files are renamed with windows-safe
            characters only. ie. "\\/<>|:*?"
            """,
        type=bool,
        default=True,
    )

    args = parser.parse_args()

    if args.search_dir:
        args.target_file = None

    if args.dryrun:
        args.auto_delete = False

    try:
        parse_config(args)
    except (ValueError, AttributeError, KeyError):
        raise  # Exception("Config file does not meet format requirements.")
    else:
        get_ignorelist(args)
        return args


def parse_config(args):
    cfg = configparser.ConfigParser()
    cfg.read(args.config)

    args.apikey = cfg["TVDB"]["APIKEY"]

    if "DIRS" in cfg:
        if "SEARCH_DIR" in cfg["DIRS"] and not args.target_file:
            args.search_dir = os.path.dirname(cfg["DIRS"]["SEARCH_DIR"])
        if "OUTPUT_DIR_ROOT" in cfg["DIRS"]:
            args.output_dir = os.path.dirname(cfg["DIRS"]["OUTPUT_DIR_ROOT"])
    args.templates = (
        {
            "episode": cfg["TEMPLATES"]["EPISODE"],
            "season_folder": cfg["TEMPLATES"]["SEASON_FOLDER"],
        },
    )
    args.auto_delete = cfg["SETTINGS"]["AUTO_DELETE"]
    args.winsafe = cfg["SETTINGS"]["WINSAFE"]
    return None


def get_ignorelist(args):
    if args.search_dir:
        ignore_list_file = os.path.join(args.search_dir, "ignore_list.json")
    else:
        ignore_list_file = os.path.join(
            os.path.dirname(args.target_file), "ignore_list.json"
        )

    try:
        ignore_list = generate_ignore_list(ignore_list_file)
    except:
        raise  # return empty list?
    else:
        args.ignore_list_file = ignore_list_file
        args.ignore_list = ignore_list
    return None


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_ignore_list(ignore_list_file):
    try:
        with open(ignore_list_file, "r", encoding="utf-8") as f:
            ignore_list = json.load(f)
        return ignore_list
    except FileNotFoundError:
        return ["ignore_list.json"]
    except:
        raise  # needs further breakdown


def json_dump_file(data, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)
