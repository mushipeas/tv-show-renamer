# `tv-show-renamer`

A TV Show episode automatic-renamer designed around the tvdb_api python project.
The script recursively scans a directory and uses tvdb_api to get the episode details for renaming for all supporting media files.
Does a better job of finding the right show by default than most.

tvdb.com: http://thetvdb.com

tvdb_api: https://github.com/dbr/tvdb_api

Written for and tested on Python 3.7.5

## To Initialise the Project

### Recommended:
In the root dir of project, run:

    python -m venv .venv
This should create a virtual environment

### Activate the environment:
    .\.venv\Scripts\activate (Windows)
    source env/bin/activate (UNIX)

### Install required packages:
    pip install -r requirements.txt

## Useage

### Config.json:
`config.json` must be placed in the root dir with `__main__.py` (and this README).

The search directory `"SEARCH_DIR"` must be specified in the config.

If the output directory `"OUTPUT_DIR_ROOT"` is not specified, it will default to the same as the search directory.

`Config.json` minimum requirements:

    {
        "APIKEY" :              "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "SEARCH_DIR" :          "home/temp_dl_tv/"
    }

See http://thetvdb.com/?tab=apiregister to get your own API key.

By default the program will dry run and output proposed name changes.

This needs to be turned off by specifying `"DRYRUN" : false` in the config.

### Optional Configs:

    {
        ...
        "OUTPUT_DIR_ROOT" :     "media/TV Shows/",
        "FILE_NAME_TEMPLATE" :  "{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}.{ext}",
        "SEASON_DIR_TEMPLATE" : "Season {0:02d}",
        "MAKEWINSAFE" :         (default = true),
        "AUTODELETE" :          (default = false),
        "DRYRUN" :              (default = true)
    }

If `"AUTODELETE"` is true, any file that is not matched for renaming will be deleted. Be careful with this! Additional functionality to only delete files with certain extensions needs to be added in the future. (Though it would be trivial if you wanted to modify the code)

`"FILE_NAME_TEMPLATE"` has the following keywords:
    
-  `series_title`   = The title of the series as given by TVDB
-  `s_no`           = Season number, as integer
-  `ep_no`          = Episode number, as integer
-  `ep_name`        = The name of the episode as given by TVDB
-  `ext`            = filename extension. Probably leave this as it is

The string follows the Python String Format Spec. Mini Language, as given by:
https://docs.python.org/3.4/library/string.html#formatspec

Default  `"SEASON_DIR_TEMPLATE"` and `"FILE_NAME_TEMPLATE"`:

`"Season {0:02d}"` and `"{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}.{ext}"`

Which gives:

`OUTPUT_DIR_ROOT\Series Title\Season XX\Series Title - SXXEXX - Episode Title.ext`

### Running the script:
Once the `config.json` is in place, simply run the script as its root directory:

    python3 tv-show-renamer

or 

    python3 __main__.py

### Automation:

The script can be run on a schedule using Task Scheduler (Win) or cronjobs (UNIX), as long as the config is set up correctly (see above).

If using a virtual environment, it must be activated by the automation script first (and deactivated after).