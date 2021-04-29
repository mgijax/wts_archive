# actually conduct searches of the WTS Archive, consolidate, and return results

import debug
import subprocess

###--- globals ---###

searchFile = None                       # path to file for searching
lookupFile = None                       # path to lookup up data for individual TRs

###--- functions ---###

def initialize(search, lookup):
        # initialize this module by providing the path to the search file and the lookup file

        global searchFile, lookupFile

        searchFile = search
        lookupFile = lookup
        return

def stripEmptyLines(myList):
        while '' in myList:
                myList.remove('')
        return myList

def grep(phrase, file, flags=''):
        # execute a grep for the given phrase against the given file, with given flags for grep.
        # return (return code, stdout, stderr)

        commandLine = [ 'grep' ]
        if flags:
                commandLine.append(flags)
        commandLine = commandLine + [ phrase, file ]

        proc = subprocess.Popen(commandLine, 2500000, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = ''
        err = ''
        while (proc.returncode == None):
                o, e = proc.communicate(2)
                out = out + o.decode(errors='ignore')
                err = err + e.decode(errors='ignore')
        returnCode = proc.returncode
        return returnCode, stripEmptyLines(out.split('\n')), stripEmptyLines(err.split('\n'))
        
def search(parms):
        # search for results based on the given parameters

        global ids

        if (searchFile == None) or (lookupFile == None):
                raise Exception('searcher.py module needs to be initialized')

        # fire off the searches, then wait for them to finish

        out = []
        err = []

        phrases = [ 'phrase1', 'phrase2', 'phrase3', 'phrase4' ]
        for phrase in phrases:
                if (phrase in parms) and (parms[phrase].strip() != ''):
                        r, o, e = grep(parms[phrase], searchFile, '-i')
                        out = out + o
                        err = err + e
        return out
