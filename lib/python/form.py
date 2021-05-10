# query form object (fields / values)

import math

###--- globals ---###

currentWtsAreas = [ 'backend/pwi', 'backend/load', 'backend/data_cleanup', 'backend/custom_sql', 'backend/nomen', 'backend/public_reports',
            'backend/qc_reports', 'dbAdmin', 'frontend/wi_pub', 'imsr', 'misc', 'new_hire', 'user_support', 'unknown' ]

oldWtsAreas = [ 'mouseBlast', 'ratpages', 'komp', 'iws', 'seInfrastructure', 'webAdmin', 'searchTool', 'wi-prod', 'dumps', 'mgs',
            'mailingLists', 'faq', 'wi', 'mtb', 'admin', 'biomart', 'dataMigration', 'mgihome', 'homepages', 'seAdmin', 'ccr',
            'sysAdmin-Mac', 'EIPerms', 'gen', 'sysAdmin-Unix', 'sysAdmin-PC', 'sysAdmin-Misc', 'schema', 'wts', ]

currentWtsTypes = [ 'dbAdmin', 'misc', 'seAdmin', 'swEnhance', 'swFix', 'swNew', 'swRelease', 'unknown', 'userDocEnhance', 'userDocFix',
            'userDocNew' ]

oldWtsTypes = [ 'bigThing', 'configMgmt', 'curatorial', 'dataFiles', 'dataFix', 'dbDesign', 'policy', 'projectGroup',
            'sysAdmin', 'webAdmin', ]

###--- functions ---###

def helpTable(options1, options2, heading1, heading2, defaultClass=''):
        # generate a help table for the two sets of options with the two headings
        
        half1 = math.ceil(len(options1) / 2)
        leftHalf1 = options1[:half1]
        rightHalf1 = options1[half1:]

        half2 = math.ceil(len(options2) / 2)
        leftHalf2 = options2[:half2]
        rightHalf2 = options2[half2:]
        
        tbl = [
            '<style>',
            '.helpTable { border-collapse: collapse; }',
            '.head { background-color: lightgray; text-align: center; font-weight: bold; border: 1px solid black; }',
            '.cell { text-align: center; border: 1px solid black; vertical-align: top; }',
            '</style>',
            '<table class="helpTable %s">' % defaultClass,
            '<tbody>',
            ]
        
        tbl.append('<tr><td class="head" colspan="2">%s</td>' % heading1)
        tbl.append('<td class="head" colspan="2">%s</td></tr>' % heading2)

        tbl.append('<tr>')
        tbl.append('<td class="cell">%s</td>' % '<br/>'.join(leftHalf1))
        tbl.append('<td class="cell">%s</td>' % '<br/>'.join(rightHalf1))
        tbl.append('<td class="celL">%s</td>' % '<br/>'.join(leftHalf2))
        tbl.append('<td class="cell">%s</td>' % '<br/>'.join(rightHalf2))
        tbl.append('</tr>')

        tbl.append('</tbody></table>')
        return '\n'.join(tbl)
   
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
                value = parms[fieldname]

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

        js = '''<script>
            function clearForm() {
                $('[name=phrase1]')[0].value=null;
                $('[name=phrase2]')[0].value=null;
                $('[name=phrase3]')[0].value=null;
                $('[name=phrase4]')[0].value=null;
                $('[name=years]')[0].value=null;
                document.getElementsByName('file')[0].selectedIndex = 0;
                document.getElementsByName('anyAll')[0].selectedIndex = 0;
            }
            </script>
            '''
        return '%s <INPUT TYPE="button" VALUE="%s" onClick="clearForm()">' % (js, text)

def buildForm(parms):
        # build and return the HTML code for the query form, pre-filling any fields specified in 'parms'

        areaString = ', '.join(currentWtsAreas)
        typeString = ', '.join(currentWtsTypes)
        
        lines = [ 
                '''<script>
                function hideShow(i) {
                    var set1 = '.helpShown' + i;
                    var set2 = '.helpHidden' + i;
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
                </script>''',
                '<style>',
                '.wrapper { margin-bottom: 8px; }',
                '.hidden { display: none } ',
                '.shown { display: inline } ',
                '.blue { color: blue } '
                '</style>',
                '<FORM ACTION="./search.cgi" METHOD="get">',
                'Show TRs containing ',
                pickList(parms, 'anyAll', [ 'all', 'any' ],
                        '"all" requires matches of all specified search strings, ' + \
                        'while "any" requires that at least one of them match.'),
                'of the following words or phrases:',
                '<p/>',

                '<div class="wrapper">',
                '<div style="margin-left: 30px; float:left; padding-right: 30px;">',
                textField(parms, 'phrase1', 40, 'Specify a word or phrase to match'),
                '<br/>',
                textField(parms, 'phrase2', 40, 'Specify another word or phrase to match', '(optional)'),
                '<br/>',
                textField(parms, 'phrase3', 40, 'Specify another word or phrase to match', '(optional)'),
                '<br/>',
                textField(parms, 'phrase4', 40, 'Specify another word or phrase to match', '(optional)'),
                '<p/>',
                '</div>',
                
                '<div style="display: inline;">',
                'Need suggestions from the old WTS search options?<br/>',
                '<span class="helpShown0 shown" onClick="hideShow(0)">(<span class="blue">show areas</span>)</span>',
                '<span class="helpHidden0 hidden" onClick="hideShow(0)">(<span class="blue">hide areas</span>)</span>',
                '<span class="helpShown1 shown" onClick="hideShow(1)">(<span class="blue">show types</span>)</span>',
                '<span class="helpHidden1 hidden" onClick="hideShow(1)">(<span class="blue">hide types</span>)</span>',
                '<div style="clear:both"></div>',
                helpTable(currentWtsAreas, oldWtsAreas, 'Newer Areas', 'Older Areas', 'helpHidden0 hidden'),
                helpTable(currentWtsTypes, oldWtsTypes, 'Newer Types', 'Older Types', 'helpHidden1 hidden'),
                '</div>',
                
                '</div><!-- wrapper -->',

                '<div style="clear:both">',
                'Search through: ',
                pickList(parms, 'file', [ 'full TRs', 'only TR # and Titles' ],
                        '"full TRs" will look in all fields of the TRs, while ' + \
                        'while "only TR # and Titles" will only examine the Title fields.'),
                '<p/>',

                'Restrict by year created: (e.g.- "< 2015" or "> 2015" or "2015-2018" or "2015")',
                '<p/>',
                '</div>',
                '<div style="margin-left: 30px;">',
                textField(parms, 'years', 40, 'Only show TRs created in the specified year(s)', '(optional)'),
                '</div>',
                '<br/>',

                submitButton('Search'),
                resetButton('Reset'),

                '</div>'
                ]

        lines.append('</FORM>')

        return '\n'.join(lines)
