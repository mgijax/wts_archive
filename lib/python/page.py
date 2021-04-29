# basic functions for helping to build an HTML page

def header (title):
        lines = [
                '<HTML><HEAD><TITLE>%s</TITLE></HEAD><BODY>' % title,
                '<H3>%s</H3>' % title,
                ]
        return '\n'.join(lines)

def footer ():
        return '</BODY></HTML>'
