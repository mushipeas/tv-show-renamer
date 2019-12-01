# `tv-show-renamer`

A TV Show episode automatic-renamer designed around the tvdb_api python project.
The script recursively scans a directory and uses tvdb_api to get the episode details for renaming for all supporting media files.
Does a better job of finding the right show by default than most.

tvdb.com: [http://thetvdb.com][tvdb]
tvdb_api: [https://github.com/dbr/tvdb_api][tvdb_api Github]


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
config.json must be places in the root dir with `main.py`.
The search directory `"SEARCH_DIR"` must be specified in the config.
If the output directory `"OUTPUT_DIR_ROOT"` is not specified, it will default to the same as the search directory.

Config.json minimum requirements:

    {
        "APIKEY" : "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "SEARCH_DIR" : "home/temp_dl_tv/",
        "OUTPUT_DIR_ROOT" : "media/TV Shows/"
    }

See http://thetvdb.com/?tab=apiregister to get your own API key
By default the program will dry run and output proposed name changes.
This needs to be turned off by specifying `"DRYRUN" : false` in the config.

### Optional Configs:

    {
        ...
        "OUTPUT_FORMAT_STRING" :  (default = "{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}.{ext}" ),
        "MAKEWINSAFE" :  (default = true),
        "AUTODELETE" :  (default = false),
        "DRYRUN" : (default = true)
    }

If `"AUTODELETE"` is true, any file that is not matched for renaming will be deleted. Be careful with this! Additional functionality to only delete files with certain extensions needs to be added in the future. (Though it would be trivial if you wanted to modify the code)

### Running the script

Once the `config.json` is in place, simply run the script in its root directory:

    python3 main.py

### Automation

The script can be run on a schedule using Task Scheduler (Win) or cronjobs (UNIX), as long as the config is set up correctly (see above). The root dir of the project must first be traversed to in any automated script ie. with the `cd` command before the script is called.