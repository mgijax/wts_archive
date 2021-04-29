#!./python

# Displays the query form for searching WTS archives.  Can pre-fill fields given parameters coming in.

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

###--- classes ---###

class SearchFormCGI (CGI.CGI):
        # builds and displays a search form for the WTS Archive

        def main(self):
                # takes incoming parameters to pre-fill form fields, builds and outputs the page

                parms = self.get_parms()

                lines = [
                        page.header('WTS Archive : Search'),
                        form.buildForm(parms),
                        page.footer(),
                        ]
                print('\n'.join(lines))

###--- main program ---###

qf = SearchFormCGI()
qf.go()
