#!/bin/bash
echo 'Updating the date'
DATE=`date +%Y-%m-%d`
head -n -1 /home/askoski/Service-AskOski/scripts/env.sh > /home/askoski/Service-AskOski/scripts/temp.sh
mv /home/askoski/Service-AskOski/scripts/temp.sh /home/askoski/Service-AskOski/scripts/env.sh
dateCommand='export dateUpdated='$DATE
echo $dateCommand >> /home/askoski/Service-AskOski/scripts/env.sh

FILE='/research/UCBDATA/edw_askoski_student_grades.txt'
if [ -f $FILE ]; then
   echo "File $FILE exists."
else
   echo "File $FILE does not exist."
fi

echo 'Hashing and moving files after a delay to make sure files uploaded'
. /home/askoski/Service-AskOski/scripts/env.sh
echo $seedBin
echo $majorsFile
python /home/askoski/Service-AskOski/scripts/refresh/refresh.py

NONE='\033[00m'
GREEN='\033[01;32m'
eval echo '${GREEN}Done with pipeline${NONE}'
