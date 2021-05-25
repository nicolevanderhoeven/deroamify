# Prints filenames that have colons in them

import os
import re

vaultDir = '/Users/nic/Dropbox/DownloadMyBrain/dmb-obsidian/'
files = os.listdir(vaultDir)

for file in files:
    # open file
    try:
        fhand = open(vaultDir + file)
        # print('Opened', file)
    except:
        print('File cannot be opened:', file)
    # Print any lines in file that have a colon
    for line in fhand:
        if re.match("r'\[\[(.+)\]\]",line):
            print(line)
