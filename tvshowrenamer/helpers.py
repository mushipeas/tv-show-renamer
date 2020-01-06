import collections
import json
import os
import re
from tqdm import tqdm
from guessit import guessit
from pathlib import Path

AssessedFile = collections.namedtuple("AssessedFile", "filePath info media_type")


# Extension groups
SUBTITLE_EXTENSIONS = [
    "srt",
    "sub",
    "smi",
    "txt",
    "ssa",
    "ass",
    "mpl",
]
VIDEO_EXTENSIONS = [
    "3gp",
    "3g2",
    "asf",
    "wmv",
    "avi",
    "divx",
    "evo",
    "f4v",
    "flv",
    "mkv",
    "mk3d",
    "mp4",
    "mpg",
    "mpeg",
    "m2p",
    "m4v",
    "ps",
    "ts",
    "m2ts",
    "mxf",
    "ogg",
    "mov",
    "qt",
    "rmvb",
    "vob",
    "webm",
]


def find_files(args):
    # find files (not in ignore_list) to be parsed
    ignore_list = args.ignore_list

    if args.target_file:
        # log single file being parsed
        subfolders = []
        files = [Path(args.target_file)]
    elif args.search_dir:
        subfolders, all_files = _scan_dir(args.search_dir)
        files = [file_ for file_ in all_files if file_.name not in ignore_list]

    return subfolders, files


def assess_media_types(files):
    assessed_files = []
    files = tqdm(files, desc="Assessing input files", unit="files")
    for file_ in files:
        info = guess_file_info(file_)
        media_type = _det_type(info)
        assessed_files.append(
            AssessedFile(filePath=file_, info=info, media_type=media_type,)
        )

    return assessed_files


def ensure_dir(file_path):
    directory = file_path.parent
    if not directory.exists():
        directory.mkdir


def json_dump_file(data, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)


def _scan_dir(directory):
    # returns all [subfolders] and [files] present in directory as path objects
    all_files = []
    all_subfolders = []
    for root, _subdirs, _files in os.walk(directory):
        subdirs = [Path(root, subdir) for subdir in _subdirs]
        files = [Path(root, file_) for file_ in _files]
        all_subfolders.extend(subdirs)
        all_files.extend(files)

    return all_subfolders, all_files


def guess_file_info(file_):
    """ Guess file info using guessit.
    Returns MatchesDict([
            ('title', 'Dexter'),
            ('season', 1),
            ('episode', 6),
            ('year', 2006),
            ('episode_title', 'Return to Sender'),
            ('container', 'mp4'),
            ('mimetype', 'video/mp4'),
            ('type', 'episode')
        ])
    """
    # regex = get_regex_tv_info(file_.name)
    # if regex:
    #     return regex
    # else:
    #     # log regex didn't work - falling back to guessit
    #     return guessit(file_.name)
    return guessit(file_.name)


def _det_type(file_info):
    # determines file_info "media_type" for later sorting, using the return
    # file_info from guessit
    if "container" in file_info:
        if file_info["type"] == "episode":
            if "season" in file_info and "episode" in file_info:
                if file_info["container"] in VIDEO_EXTENSIONS:
                    return "tvepisode"
                elif file_info["container"] in SUBTITLE_EXTENSIONS:
                    return "tvepisode_sub"

            elif "season" in file_info or "episode" in file_info:
                if "episode_title" in file_info:
                    if file_info["container"] in VIDEO_EXTENSIONS:
                        return "tvanime"
                    elif file_info["container"] in SUBTITLE_EXTENSIONS:
                        return "tvanime_sub"

        if file_info["type"] == "movie":
            if file_info["container"] in VIDEO_EXTENSIONS:
                return "movie"
            elif file_info["container"] in SUBTITLE_EXTENSIONS:
                return "movie_sub"
        return "misc_video"
    return "unknown"



def get_regex_tv_info(video_filename: str):
    pattern = r"(^[\w\._\-\s&!\')(]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\[\._\-\ss](\d{1,2})[x\._\-\s]*[e|(ep)|x](\d{1,3})[^\d](?:.*)(mp4|avi|mkv|m4v|webm|divx|idx|srt$)"
    prog = re.compile(pattern, re.IGNORECASE)
    match = prog.match(video_filename)

    output = (
        {
            "original_file_name": match.string,
            "title": match.group(1).replace(".", " "),
            "year": match.group(2),
            "season": int(match.group(3)),
            "episode": int(match.group(4)),
            "container": match.string.split(".")[-1],
            "type": "episode"
        }
        if match
        else {}
    )

    return output