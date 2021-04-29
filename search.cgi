#!./python

# Receives parameters coming in from the query form, executes searches against the WTS archives, 
# formats the results for the user, etc.

import sys
if './lib/python' not in sys.path:
        sys.path.insert(0, './lib/python')
if '/usr/local/mgi/live/lib/python' not in sys.path:
        sys.path.insert(0, '/usr/local/mgi/live/lib/python')

import Configuration
config = Configuration.get_Configuration('Configuration', 1)

import CGI
import page
import form
import searcher
import traceback

###--- classes ---###

class SearchResultsCGI (CGI.CGI):
        # receives parameters, contucts a search of the WTS archive, formats results for the user

        def main(self):
                parms = self.get_parms()
                try:
                        results = searcher.search(parms)

                        lines = [
                                page.header('WTS Archive : Search'),
                                page.youSearchedFor(parms),
                                page.resultsTable(results),
                                page.footer(),
                                ]
                        print('\n'.join(lines))
                except Exception as e:
                        self.reportError(e)

        def reportError(self, e):
                lines = [
                        page.header('WTS Archive : Search Error'),
                        'An error occurred:<br/>',
                        '<B><I>%s</I></B>' % str(e),
                        page.footer(),
                        ]
                print('\n'.join(lines))


###--- main program ---###

qf = SearchResultsCGI()
qf.go()
