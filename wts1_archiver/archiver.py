#
# archiver.py
#
# Archives TR pages. For the specified range of TRs, requests them from 
#    http://wts.informatics.jax.org/searches/tr.detail.cgi
# Then saves the HTML as files in the archive area.
#
# Takes an optional argument which is a CSV file of Jira stories that have "TR" in the title.
# (Generate this file from within Jira.)
# This info is used to insert links from the archived TRs to the associated Jira stories.
#

import sys
import math
import os
from urllib.request import Request, urlopen
from argparse import ArgumentParser
import db
import re

db.set_sqlServer('bhmgidb01.jax.org')
db.set_sqlDatabase('prod')
db.set_sqlUser('mgd_public')
db.set_sqlPassword('mgdpub')

# Need to search replace relative links that look like "tr.details.cgi?TR_Nr=2010" with 
# relative links that look like "../2000/TR2010.html".
href_re = b'<a href="tr.detail.cgi\?TR(_Nr)?=([0-9]+)">'
# Regex to find insertion point for adding WTS2 links.
insert_re = b'<STRONG>Project Definition:</STRONG></A><BR>'
# Archive path pattern
archiveRelUrl = b'../%d/TR%d.html'

# The replacement function to be used. m is a match object containing
# one match of the href_re pattern.
def repl (m) :
    trnum = int(m.group(2))
    parentdir =100*int(trnum/100)
    href = archiveRelUrl % (parentdir,trnum)
    return b'<a href="%s">' % href

url_tmplt = 'http://wts.informatics.jax.org/searches/tr.detail.cgi?TR_Nr=%d'
wts2_tmplt = '<a href="https://mgi-jira.atlassian.net/browse/%s">%s</a>'
trfile_tmplt = 'TR%d.html'
hdr = { "Authorization": "Basic amVyOmplbjY4Yg==" }
not_found = b'WTS2.0: Cant Find Tracking Record'
ARCHIVE_DIR = '/mgi/all/wts_projects/archive'

# (Copied this code from exporter.py. Ugh.)
def getJiraStories (fname) :
    if not fname:
        return {}
    fd = open(fname,'r')
    ikey = -1
    ititle = -1
    tr2jira = {}
    for i,line in enumerate(fd):
        flds = line[:-1].split(",")
        if i == 0:
            ikey = flds.index('Issue key')
            ititle = flds.index('Summary')
        else:
            k = flds[ikey]
            title = flds[ititle]
            m = re.search("TR[: ]*([0-9][0-9]*)", title)
            if m:
                tr = int(m.group(1))
                tr2jira.setdefault(tr,[]).append(k)
    return tr2jira

#
def getOpts () :
    q = '''SELECT min(_tr_key), max(_tr_key) FROM "wts"."wts_trackrec";'''
    minmax = db.sql(q)[0]
    #
    parser = ArgumentParser()
    parser.add_argument(
      "-m", "--minTR",
      default=minmax['min'],
      type=int,
      help="Minimum TR number. Default=%(default)d.")
    parser.add_argument(
      "-M", "--maxTR",
      default=minmax['max'],
      type=int,
      help="Maximum TR number. Default=%(default)d.")
    parser.add_argument(
      "-j", "--jira-stories",
      dest="jiraStories",
      help="File of Jira stories and associated TRs.")
    parser.add_argument(
      "-d", "--directory",
      default=ARCHIVE_DIR,
      help="Output directory. Default=%(default)s")
    return parser.parse_args()

def generateLinkSection (tr_key, tr2stories):
    stories = tr2stories.get(tr_key, [])
    if len(stories) == 0:
        return b''
    links = map(lambda s: wts2_tmplt % (s,s), stories)
    start = '<div style="background-color:#ccc;"><span>See Jira ticket(s): </span>'
    middle = ', '.join(links)
    end = '</div>'
    return str(start+middle+end).encode('utf8')

def archiveTR (tr_key, tr2stories, archive_dir) :
    url = url_tmplt % tr_key
    req = Request(url, headers=hdr)
    fd = urlopen(req)
    page = fd.read()
    #
    page = re.sub(href_re, repl, page, flags = re.I)
    #
    fd.close()
    if page.find(not_found) >= 0:
        # tr not valid
        sys.stdout.write('? ')
        return
    # Insert WTS2 link section
    linkSec = generateLinkSection(tr_key, tr2stories)
    i,j = re.search(insert_re, page, flags = re.M).span()
    page = page[0:j] + linkSec + page[j:]
    #
    intermediateDir = os.path.join(archive_dir, str(100 * math.floor(tr_key / 100)))
    os.makedirs(intermediateDir, exist_ok=True)
    fname = os.path.join(intermediateDir, trfile_tmplt % tr_key)
    ofd = open(fname, 'wb')
    ofd.write(page)
    ofd.close()
    
def main () :
    opts = getOpts()
    tr2stories = getJiraStories(opts.jiraStories)
    #print(tr2stories)
    #sys.exit(0)
    tr_key = opts.minTR
    tr_max_key = opts.maxTR
    while tr_key <= tr_max_key:
        archiveTR(tr_key, tr2stories, opts.directory)
        if tr_key % 50 == 0:
            sys.stdout.write(str(tr_key) + ' ')
            if tr_key % 1000 == 0:
                sys.stdout.write('\n')
            sys.stdout.flush()
        tr_key += 1
    sys.stdout.write('\n')

#
main()
