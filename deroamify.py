# Takes exported Roam input and turns it into a better format for publishing.
# Output is still Markdown, but it's one that doesn't support backlinks.
# Good for traditional blogs.
# Run from a directory with a source .md file.
# Pipe output to a new file, i.e., output.md

import re
import glob
try:
    #filename = glob.glob('*.md')
    #fhand = open(filename[0])
    fhand = open('input.md')
except:
    print('File cannot be opened:', filename)
    exit()

foundCodeBlock = 0

for line in fhand:
    # Turn backlinks into plain text
    line = line.replace('[[', '')
    line = line.replace(']]', '')

    # Remove double block references (block reference of a block that contains a block reference), exported from Roam with "" "".
    # Remove one line return (print adds another).
    # Removes bullet points (-).
    line = line.rstrip('""\n')
    previousLine = line
    line = line.lstrip('- ""')

    #If the line is not one that's part of a code, handle normally.
    if foundCodeBlock == 0:
        # Handle blockquotes
        if line.startswith('>'):
            line = line + '\n'
        # Handle first line of code blocks (can have bullets or leading spaces)
        if line.startswith('```'):
            foundCodeBlock = 1
    else:
        # If the line is in the middle of a code block, don't modify it (these don't have weird characters)
        line = previousLine
        # If the line is the end of a code block, add a line return before and after the ending backticks.
        if line.endswith('```'):
            line = line.replace('```', '\n```\n')
            foundCodeBlock = 0
    print(line)
