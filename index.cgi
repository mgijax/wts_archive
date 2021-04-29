#!./python

# Displays the query form for searching WTS archives.  Can pre-fill fields given parameters coming in.

import sys
if '.' not in sys.path:
        sys.path.insert(0, '.')

import Configuration
config = Configuration.get_Configuration('Configuration', 1)

import CGI

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
                print(lines)

###--- main program ---###

form = SearchFormCGI()
form.go()
