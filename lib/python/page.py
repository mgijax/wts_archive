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

        lines.append(op.join(words) + '<p/>')
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
        for row in results:
                out.append('<tr>')
                out.append('<td>TR%s</td>' % row['TR #']),
                out.append('<td>%s</td>' % row['status']),
                out.append('<td>%s</td>' % row['created date']),
                out.append('<td>%s</td>' % row['modified date']),
                out.append('<td>%s</td>' % row['title']),
                out.append('</tr>')
        out.append('</table>')
        return '\n'.join(out)
