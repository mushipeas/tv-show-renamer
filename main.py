#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Renames TV episodes with data from the TVDB."""

# import argparse
import os
import sys
import json
import shutil
from pathlib import Path
from renamer import Renamer, Defaults

__name__: str = 'tv-show-renamer'
__version__: str = '0.0.1'

# Get Config data
with open('config.json') as json_data_file:
    cfg = json.load(json_data_file)
# necessary configs
APIKEY = cfg['APIKEY'] if 'APIKEY' in cfg else None
SEARCH_DIR = cfg['SEARCH_DIR']
# optional configs
OUTPUT_DIR_ROOT = cfg['OUTPUT_DIR_ROOT'] if 'OUTPUT_DIR_ROOT' in cfg else SEARCH_DIR
FILE_NAME_TEMPLATE = cfg['FILE_NAME_TEMPLATE'] if 'FILE_NAME_TEMPLATE' in cfg else Defaults.FILE_NAME_TEMPLATE
PATTERN = cfg['PATTERN'] if 'PATTERN' in cfg else Defaults.PATTERN
SEASON_DIR_TEMPLATE= cfg['SEASON_DIR_TEMPLATE'] if 'SEASON_DIR_TEMPLATE' in cfg else Defaults.SEASON_DIR_TEMPLATE
MAKEWINSAFE = cfg['MAKEWINSAFE'] if 'MAKEWINSAFE' in cfg else True
DRYRUN = cfg['DRYRUN'] if 'DRYRUN' in cfg else True 
AUTODELETE = cfg['AUTODELETE'] if 'AUTODELETE' in cfg and not DRYRUN else False

print(' ------- DRYRUN     : ' + str(DRYRUN))
print(' ------- AUTODELETE : ' + str(AUTODELETE))

if APIKEY: rn = Renamer(FILE_NAME_TEMPLATE=FILE_NAME_TEMPLATE,
            PATTERN=PATTERN,
            SEASON_DIR_TEMPLATE=SEASON_DIR_TEMPLATE,
            MAKEWINSAFE=MAKEWINSAFE,
            APIKEY=APIKEY)

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def recursive_dir_scan(search_dir, file_output):
    with os.scandir(search_dir) as it:
        for entry in it:
            if entry.is_dir():
                recursive_dir_scan(entry, file_output)
                if AUTODELETE:
                    try:
                        os.rmdir(entry.path)
                        log = '[x]      {:<60}   ->   Deleted.'.format(entry.name)
                        file_output.append(log+'\n')
                        print(log)
                    except:
                        log = '[x]      {:<60}   ->   Could not delete.'.format(entry.name)
                        file_output.append(log+'\n')
                        print(log)
            if entry.is_file():
                orig_filename = entry.name
                new_rel_path = rn.get_relative_pathname(orig_filename)
                if new_rel_path:
                    new_abs_path = os.path.join(OUTPUT_DIR_ROOT, new_rel_path)
                    log = '         {:<60}   ->   {}'.format(orig_filename[:55],new_rel_path)
                    file_output.append(log+'\n')
                    print(log)
                    if not DRYRUN:
                        ensure_dir(new_abs_path)
                        shutil.move(entry.path,new_abs_path)
                else:
                    if AUTODELETE:
                        try:
                            os.remove(entry.path)
                            log = '[x]      {:<60}   ->   Deleted.'.format(entry.name)
                            file_output.append(log+'\n')
                            print(log)
                        except: 
                            log = '[x]      {:<60}   ->   Could not delete.'.format(entry.name)
                            file_output.append(log+'\n')
                            print(log)
                    else:
                        log = '[x]      {:<60}   ->   Unchanged.'.format(entry.name)
                        file_output.append(log+'\n')
                        print(log)
    return file_output

file_output = []
recursive_dir_scan(SEARCH_DIR, file_output)
print(" ------- Finished Script")

# text output
with open('outputfile.txt', 'w+', encoding='utf-8') as output_file:
    for item in file_output:
        output_file.write(item)
