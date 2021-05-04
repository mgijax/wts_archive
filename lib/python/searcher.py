# actually conduct searches of the WTS Archive, consolidate, and return results

import debug
import subprocess
import re

###--- globals ---###

searchFile = None                       # path to file for searching
titleFile = None                        # path to file for searching only titles
lookupFile = None                       # path to lookup up data for individual TRs

# identifies TR number from within filename
trNumRE = re.compile('[0-9]+/TR([0-9]+)\.html')

# identify "less than" year string
ltYearRE = re.compile('^< *([0-9]{4})$')

# identify "greater than" year string
gtYearRE = re.compile('^> *([0-9]{4})$')

# identify "between" year string
betweenYearRE = re.compile('^([0-9]{4}) *- *([0-9]{4})$')

# identify single year string
oneYearRE = re.compile('^([0-9]{4})$')

###--- functions ---###

def initialize(search, lookup, titles):
        # initialize this module by providing the path to the search file, the lookup file,
        # and the title file

        global searchFile, lookupFile, titleFile

        searchFile = search
        lookupFile = lookup
        titleFile = titles
        return

def _stripEmptyLines(myList):
        # remove any empty lines from myList
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
        return returnCode, _stripEmptyLines(out.split('\n')), _stripEmptyLines(err.split('\n'))
        
def _splitLine(matchingLine, separator = ' '):
        # split the matching line into its filename and then the rest of it
        
        parts = matchingLine.strip().split(separator)
        return parts[0], ' '.join(parts[1:])
            
def _rawSearch(parms, fileToSearch):
        # actually execute the searches based on the parameters

        out = []
        err = []

        phrases = [ 'phrase1', 'phrase2', 'phrase3', 'phrase4' ]
        for phrase in phrases:
                if (phrase in parms) and (parms[phrase].strip() != ''):
                        r, o, e = grep(parms[phrase].strip(), fileToSearch, '-i')
                        out.append(o)
                        err = err + e
        return out, err

def _sliceAndDice(out, anyAll, separator = ' '):
        # out is a list of lists, each containing matching lines for one search
        # phrase.  This function slices and dices them to return:
        #  (ordered list of filenames with matches, { filename : matching lines })
        
        matchingLines = {}      # filename : matching lines
        matchingFilenames = []  # has one Set for each search phrase
        
        # split the matches and collect the pieces
        
        for matches in out:
            newSet = set()

            for match in matches:
                filename, matchingLine = _splitLine(match, separator)
                newSet.add(filename)
                
                if filename not in matchingLines:
                    matchingLines[filename] = set()
                matchingLines[filename].add(matchingLine)
                
            matchingFilenames.append(newSet)
        
        # join the match sets appropriately (any / all)
        
        results = matchingFilenames[0]
        for otherSet in matchingFilenames[1:]:
            if anyAll == 'all':
                results = results.intersection(otherSet)
            else:
                results = results.union(otherSet)

        # remove lists of matching lines for filenames that are no longer
        # in the matching set
        
        filenames = list(matchingLines.keys())
        for filename in filenames:
            if filename not in results:
                del matchingLines[filename]
            
        # pull the results out of the set into a list and sort it
        
        asList = list(results)
        asList.sort()
        
        return asList, matchingLines

def _extractTRNum(filename):
        # return the integer TR number out of the given filename
        
        match = trNumRE.match(filename)
        if (match):
            return int(match.group(1))
        raise Exception('Cannot find TR number in: %s' % filename)
        
def _extractData(o):
        # take output from grep (o) and pull out the extracted data into a dictionary (see the
        # _getData() function for fields)
        
        pieces = o.split('\t')
        d = {
            'filename' : pieces[0],
            'TR #' : _extractTRNum(pieces[0]),
            'status' : pieces[1],
            'created date' : pieces[2],
            'modified date' : pieces[3],
            'created year' : pieces[4],
            'title' : pieces[5]
            }
        return d
        
def _splitList (items, n = 12):
    # splits 'items' in a list of sub-lists, each of which has 'n' or fewer items in it

    if len (items) <= n:
        return [ items ]
    else:
        return [ items [:n] ] + _splitList (items [n:], n)
        
def _getData(filenames, parms, fileToSearch):
        # use the lookupFile to get the display attributes for the listed files, returning
        # a list of dictionaries, where each dictionary is for one file and contains these fields:
        #    filename, TR #, status, created date, modified dated, created year, title

        out = []
        for sublist in _splitList(filenames):
            r, o, e = grep('\|'.join(sublist), fileToSearch, '-i')
            if (r != 0) or e:
                raise Exception("Error in looking up data for %s: %s" % (filename, e))
            
            for line in o:
                out.append(_extractData(line))
            
        return out

def _filter(data, parms):
        # filter the given data set down based on any parameters for restricting what is displayed
        
        # short-circuit if no years restriction specified (it's currently the only one)
        if ('years' not in parms) or (parms['years'].strip() == ''):
            return data
        
        years = parms['years'].strip()
        desired = []
        
        match = oneYearRE.match(years)
        if match:
            desired.append(match.group(1))

        if not desired:
            match = ltYearRE.match(years)
            if match:
                for i in range(1995, int(match.group(1))):
                    desired.append(str(i))
            
        if not desired:
            match = gtYearRE.match(years)
            if match:
                for i in range(int(match.group(1)) + 1, 2022):
                    desired.append(str(i))
        
        if not desired:
            match = betweenYearRE.match(years)
            if match:
                for i in range(int(match.group(1)), int(match.group(2)) + 1):
                    desired.append(str(i))
        
        if not desired:
            raise Exception("Cannot recognize year: %s" % years)

        # need to parse the specified years and identify which ones to keep (as strings)
        
        filteredData = []
        
        for row in data:
            if row['created year'] in desired:
                filteredData.append(row)

        return filteredData
        
def search(parms):
        # search for results based on the given parameters

        if (searchFile == None) or (lookupFile == None) or (titleFile == None):
                raise Exception('searcher.py module needs to be initialized')

        lookIn = searchFile
        separator = ' '
        if ('file' in parms) and (parms['file'].strip() == 'only TR # and Titles'):
            lookIn = titleFile
            separator = '\t'
            
        # fire off the searches, then wait for them to finish
        out, err = _rawSearch(parms, lookIn)
        if err:
            return [], err
        
        # determine whether to join them by AND (all) or OR (any)

        anyAll = 'all'
        if 'anyAll' in parms:
            if parms['anyAll'] == 'any':
                anyAll = 'any'

        # join the sets of matches appropriately
        filenames, matchingLines = _sliceAndDice(out, anyAll, separator)
        
        # look up the attributes for the matching TRs
        data = _getData(filenames, parms, lookupFile)
        
        # sort the data by TR number
        data.sort(key=lambda x: x['TR #'])
        
        # add in the matching lines
        for row in data:
            filename = row['filename']
            if filename in matchingLines:
                row['lines'] = matchingLines[filename]
            else:
                row['lines'] = []
                
        return _filter(data, parms), err
