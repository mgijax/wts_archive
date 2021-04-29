# query form object (fields / values)

###--- functions ---###

def pickList(parms, fieldname, values, tooltip = ''):
        # generate a pick-list for the given parameters

        lines = [
                '<SELECT NAME="%s" TITLE="%s">' % (fieldname, tooltip),
                ]

        selectedValue = None
        if fieldname in parms:
                selectedValue = parms[fieldname]

        for value in values:
                flag = ''
                if value == selectedValue:
                        flag = ' SELECTED'
                lines.append('<OPTION VALUE="%s"%s>%s</OPTION>' % (value, flag, value))

        lines.append('</SELECT>')
        return '\n'.join(lines)

def textField(parms, fieldname, size = 40, tooltip = '', placeholder=''):
        # generate a text input field for the given parameters

        line = '<INPUT NAME="%s" TYPE="text" SIZE="%s" VALUE="%s" PLACEHOLDER="%s" TITLE="%s">'
        value = ''
        if fieldname in parms:
                value = parms['fieldname']

        return line % (fieldname, size, value, placeholder, tooltip)

def checkbox(parms, fieldname, value, tooltip = ''):
        # generate a checkbox input field for the given parameters

        line = '<INPUT NAME="%s" TYPE="checkbox" VALUE="%s" TITLE="%s"%s>'
        flag = ''
        if fieldname in parms:
                flag = 'CHECKED'
        return line % (fieldname, value, tooltip, flag)

def submitButton(text):
        # generate a submit button with the given text on it

        return '<INPUT TYPE="submit" VALUE="%s">' % text

def resetButton(text):
        # generate a reset button with the given text on it

        return '<INPUT TYPE="reset" VALUE="%s">' % text

def buildForm(parms):
        # build and return the HTML code for the query form, pre-filling any fields specified in 'parms'

        lines = [ 
                '<FORM ACTION="./search.cgi" METHOD="get">',
                'Show TRs containing ',
                pickList(parms, 'anyAll', [ 'all', 'any' ],
                        '"all" requires matches of all specified search strings, ' + \
                        'while "any" requires that at least one of them match.'),
                'of the following words or phrases:',
                '<p/>',

                '<div style="left-margin: 30px;">',
                textField(parms, 'phrase1', 40, 'Specify a word or phrase to match'),
                '<br/>',
                textField(parms, 'phrase2', 40, 'Specify another word or phrase to match', '(optional)'),
                '<br/>',
                textField(parms, 'phrase3', 40, 'Specify another word or phrase to match', '(optional)'),
                '<br/>',
                textField(parms, 'phrase4', 40, 'Specify another word or phrase to match', '(optional)'),
                '<p/>',

                'Restrict by year created: (e.g.- "< 2015" or "> 2015" or "2015-2018" or "2015")',
                '<p/>',
                textField(parms, 'years', 40, 'Only show TRs created in the specified year(s)', '(optional)'),
                '<br/>',

                submitButton('Search'),
                resetButton('Reset'),

                '</div>'
                ]

        lines.append('</FORM>')

        return '\n'.join(lines)
