#!/bin/sh

# Walk through the single file produced by buildCombinedFile.sh and pull out data needed for summary
# display.  (actual work done by associated python script)

. ../Configuration

if [ "${WTS_ARCHIVE_PATH}" == "" ]; then
        echo "Error: Missing WTS_ARCHIVE_PATH - check Configuration file"
        exit 1
fi

INPUT_FILE=${WTS_ARCHIVE_PATH}noTags.txt
OUTPUT_FILE=${WTS_ARCHIVE_PATH}extractedData.txt

if [ ! -e ${INPUT_FILE} ]; then
        echo "Error: Missing ${INPUT_FILE} - run buildNoTags.sh"
        exit 1
fi

if [ -e ${OUTPUT_FILE} ]; then
        echo "Removing previous extractedData.txt..."
        rm ${OUTPUT_FILE}
fi

echo "Building extractedData.txt..."
cat ${INPUT_FILE} | buildExtractedData.py > ${OUTPUT_FILE}

LINE_COUNT=`wc -l ${OUTPUT_FILE} | awk '{print $1}'`
echo "- Built ${OUTPUT_FILE} with ${LINE_COUNT} lines"
