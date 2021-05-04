# basic functions for helping to build an HTML page

import re
import form

def header (title):
        lines = [
                '<HTML><HEAD><TITLE>%s</TITLE></HEAD><BODY>' % title,
                '<H3>%s</H3>' % title,
                ]
        return '\n'.join(lines)

def footer ():
        lines = [
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>',
            '<link rel="stylesheet" href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" />',
            '<script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>',
            '<script>',
            '''$(document).ready( function () {
                $("#results").DataTable( {paging : false} );
                } );''',
            '</script>',
            '</BODY></HTML>'
            ]
        return '\n'.join(lines)

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
        
        if 'file' in parms:
            lines.append('<br/>')
            lines.append('Searching in: %s' % parms['file'])
            
        if 'years' in parms:
            lines.append('<br/>')
            lines.append('Restricted to only show years: %s' % parms['years'])
            
        lines.append('<p/>')
        lines.append('</DIV></DIV>')

        return '\n'.join(lines)

def summaryLine(resultCount, elapsed, parms):
        lines = [
            '<DIV>',
            '<B>You found %s results in %0.3f seconds.</B> ' % (resultCount, elapsed),
            '''(<span class="shown0 shown blue" onClick="toggle('0')">show QF</span><span class="hidden0 hidden blue" onClick="toggle('0')">hide QF</span>)''' ,
            '''<div id="matches0" class="hidden0 hidden"><p/>''',
            form.buildForm(parms),
            '</div>',
            '<p/>',
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
            return '%s%s%s' % (d[2], d[0], d[1])

        return str(x).zfill(6)
    
def matchesCell(trNum, matches):
        # builds the contents of the cell for matches for a single TR
        
        out = [
            '''<span style="display:none">%d</span>%d (<span class="shown%d shown blue" onClick="toggle('%d')">show</span><span class="hidden%d hidden blue" onClick="toggle('%d')">hide</span>)''' % (
                len(matches), len(matches), trNum, trNum, trNum, trNum),
            '''<div id="matches%d" class="hidden%d hidden"><ul>''' % (trNum, trNum),
            ]
        
        for match in matches:
            out.append('<li>%s</li>' % match.replace('<', '&lt;').replace('>', '&gt;'))
        
        out.append('</ul></div>')
        return '\n'.join(out)
        
def resultsTable(results):
        out = [
                '''
                <script>
                function toggle(trNum) {
                    $('#matchesColumn').css( { 'width' : '40%' } );
                    var set1 = '.shown' + trNum;
                    var set2 = '.hidden' + trNum;
                    if ($(set1).hasClass('shown')) {
                        $(set1).removeClass('shown');
                        $(set1).addClass('hidden');
                        $(set2).removeClass('hidden');
                        $(set2).addClass('shown');
                        }
                    else {
                        $(set2).removeClass('shown');
                        $(set2).addClass('hidden');
                        $(set1).removeClass('hidden');
                        $(set1).addClass('shown');
                    }
                }
                </script>
                ''',
                '<style>',
                '.hidden { display: none } ',
                '.shown { display: inline } ',
                '.blue { color: blue } '
                '#results { border-collapse: collapse; }',
                '#results tr th { text-align: center; font-weight: bold; border: 1px solid black; border-collapse: collapse; padding: 3px; }',
                '#results tr td { text-align: left; border: 1px solid black; border-collapse: collapse; padding: 3px; }',
                '#results tr:nth-child(even) { background-color: #f3f3f3; }',
                '.wide { width: 25%; }',
                '</style>',
                '<table id="results">',
                '<thead>',
                '<tr>',
                '<th>TR #</th><th>Status</th><th>Created</th><th>Last Modified</th><th>Title</th><th id="matchesColumn">Matching Lines</th>',
                '</tr>',
                '</thead><tbody>'
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
                out.append('<td>%s</td>' % matchesCell(row['TR #'], row['lines']))
                out.append('</tr>')
        out.append('</tbody></table>')
        return '\n'.join(out)

def searchAgain():
        return '''<div style="padding-top: 10px"><button onClick="window.location.href='index.cgi';">Search Again</button></div>'''