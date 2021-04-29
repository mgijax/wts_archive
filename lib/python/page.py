# basic functions for helping to build an HTML page

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

        lines.append('</DIV></DIV>')

        return '\n'.join(lines)

def resultsTable(results):
        return 'results table'
