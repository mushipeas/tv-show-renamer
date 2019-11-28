#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Downloads and saves comments from Twitch VODs as json data.
Also generates highlight sections for the VOD using comment data.
Currently using the frequency of comments per section of video"""

# import argparse
import os
import sys
import json
import shutil
from pathlib import Path
from renamer.renamer import Renamer

__name__: str = 'tv-show-renamer'
__version__: str = '0.0.1'

# Get Config data
with open('config.json') as json_data_file:
    cfg = json.load(json_data_file)
OUTPUT_FORMAT_STRING = cfg['OUTPUT_FORMAT_STRING']
MAKEWINSAFE = cfg['MAKEWINSAFE']
OUTPUT_DIR_ROOT = cfg['OUTPUT_DIR_ROOT']
SEARCH_DIR = cfg['SEARCH_DIR']

rn = Renamer(OUTPUT_FORMAT_STRING=OUTPUT_FORMAT_STRING)

# test using testfile.txt
def test(testfile):
    output = []
    with open(testfile, 'r') as test_file:
        for line in test_file:
            orig_filename = line[:-1]
            try: new_filename = rn.get_relative_pathname(orig_filename)
            except: print(Exception)
            if new_filename:
                output.append('         {:<60}   ->   {}\n'.format(orig_filename[:55],os.path.basename(new_filename)))
            else:
                output.append('[x]      {:<60}   ->   Shit happened.\n'.format(orig_filename[:55]))
    return output

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def recursive_dir_scan(search_dir, output):
    for entry in os.scandir(search_dir):
        if entry.is_dir():
            recursive_dir_scan(entry, output)
            os.rmdir(entry.path)
        if entry.is_file():
            orig_filename = entry.name
            new_rel_path = rn.get_relative_pathname(orig_filename)
            if new_rel_path:
                new_abs_path = os.path.join(OUTPUT_DIR_ROOT, new_rel_path)
                output.append('         {:<60}   ->   {}\n'.format(orig_filename[:55],new_abs_path))
                print('{:<60}   ->   {}'.format(orig_filename[:55],new_rel_path))
                ensure_dir(new_abs_path)
                shutil.move(entry.path,new_abs_path)
            else:
                output.append('[x]      {:<60}   ->   Deleted.\n'.format(entry.name))
                os.remove(entry.path)
    return output

# output = []
# recursive_dir_scan(SEARCH_DIR, output)

output = test('testfile.txt',)

# test output
with open('outputfile.txt', 'w+') as output_file:
    for item in output:
        output_file.write(item)
