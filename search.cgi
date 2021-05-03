#!./python

# Receives parameters coming in from the query form, executes searches against the WTS archives, 
# formats the results for the user, etc.

import sys
if './lib/python' not in sys.path:
        sys.path.insert(0, './lib/python')
if '/usr/local/mgi/live/lib/python' not in sys.path:
        sys.path.insert(0, '/usr/local/mgi/live/lib/python')

import CGI
import page
import form
import searcher
import traceback
import os
import sys
import debug
import time

###--- classes ---###

class SearchResultsCGI (CGI.CGI):
        # receives parameters, contucts a search of the WTS archive, formats results for the user

        def initialize(self, parms):
                try:
                        returncode, stdout, stderr = searcher.grep('WTS_ARCHIVE_PATH', 'Configuration', '-h')
                        dir = None

                        for line in stdout:
                                line = line.strip()
                                if line.startswith('WTS_ARCHIVE_PATH'):
                                       dir = line.split('=')[1]

                        if dir == None:
                                raise Exception('Missing config parameter: WTS_ARCHIVE_PATH')

                        searchFile = dir + 'noTags.txt'
                        lookupFile = dir + 'extractedData.txt'
                        titleFile = dir + 'titleData.txt'

                        searcher.initialize(searchFile, lookupFile, titleFile)
                except Exception as e:
                        self.reportError(e)
                        return False
                return True

        def main(self):
                parms = self.get_parms()
                try:
                        if not self.initialize(parms):
                                return

                        start = time.time()
                        results, errors = searcher.search(parms)
                        elapsed = time.time() - start

                        lines = [
                                page.header('WTS Archive : Search'),
                                page.youSearchedFor(parms),
                                page.summaryLine(len(results), elapsed),
                                page.resultsTable(results),
                                page.searchAgain(),
                                page.footer()
                                ]
                        print('\n'.join(lines))
                except Exception as e:
                        self.reportError(e)

        def reportError(self, e):
                tb = '<br/>'.join(traceback.format_exception(None, e, e.__traceback__))
                lines = [
                        page.header('WTS Archive : Search Error'),
                        'An error occurred:<br/>',
                        '<B><I>%s</I></B>' % tb,
                        page.footer(),
                        ]
                print('\n'.join(lines))

###--- main program ---###

qf = SearchResultsCGI()
qf.go()
