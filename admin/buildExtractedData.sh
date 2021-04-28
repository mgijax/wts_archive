#!/bin/sh

# Walk through the single file produced by buildCombinedFile.sh and pull out data needed for summary
# display.  (actual work done by associated python script)

. ../Configuration

if [ "${WTS_ARCHIVE_PATH}" == "" ]; then
        echo "Error: Missing WTS_ARCHIVE_PATH - check Configuration file"
        exit 1
fi

if [ -e ${WTS_ARCHIVE_PATH}noTags.txt ]; then
        echo "Error: Missing ${WTS_ARCHIVE_PATH}noTags.txt - run buildNoTags.sh"
        exit 1
fi

echo "Building extractedData.txt..."
extractSummaryData.py ${WTS_ARCHIVE_PATH}

LINE_COUNT=`wc -l ${WTS_ARCHIVE_PATH}extractedData.txt | awk '{print $1}'`
echo "- Built ${WTS_ARCHIVE_PATH}extractedData.txt with ${LINE_COUNT} lines"
