import re
import os
from dateutil.parser import parse

path = 'PATH' #insert file path to your vault here

### Convert date format in file content

for root, dirs, files in os.walk(path):
    files = [f for f in files if re.match(r'.*\.md', f)] # only keep files end with `.md`

    #TODO: could better ignore all dirs with `.` like `.git`

    for f in files:
        fullpath = (os.path.join(root, f))
        with open(fullpath, 'r') as f: #opens each .md file
            contents = f.read() #reads the contents
            #substitutes dates with the format [[April 20th, 2020]] for [[2020-04-20]]
            new_contents = re.sub(r'(?<=\[)[\w]+\s\d{1,2}\w{1,2},\s\d{4}(?=\])',
                                  lambda x: str(parse(x.group(0), ignoretz=True)).split(" ")[0], contents, flags=re.M)
        with open(fullpath, 'w') as f:
            f.write(new_contents) #writes the files with the new substitutions

### Convert daily notes names

for root, dirs, files in os.walk(path):
    files = [f for f in files if re.match(r'[\w]+\s\d{1,2}\w{1,2},\s\d{4}\.md', f)]
    for f in files:
        fullpath = (os.path.join(root, f))
        new_fullpath = re.sub(r'[\w]+\s\d{1,2}\w{1,2},\s\d{4}',
                                  lambda x: str(parse(x.group(0), ignoretz=True)).split(" ")[0], fullpath, flags=re.M)
        os.rename(fullpath, new_fullpath)
