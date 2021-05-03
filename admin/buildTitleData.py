#!./python

# Reads from stdin, writes to stdout.
# Expects to receive contents of noTags.txt file on stdin (many lines per TR, with all HTML tags stripped out).
# Assumes all lines for a TR come in consecutively on stdin (not out-of-order).
# Parses to pull out title field needed for searching.  Writes as a tab-delimited file, one line per TR, to stdout.

import sys
import re

###--- regular expressions ---###

# ID is the first thing on each line, coming before the first space. Group 1: ID
idRE = re.compile('^([^ ]+)')

# title comes on a line beginning with the ID, then a space, then the word "Title", then another
# space, followed by the title itself.  Group 1: title
titleRE = re.compile('^[^ ]+ Title (.*)$')

###--- classes ---###

class TR:
        def __init__ (self):
                self.id = None
                self.title = None
                return

        def setID(self, id):
                self.id = id.strip()

        def setTitle(self, title):
                self.title = title.strip()

        def formatted(self):
                return '%s\t%s' % (self.id, self.title)

###--- functions ---###


###--- main program ---###

tr = TR()
input = sys.stdin.buffer

for line in input:
        try:
                line = line.decode('utf-8', errors='ignore')
        except:
                print(line)
                sys.exit(1)

        # If we find a new ID, then we need to write out the data for the old TR (if there is an
        # old one) and start a new TR object.
        match = idRE.match(line)
        if match:
                id = match.group(1)
                if id != tr.id:
                        if tr.id != None:
                                print(tr.formatted())
                        tr = TR()
                        tr.setID(id)

        match = titleRE.match(line)
        if match:
                tr.setTitle(match.group(1)) 

if (tr.id != None):
        print(tr.formatted())
