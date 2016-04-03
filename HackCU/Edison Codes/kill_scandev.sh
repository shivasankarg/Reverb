#!/usr/bin/bash

ps>process.txt
grep -rw '/home/root/process.txt' -e 'python /home/root/bluez-5.24/test/./test-discovery'>pid.txt
pin=$(awk '{print $1}' pid.txt)
#echo $pin
kill $pin
rm -rf process.txt
rm -rf pid.txt
