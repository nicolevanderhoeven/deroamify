import re
import os

def convert_todo(match):
    if match[1] == "x" or match[1] == "X":
        return "DONE"
    else:
        return "TODO"

def convert_numbers(match):
    contents = match[0].replace(match[2], "- ")
    contents = contents + "\n" + match[1] + "logseq.order-list-type:: number"
    return contents

# insert file path to your vault here
path = '../../'

# Convert date format in file content

for root, dirs, files in os.walk(path):
    # only keep files end with `.md`
    files = [f for f in files if re.match(r'.*\.md', f)]

    for f in files:
        fullpath = (os.path.join(root, f))
        with open(fullpath, 'r') as f:  # opens each .md file
            contents = f.read()  # reads the contents
            # substitutes dates with the format [ ] or [x]
            new_contents = re.sub(
                r'\[([ xX])\]',
                convert_todo,
                contents,
                flags=re.M)

            new_contents = re.sub(
                r'([ ]*)([\d]+.) (DONE|TODO).*',
                convert_numbers,
                new_contents,
                flags=re.M)

        with open(fullpath, 'w') as f:
            # writes the files with the new substitutions
            f.write(new_contents)
