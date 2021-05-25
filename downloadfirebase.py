# Opens files in directory, outputs firebase URLs to a file, downloads them, and replaces the links with a link to the new files.

import re
import glob
import os
import requests
import calendar
import time

# vaultDir = '/Users/nic/Dropbox/DownloadMyBrain/dmb-obsidian'
vaultDir = '/Users/nic/Downloads/temp'

firebaseUrl = 'none'
fullRead = 'none'
fileFullPath = ''
fullTempFilePath = ''
i = 0
ext = '.png'

for subdir, dirs, files in os.walk(vaultDir):
    for file in files:
        # Open file in directory
        fileFullPath = os.path.join(subdir,file)
        fhand = open(fileFullPath, errors='ignore')
        for line in fhand:
            # Save the firebase link
            if 'firebase' in line:
                try:
                    # If it's a PDF, it will be in the format {{pdf: link}}
                    if '{{pdf:' in line:
                        link = re.search(r'https://firebase(.*)\?alt(.*)\}', line)
                    else:
                        link = re.search(r'https://firebase(.*)\?alt(.*)\)', line)
                    firebaseUrl = 'https://firebase' + link.group(1) # https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FDownloadMyBrain%2FLy4Wel-rjk.png
                    firebaseReplace = link.group(0)[:-1] # https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FDownloadMyBrain%2FLy4Wel-rjk.png?alt=media&token=0fbafc8f-0a47-4720-9e68-88f70803ced6
                    # Download the file locally
                    r = requests.get(firebaseUrl)
                    timestamp = calendar.timegm(time.gmtime())
                    # Get file extension of file. Ex: .png; .jpeg
                    reg = re.search(r'(.*)\.(.+)', firebaseUrl[-5:]) # a.png / .jpeg
                    ext = '.' + reg.group(2) # .jpeg
                    # Create new local file out of downloaded firebase file
                    newFilePath = 'assets/' + str(timestamp) + '_' + str(i) + ext
                    print(firebaseReplace + '>>>' + newFilePath)
                    with open(vaultDir + '/' + newFilePath,'wb') as output_file:
                        output_file.write(r.content)
                except AttributeError: # This is to prevent the AttributeError exception when no matches are returned
                    continue
                # Save Markdown file with new local file link as a temp file
                # If there is already a temp version of a file, open that.
                fullTempFilePath = vaultDir + '/temp_' + file
                if os.path.exists(fullTempFilePath):
                    fullRead = open(fullTempFilePath, errors='ignore')
                else:
                    fullRead = open(fileFullPath, errors='ignore')
                data = fullRead.read()
                data = data.replace(firebaseReplace,newFilePath)
                with open(fullTempFilePath,'wt') as temp_file:
                    temp_file.write(data)
                    i = i + 1
                if os.path.exists(fullTempFilePath):
                    path = os.replace(fullTempFilePath,fileFullPath)
                # fullRead.close()
                # time.sleep(1)
        # Close file
        fhand.close()
