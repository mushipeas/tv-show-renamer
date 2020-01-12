import argparse
import configparser
import json
import os
from pathlib import Path
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__


# here = os.path.abspath(os.path.dirname(__file__))
default_ep_template = "{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}.{ext}"
default_sf_template = "Season {0:02d}"


def init():
    """Initialise the script by combining cmd-line and config args, and getting
    the ignore_list.
    """
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        "config",
        help="""Config.ini file, containing search and output directories,
            API Key, and templates. Arguments passed in the cmd-line
            override config arguments.
            See README.md for full outline.
            """,
        type=str,
    )

    parser.add_argument(
        "-f",
        "--target_file",
        help="""File to rename. If this arg is provided, search_dir will be ignored""",
        type=str,
        default=None,
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
    )

    parser.add_argument(
        "-ws",
        "--winsafe",
        help="""Ensures files are renamed with windows-safe
            characters only. ie. "\\/<>|:*?"
            """,
        type=bool,
    )

    args = parser.parse_args()

    if args.dryrun:
        args.auto_delete = False

    try:
        _parse_config(args)
    except (ValueError, AttributeError, KeyError):
        print("Config file does not meet format requirements. See README.md.")
        exit()
    else:
        print("DRYRUN     : " + str(args.dryrun))
        print("AUTODELETE : " + str(args.auto_delete))
        if not args.search_dir and not args.target_file:
            print("No files to parse. Please set search_dir or target_file")
            exit()
        _append_ignorelist(args)
        return args


def _parse_config(args):
    # add config variables to args
    _cfg = configparser.ConfigParser()
    _cfg.read(args.config)

    cfg = _cfg["SETTINGS"]

    args.apikey = cfg.get("APIKEY", None)

    if args.search_dir:
        args.search_dir = Path(args.search_dir)
    elif "SEARCH_DIR" in cfg:
        args.search_dir = Path(cfg.get("SEARCH_DIR"))

    if args.output_dir:
        args.output_dir = Path(args.output_dir)
    elif "OUTPUT_DIR_ROOT" in cfg:
        args.output_dir = Path(cfg.get("OUTPUT_DIR_ROOT"))

    args.templates = {
        "episode": cfg.get("EPISODE", default_ep_template),
        "season_folder": cfg.get("SEASON_FOLDER", default_sf_template),
    }

    if not args.auto_delete:
        args.auto_delete = cfg.getboolean("AUTO_DELETE", False)

    if not args.winsafe:
        args.winsafe = cfg.getboolean("WINSAFE", False)

    return None


def _append_ignorelist(args):
    # append [ignore_list] to args
    if args.search_dir:
        ignore_list_file = os.path.join(args.search_dir, "ignore_list.json")
    else:
        ignore_list_file = os.path.join(
            os.path.dirname(args.target_file), "ignore_list.json"
        )

    try:
        ignore_list = _generate_ignore_list(ignore_list_file)
    except:
        # log issue with ignore_list
        raise
    else:
        args.ignore_list_file = ignore_list_file
        args.ignore_list = ignore_list
    return None


def _generate_ignore_list(ignore_list_file):
    # generate ignore_list, either from file or empty (if it doesn't exist)
    try:
        with open(ignore_list_file, "r", encoding="utf-8") as f:
            ignore_list = json.load(f)
        return ignore_list
    except FileNotFoundError:
        # log new ignore_list generated
        return ["ignore_list.json"]
    except:
        raise
