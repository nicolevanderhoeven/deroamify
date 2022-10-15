# Opens files in directory, outputs firebase URLs to a file, downloads them, and replaces the links with a link to the new files.
# To use, replace PATH in the variable vaultDir with your vault's root directory.
# This automatically puts filenames in /assets - change the newFilePath variable if you want to change this

import re
import glob
import os
import requests
import calendar
import time
from io import BytesIO
import shutil

vaultDir = '/Users/nic/Desktop/test2021'

firebaseShort = 'none'
fullRead = 'none'
fileFullPath = ''
fullTempFilePath = ''
i = 0
ext = ''

# Walk through all files in all directories within the specified vault directory
for subdir, dirs, files in os.walk(vaultDir):
    for file in files:
        # Open file in directory
        fileFullPath = os.path.join(subdir,file)
        fhand = open(fileFullPath, errors='ignore')
        for line in fhand:
            # Download the Firebase file and save it in the assets folder
            if 'firebasestorage' in line:
                try:
                    # If it's a PDF, it will be in the format {{pdf: link}}
                    if '{{pdf:' in line:
                        link = re.search(r'https://firebasestorage(.*)\?alt(.*)\}', line)
                    else:
                        link = re.search(r'https://firebasestorage(.*)\?alt(.*)\)', line)
                    firebaseShort = 'https://firebasestorage' + link.group(1) # https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FDownloadMyBrain%2FLy4Wel-rjk.png
                    firebaseUrl = link.group(0)[:-1] # https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FDownloadMyBrain%2FLy4Wel-rjk.png?alt=media&token=0fbafc8f-0a47-4720-9e68-88f70803ced6
                    # Download the file locally
                    r = requests.get(firebaseUrl)
                    timestamp = calendar.timegm(time.gmtime())
                    # Get file extension of file. Ex: .png; .jpeg
                    reg = re.search(r'(.*)\.(.+)', firebaseShort[-5:]) # a.png / .jpeg
                    ext = '.' + reg.group(2) # .jpeg
                    # Create assets folder if it doesn't exist
                    if not os.path.exists(vaultDir + '/assets'):
                        os.makedirs(vaultDir + '/assets')
                    # Create new local file out of downloaded firebase file
                    newFilePath = 'assets/' + str(timestamp) + '_' + str(i) + ext
                    # print(firebaseUrl + '>>>' + newFilePath)
                    with open(vaultDir + '/' + newFilePath,'wb') as output_file:
                        shutil.copyfileobj(BytesIO(r.content), output_file)
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
                data = data.replace(firebaseUrl,newFilePath)
                with open(fullTempFilePath,'wt') as temp_file:
                    temp_file.write(data)
                    i = i + 1
                if os.path.exists(fullTempFilePath):
                    path = os.replace(fullTempFilePath,fileFullPath)
                fullRead.close()
        # Close file
        fhand.close()
