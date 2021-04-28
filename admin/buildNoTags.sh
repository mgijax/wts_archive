#!/bin/sh

# Build a single file that combines all the archived WTS TR files into a single one, prepends the
# TR number to each line, and strips out all HTML tags.

. ../Configuration

if [ "${WTS_ARCHIVE_PATH}" == "" ]; then
        echo "Error: Missing WTS_ARCHIVE_PATH - check Configuration file"
        exit 1
fi

cd ${WTS_ARCHIVE_PATH}

if [ -e noTags.txt ]; then
        echo "Removing previous noTags.txt..."
        rm noTags.txt
fi

echo "Building noTags.txt..."
for file in `ls */TR*html`; do
        cat ${file} | sed 's/<[^>]*>//g ; /^$/d' | sed 's@^@'"${file}"' @' >> noTags.txt
done

LINE_COUNT=`wc -l noTags.txt | awk '{print $1}'`
echo "- Built ${WTS_ARCHIVE_PATH}noTags.txt with ${LINE_COUNT} lines"
