#/usr/bin/python3

import argparse
import os
import sys
import hashlib
from collections import defaultdict
from typing import Dict


CHUNK_SIZE = 4096
 

def find_duplicates(path: str) -> Dict:
    """Find duplicate files in provided folder

    Returns:
        dict of duplicate filenames to corresponding hash
    """
    hashes = set()
    duplicates = defaultdict(list)

    for entry in os.scandir(path):
        if entry.is_file():
            file_path = os.path.join(path, entry.name)

            file_hash = hashfile(file_path)

            if file_hash in hashes:
                duplicates[file_hash].append(file_path)
            else:
                hashes.add(file_hash)

    return duplicates
 
 
def hashfile(fname: str):
    """Calculate hash of a file"""
    hash_md5 = hashlib.md5()

    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()
 
 
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find duplicate files in a folder')
    parser.add_argument('folder', type=str,
                        help='folder in which duplicate files should be performed')

    args = parser.parse_args()
    folder = args.folder

    if os.path.exists(folder):
        duplicates = find_duplicates(folder)

        if duplicates:
            print(duplicates)
        else:
            print("No duplicate files found in {}".format(folder))

    else:
        sys.exit('Invalid folder provided')
    