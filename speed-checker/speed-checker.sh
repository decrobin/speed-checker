#!/bin/bash
DATE=`date +%Y/%m/%d-%H:%M:%S`
logfile="/usr/src/speed-checker/speed.log"

timestamped () {
     #  Get time, then --simple in one line, finally combine into CSV format.
     epoch="$( date '+%Y-%m-%d, %H:%M' )" 
     
     speeds="$( echo $( /usr/local/bin/speedtest-cli --simple | sed -e 's/^.*: //' -e 's/ .*s$/, /' ))"
     #      ^on a single line: ping, download, upload speeds -- given output:
     #                   Ping: 22.602 ms
     #                   Download: 0.62 Mbit/s
     #                   Upload: 0.25 Mbit/s
     if [[ $speeds == *"error"* ]]
     then
        speeds="-1, -1, -1,"
     fi

     echo "$epoch, $speeds" |  sed -e 's/,$//'
     #  Sample result:  "2015-03-13, 19:25, 22.602, 0.62, 0.25"
}

output=$(timestamped)

IFS=', ' read -ra RESULT <<< "$output"
sqlcommand="INSERT INTO speed_results (date, time, ping, download, upload) VALUES ('${RESULT[0]}', '${RESULT[1]}', '${RESULT[2]}', '${RESULT[3]}', '${RESULT[4]}');"

echo "psql -h postgres -U speed -d speed -c \"${sqlcommand}\""
psql -h postgres -U speed -d speed -c "${sqlcommand}"

# timestamped >> $logfile && cat $logfile