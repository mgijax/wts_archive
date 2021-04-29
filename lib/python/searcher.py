# actually conduct searches of the WTS Archive, consolidate, and return results

import Dispatcher

###--- globals ---###

dispatcher = Dispatcher.Dispatcher(4)   # max 4 processes at a time
ids = {}                                # maps from search phrase to dispatcher ID
searchFile = None                       # path to file for searching
lookupFile = None                       # path to lookup up data for individual TRs

###--- functions ---###

def initialize(search, lookup):
        # initialize this module by providing the path to the search file and the lookup file

        global searchFile, lookupFile

        searchFile = search
        lookupFile = lookup
        return

def startSearch(phrase):
        # tell the dispatcher to start up a new Linux process and run a grep against the
        # searchFile for the specified phrase

        global ids
        ids[phrase] = dispatcher.schedule("grep -i '%s' %s" % (phrase, searchFile))
        return
        
def search(parms):
        # search for results based on the given parameters

        global ids

        if (searchFile == None) or (lookupFile == None):
                raise Exception('searcher.py module needs to be initialized')

        # fire off the searches, then wait for them to finish

        phrases = [ 'phrase1', 'phrase2', 'phrase3', 'phrase4' ]
        for phrase in phrases:
                if (phrase in parms) and (parms[phrase].strip() != ''):
                        startSearch(parms[phrase])
        dispatcher.wait()

        words = list(ids.keys())
        out = []

        for word in words:
                out.append('<B>word:</B>')
                for line in dispatcher.getStdout(ids[word]):
                        out.append(line)
                out.append('<p/>')

        return out
