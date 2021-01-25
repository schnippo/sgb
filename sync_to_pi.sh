#!/bin/bash
while true; do
        sleep 5
        echo "new scan"
        rsync -avz --progress --exclude /home/jonas/git/ssgb/.git /home/jonas/git/ssgb/ pi@192.168.1.226:/home/pi/git/ssgb/
        echo "scan complete, waiting 5s"
done
