# `tv-show-renamer`

A TV Show episode automatic-renamer designed around the tvdb_api python project.
The script recursively scans a directory and uses tvdb_api to get the episode details for renaming for all supporting media files.
Does a better job of finding the right show by default than most.

tvdb.com: http://thetvdb.com

tvdb_api: https://github.com/dbr/tvdb_api

Written for and tested on Python 3.7.5

## To Initialise the Project

### Recommended:

## TO-DO:   pip install repo needs to be added.

### Alternatively:
In the root dir of project, run:

    pip install

### Dev Install:
In the root dir of project, run:

    pip install -e .

## Useage

### Running the program:
    usage: tvshowrenamer [-h] [-f TARGET_FILE] [-s SEARCH_DIR] [-o OUTPUT_DIR]
                        [-d DRYRUN] [-l LOG_LEVEL] [-a AUTO_DELETE] [-ws WINSAFE]
                        config

    TV Show Episode Renamer, using the TVDB Api

    positional arguments:
    config                Config.ini file, containing search and output
                            directories, API Key, and templates. Arguments passed
                            in the cmd-line override config arguments. See
                            README.md for full outline.

    optional arguments:
    -h, --help            show this help message and exit
    -f TARGET_FILE, --target_file TARGET_FILE
                            File to rename. If this arg is provided, search_dir
                            will be ignored
    -s SEARCH_DIR, --search_dir SEARCH_DIR
                            Directory to search for files to rename. This option
                            overrides the -f tag.
    -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            The root TV Show directory to move the file to when
                            renamed. If configured, the folder structure will be
                            built according to the templates in the config file.
    -d DRYRUN, --dryrun DRYRUN
                            Outputs suggested filename changes without
                            implementing.
    -l LOG_LEVEL, --log_level LOG_LEVEL
                            Log level for debug.
    -a AUTO_DELETE, --auto_delete AUTO_DELETE
                            Deletes files which are not videos or subtitles.
    -ws WINSAFE, --winsafe WINSAFE
                            Ensures files are renamed with windows-safe characters
                            only. ie. "\/<>|:*?"

### Config.json:
`config.ini` must be passed to the program as the first argument. ie:

    tvshowrenamer "path/to/config.ini"

Example `Config.ini`:

    [SETTINGS]
    APIKEY = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # OPTIONAL SETTINGS:
    SEARCH_DIR = home/temp_dl_tv/
    OUTPUT_DIR_ROOT = media/TV Shows/
    # OPTIONAL SETTINGS (WITH DEFAULTS):
    EPISODE = {series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}
    SEASON_FOLDER = Season {0:02d}
    AUTO_DELETE = false
    WINSAFE = false

See http://thetvdb.com/?tab=apiregister to get your own API key.
The program will work without the API Key for testing, but it's highly recommended you get one if you're using it long-term.

The directories `SEARCH_DIR` and `OUTPUT_DIR_ROOT` aren't necessary, however if `SEARCH_DIR` is not set in cfg or passed in cmd-line args, target-file must be.
If the output directory `OUTPUT_DIR_ROOT` is not specified, it will rename files in-place.

An `ignore_list.json` file is created and maintained in the search directory `SEARCH_DIR`. This is to prevent repeated calls to the api for failed files when the program is run in automation scripts.

If `AUTO_DELETE` is true, any file that is not a media (or sub) file will be deleted. Be careful with this! Additional functionality to only delete files with certain extensions needs to be added in the future. (Though it would be trivial if you wanted to modify the code)

`EPISODE` has the following keywords:
    
-  `series_title`   = The title of the series as given by TVDB
-  `s_no`           = Season number, as integer
-  `ep_no`          = Episode number, as integer
-  `ep_name`        = The name of the episode as given by TVDB

The string follows the Python String Format Spec. Mini Language, as given by:
https://docs.python.org/3.4/library/string.html#formatspec

Default  `SEASON_FOLDER` and `EPISODE`:

`Season {0:02d}` and `{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}`

gives:

`OUTPUT_DIR_ROOT\Series Title\Season XX\Series Title - SXXEXX - Episode Title.ext`

### Running the script:
Once the `config.ini` is set up, simply run the script as its root directory:

    tvshowrenamer "path/to/config.ini"

or with cmd-line arguments, such as:

    tvshowrenamer [-h] [-f TARGET_FILE] [-s SEARCH_DIR] [-o OUTPUT_DIR]
                    [-d DRYRUN] [-l LOG_LEVEL] [-a AUTO_DELETE] [-ws WINSAFE]
                    "path/to/config.ini"

### Automation:

The script can be run on a schedule using Task Scheduler (Win) or cronjobs (UNIX), as long as the config is set up correctly (see above). I