"""
Main entry-point for package.
"""
# from .parse_args import get_args
import os
from guessit import guessit
from .initialize import init
from .tvdb import TVDBRenamer
from tqdm import tqdm

# should get api_key,
#            search_dir OR
#            target_file,
#            output_dir,
#            templates[dict: episode,season_folder],
#            dryrun,
#            log_level,
#            auto_delete
#            excluded_ext
#            min_video_size


def logger_setup(log_level):
    # sets up logger in main module
    pass


def parse_info(file_):
    # applies guessit
    return guessit(file_)


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


def _det_type(info):
    # determines file_info "media_type" to file for later sorting
    if "container" in info:
        if info["type"] == "episode":
            if "season" in info and "episode" in info:
                if info["container"] in VIDEO_EXTENSIONS:
                    return "tvepisode"
                elif info["container"] in SUBTITLE_EXTENSIONS:
                    return "tvepisode_sub"

            elif "season" in info or "episode" in info:
                if "episode_title" in info:
                    if info["container"] in VIDEO_EXTENSIONS:
                        return "tvanime"
                    elif info["container"] in SUBTITLE_EXTENSIONS:
                        return "tvanime_sub"

        if info["type"] == "movie":
            if info["container"] in VIDEO_EXTENSIONS:
                return "movie"
            elif info["container"] in SUBTITLE_EXTENSIONS:
                return "movie_sub"
        return "misc_video"
    return "unknown"


def scan_dir(directory):
    all_files = []
    all_subfolders = []
    for _, subdirs, files in tqdm(os.walk(directory)):
        all_subfolders.extend(subdirs)
        all_files.extend(files)

    return all_subfolders, all_files


def main():
    args = init()
    logger_setup(args.log_level)

    print("args: ", args)

    ignore_list = args.ignore_list

    if args.target_file:
        files = [args.target_file]
    elif args.search_dir:
        all_subfolders, all_files = scan_dir(args.search_dir)
        files = [file_ for file_ in tqdm(all_files)]  # if file_ not in ignore_list]

    for file_ in tqdm(files):  # tqdm??
        file_info = guessit(file_)
        media_type = _det_type(file_info)

        if media_type not in ["tvepisode", "tvepisode_sub"]:  # not
            print("{:15}{}".format(media_type, file_))
        #     tvdb_info = t.tvdb_episode_info(file_info)
        #     if tvdb_info:
        #         new_filename = t.new_ep_filename(file_, tvdb_info)
        #         if not dryrun:
        #             rename(file_, new_filename)
        #         else:
        #             # log filename => new_filename
        #             pass
        #     else:
        #         # can't get tvdb info for file_
        #         ignore_list.append(file_)
        # elif media_type == "tvanime" or "tvanime_sub":
        # to be implemented
        # ignore_list.append(file_)
        # elif media_type == "movie" or "movie_sub":
        # not implemented
        # ignore_list.append(file_)
        # elif media_type == "misc_video":
        #     if file_.size < args.min_video_size:
        #         if args.auto_delete:
        #             delete(file_)
        #         else:
        #             ignore_list.append()
        #     else:
        #         ignore_list.append()
        # else:
        #     if args.auto_delete:
        #         delete(file_)
        #     else:
        #         ignore_list.append(file_)


# problem files:
# misc_video    Mr. Robot - S01E01 - eps1.0_hellofriend.mov.mp4
# misc_video    Mr. Robot - S01E02 - eps1.1_ones-and-zer0es.mpeg.mp4
# misc_video    Mr. Robot - S01E03 - eps1.2_d3bug.mkv.mp4
# misc_video    Mr. Robot - S01E05 - eps1.4_3xpl0its.wmv.mp4
# misc_video    Mr. Robot - S01E06 - eps1.5_br4ve-trave1er.asf.mp4
