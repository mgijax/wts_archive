# basic functions for helping to build an HTML page

import re

def header (title):
        lines = [
                '<HTML><HEAD><TITLE>%s</TITLE></HEAD><BODY>' % title,
                '<H3>%s</H3>' % title,
                ]
        return '\n'.join(lines)

def footer ():
        return '</BODY></HTML>'

def youSearchedFor(parms):
        lines = [
                '<DIV><B>You searched for:</B><br/>',
                '<DIV STYLE="margin-left: 20px">',
                ]

        op = ' AND '
        if ('anyAll' in parms) and (parms['anyAll'] == 'any'):
                op = ' OR '

        words = []
        phrases = [ 'phrase1', 'phrase2', 'phrase3', 'phrase4' ]
        for phrase in phrases:
                if (phrase in parms) and (parms[phrase].strip() != ''):
                        words.append(parms[phrase]) 

        if len(words) == 0:
                raise Exception('No search phrases were found.  Please go back and try again.')

        lines.append(op.join(words))
        if 'years' in parms:
            lines.append('<br/>')
            lines.append('Restricted to only show years: %s' % parms['years'])

        lines.append('<p/>')
        lines.append('</DIV></DIV>')

        return '\n'.join(lines)

def summaryLine(resultCount, elapsed):
        lines = [
            '<DIV>',
            '<B>You found %s results in %0.3f seconds.</B><p/>' % (resultCount, elapsed),
            '</DIV>',
            ]
        return '\n'.join(lines)

tagRE = re.compile('(<[^>]*>)')
def stripHtmlTags(s):
        match = tagRE.search(s)
        while match:
                s = s.replace(match.group(1), '')
                match = tagRE.search(s)
        return s 

def sortable(x):
        # take a date as mm/dd/yyyy and return it as yyyymmdd for easier sorting as a string (if a date is received)
        # or if not a date, return integer with zeroes padded at left for sorting
        
        y = str(x)
        if y.find('/') >= 0:
            d = y.split('/')
            return '%s%s%s' % (d[2], d[1], d[0])

        return str(x).zfill(6)
    
def resultsTable(results):
        out = [
                '<style>',
                '#results { border-collapse: collapse; }',
                '#results tr th { text-align: center; font-weight: bold; border: 1px solid black; border-collapse: collapse; padding: 3px; }',
                '#results tr td { text-align: left; border: 1px solid black; border-collapse: collapse; padding: 3px; }',
                '#results tr:nth-child(even) { background-color: #f3f3f3; }',
                '</style>',
                '<table id="results">',
                '<tr>',
                '<th>TR #</th><th>Status</th><th>Created</th><th>Last Modified</th><th>Title</th>',
                '</tr>',
                ]

        link = '<a href="http://wts.informatics.jax.org/wts_projects/archive/%s" target="_blank">TR%s</a>'
        for row in results:
                out.append('<tr>')
                out.append('<td><span style="display:none">%s</span>%s</td>' % (sortable(row['TR #']),
                    link % (row['filename'], row['TR #']))),
                out.append('<td>%s</td>' % row['status']),
                out.append('<td><span style="display:none">%s</span>%s</td>' % (sortable(row['created date']), row['created date'])),
                out.append('<td><span style="display:none">%s</span>%s</td>' % (sortable(row['modified date']), row['modified date'])),
                out.append('<td>%s</td>' % row['title']),
                out.append('</tr>')
        out.append('</table>')
        return '\n'.join(out)
