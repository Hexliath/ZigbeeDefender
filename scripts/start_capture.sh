#!/bin/bash

cd /app/server/
while true
do
        sleep 20
        ./launch.sh &
        sleep 300
        killall "python" "launch.sh" "tshark" "whsniff"
        echo -e 'Restarting...'
done
