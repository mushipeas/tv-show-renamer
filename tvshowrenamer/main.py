"""
Main entry-point for package.
"""
# from .parse_args import get_args
import shutil
from tqdm import tqdm
from .initialize import init
from .tvdb import TVDB
from .renamer import Renamer
from .helpers import _det_type, guess_file_info, assess_media_types
from .helpers import _scan_dir, find_files, ensure_dir, json_dump_file


def logger_setup(log_level):
    # sets up logger in main module
    pass


def main():
    args = init()
    logger_setup(args.log_level)

    # log this:
    # print("args: ", args)

    subfolders, files = find_files(args)
    assessed_files = assess_media_types(files)

    tv_files = [
        file_
        for file_ in assessed_files
        if file_.media_type in ["tvepisode", "tvepisode_sub"]
    ]

    unknown_files = [file_ for file_ in assessed_files if file_.media_type == "unknown"]

    print("Files found that match : {}/{}".format(len(tv_files), len(assessed_files)))
    print(
        "Files found to delete  : {}/{}".format(len(unknown_files), len(assessed_files))
    )

    tvdb = TVDB(args.apikey)
    rn = Renamer(
        args.templates["episode"], args.templates["season_folder"], args.winsafe,
    )

    # tv_files = tqdm(tv_files, desc="Getting TVDB info    ", unit="files")
    for file_, file_info, _ in tv_files:
        tvdb_series, tvdb_episode = tvdb.get_ep_tvdb_info(file_info)

        if tvdb_episode:
            if args.output_dir:
                _new_filename = rn.get_relative_pathname(
                    tvdb_series, tvdb_episode, file_.suffixes
                )
                new_filename = args.output_dir.joinpath(_new_filename)
            else:
                _new_filename = rn.get_ep_filename(
                    tvdb_series, tvdb_episode, file_.suffixes
                )
                new_filename = file_.with_name(_new_filename)

            if args.dryrun:
                # log
                print(
                    "{old_fn:<40.40}  ->  {new_fn}".format(
                        old_fn=file_.name, new_fn=new_filename
                    )
                )
            else:
                ensure_dir(new_filename.parent)
                try:
                    shutil.move(file_, new_filename)
                except FileNotFoundError:
                    # log input file does not exist
                    print(
                        "{:<40.40}  ->  original file does not exist".format(file_.name)
                    )
                else:
                    print(
                        "{old_fn:<40.40}  ->  {new_fn}".format(
                            old_fn=file_.name, new_fn=new_filename
                        )
                    )
                pass
        else:
            # log: can't get tvdb info for file_
            args.ignore_list.append(file_.name)

    for file_, _, _ in unknown_files:
        if args.auto_delete:
            try:
                file_.unlink
            except:
                # log: file cannot be deleted
                raise
        else:
            print("{:<40.40}  ->  file will be deleted".format(file_.name))

    # folder clean-up
    for folder in subfolders:
        try:
            folder.rmdir()
        except OSError:
            # folder not empty
            pass

    json_dump_file(args.ignore_list, args.ignore_list_file)


if __name__ == "__main__":
    import sys

    sys.argv = ["", "config.ini", "-f", "x:\temp\test_files\the.100.mkv", "-d", "True"]
    main()
