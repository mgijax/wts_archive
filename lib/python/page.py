# basic functions for helping to build an HTML page

def header (title):
        lines = [
                'Content-type: text/html',
                '',
                '<HTML><HEAD><TITLE>%s</TITLE></HEAD><BODY>',
                '<H3>%s</H3>' % title,
                ]
        return '\n'.join(lines)

def footer ():
        return '</BODY></HTML>'