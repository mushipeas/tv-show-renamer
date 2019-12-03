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

cfgfile = os.path.join(os.path.dirname(__file__),'config.json')
output_file = os.path.join(os.path.dirname(__file__),'outputfile.txt')
ignore_list_file = os.path.join(os.path.dirname(__file__),'ignore_list.json')

# Get Config data
with open(cfgfile) as json_data_file:
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

def generate_ignore_list(ignore_list_file):
    try:
        with open(ignore_list_file, 'r', encoding='utf-8') as f:
            ignore_list = json.load(f)
        return ignore_list
    except FileNotFoundError:
        return ['dummyname']
    except:
        return ['dummyname'] # needs further breakdown

def recursive_dir_rename(search_dir: str, file_output: list, ignore_list: set):
    with os.scandir(search_dir) as it:
        for entry in it:
            if entry.is_dir():
                recursive_dir_rename(entry, file_output, ignore_list)
                if AUTODELETE:
                    try:
                        os.rmdir(entry.path)
                        file_status = 'Deleted.'
                    except:
                        file_status = 'Could not delete.'
                    formatted_print(entry.name,file_status,file_output,'[x]')
            elif entry.is_file() and entry.name not in ignore_list:
                ignore_list.append(entry.name)
                orig_filename = entry.name
                new_rel_path = rn.get_relative_pathname(orig_filename)
                if new_rel_path:
                    new_abs_path = os.path.join(OUTPUT_DIR_ROOT, new_rel_path)
                    formatted_print(orig_filename, new_rel_path, file_output)
                    if not DRYRUN:
                        ensure_dir(new_abs_path)
                        shutil.move(entry.path,new_abs_path)
                else:
                    if AUTODELETE:
                        try:
                            os.remove(entry.path)
                            file_status = 'Deleted.'
                        except:
                            file_status = 'Could not delete.'
                    else:
                        file_status = 'Unchanged.'
                    formatted_print(entry.name,file_status,file_output,'[x]')
            else:
                file_status = 'Ignored. See ignore_list.'
                formatted_print(entry.name,file_status,file_output,'[x]')
    return file_output

def formatted_print(input_file,stat_or_out,file_output,marker=''):
    log = '{m:<9}{input_f:<60}   ->   {stat_or_out}'.format(m=marker,input_f=input_file[:60],stat_or_out=stat_or_out)
    file_output.append(log+'\n')
    print(log)

# text output
def print_to_file(data, file):
    with open(file, 'w', encoding='utf-8') as output_file:
        for item in data:
            output_file.write(item)

def json_dump_file(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def main():
    verbose_output = []
    ignore_list = generate_ignore_list(ignore_list_file)
    recursive_dir_rename(SEARCH_DIR, verbose_output, ignore_list)
    print_to_file(verbose_output, output_file)
    json_dump_file(ignore_list, ignore_list_file)
    print(" ------- Finished Script")

main()