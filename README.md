# `tv-show-renamer`


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
        "SEARCH_DIR" : "/temp_dl/TV Shows/",
        "OUTPUT_DIR_ROOT" : "media/TV Shows/"
    }

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