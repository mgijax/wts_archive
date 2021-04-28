#!./python

# Reads from stdin, writes to stdout.
# Expects to receive contents of noTags.txt file on stdin (many lines per TR, with all HTML tags stripped out).
# Assumes all lines for a TR come in consecutively on stdin (not out-of-order).
# Parses to pull out various fields needed for display.  Writes as a tab-delimited file, one line per TR, to stdout.

import sys
import re

###--- regular expressions ---###

# ID is the first thing on each line, coming before the first space. Group 1: ID
idRE = re.compile('^([^ ]+)')

# title comes on a line beginning with the ID, then a space, then the word "Title", then another
# space, followed by the title itself.  Group 1: title
titleRE = re.compile('^[^ ]+ Title (.*)$')

# status comes after a line beginning with the ID, a little later having a Priority field, then a
# Status label, followed by the status value, a space, and a hyphen, then space and Date.
statusRE = re.compile('^[^ ]+ Priority.*Status ([^ ]+) - Date')

# The modifiedBy date is found on a line beginning with the ID, then a space, then "TR #", and a 
# little later the label "Modification Date ", followed by a date.
modifiedRE = re.compile('^[^ ]+ TR # .*Modification Date ([^ ]+)')

# The createdBy date is found on the lowest line for the TR that begins with an ID, then has a 
# status, then a space, a hyphen, and a space, then "set by", and a little later "effective"
# followed by a space and a date..
createdRE = re.compile('^[^ ]+ [^ ]+ - set by .* - effective ([0-9/]+)')

# The createdYear can be drawn from the createdBy date once matched by the createdRE regex.
createdYearRE = re.compile('[0-9]+.[0-9]+.([0-9]+)')

###--- classes ---###

class TR:
        def __init__ (self):
                self.id = None
                self.created = None
                self.modified = None
                self.title = None
                self.createdYear = None
                self.status = None
                return

        def setID(self, id):
                self.id = id.strip()

        def setCreated(self, created):
                self.created = created.strip()

        def setModified(self, modified):
                self.modified = modified.strip()

        def setTitle(self, title):
                self.title = title.strip()

        def setYear(self, year):
                self.createdYear = year.strip()

        def setStatus(self, status):
                self.status = status.strip()

        def formatted(self):
                return '%s\t%s\t%s\t%s\t%s\t%s' % (self.id, self.title, self.status, self.created,
                        self.modified, self.createdYear)

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

        match = statusRE.match(line)
        if match:
                tr.setStatus(match.group(1))

        match = modifiedRE.match(line)
        if match:
                tr.setModified(match.group(1))

        match = createdRE.match(line)
        if match:
                tr.setCreated(match.group(1))
                yearMatch = createdYearRE.match(tr.created)
                if yearMatch:
                        tr.setYear(yearMatch.group(1))

if (tr.id != None):
        print(tr.formatted())
