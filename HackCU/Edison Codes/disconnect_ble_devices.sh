#!/usr/bin/bash

wc -l adrs.txt > numb.txt
n=$(awk '{print $1}' numb.txt)
c=1
n=$(($n+1))
sh kill_heartrate.sh
while [ $c -le $n ]
do
  addr=$(awk 'FNR == '$c'{print}' adrs.txt)
  /home/root/bluez-5.24/test/./test-device disconnect $addr
  c=$(($c+1))
done


