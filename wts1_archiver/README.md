The cutover from WTS1 to WTS2 occurred on April 12, 2021. 
This directory contains the scripts that were run and the files that were generated and processed on that day.

archiver.py - Generated the HTML page for every TR and wrote it to /mgi/all/wts_projects/archive

exporter.py - Generated the list of active TRs. These were loaded into WTS2 as tickets.

jiraStories.csv - lists all Jira stories (from any project) that contains TR in the title. This file was generated in Jira and exported. Was used as input to archiver.py for inserting links from the archive HTML to relevant Jira tickets.

top10list.tsv - A dump of the old Google spreadsheet containing the PIs' lists of TRs and their priorities. Used as input to exporter.py for setting the PI and sortOrder fields of the imported tickets.

activeTrs.csv - The output of exporter.py. The file of active TRs appropriately mapped and formatted for bulk load into Jira.
