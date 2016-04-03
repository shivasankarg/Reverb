#!/bin/bash
sleep 60

echo Initializing
rfkill block bluetooth
rfkill block wifi
hciconfig hci0 down
rfkill unblock bluetooth
rfkill unblock wifi
hciconfig hci0 up
sh wifi_connect.sh Caesar 123456789
sleep 5
rm -rf adrs.txt
python /home/root/bluez-5.24/test/./test-discovery &
sleep 8
sh kill_scandev.sh
wc -l adrs.txt > numb.txt
n=$(awk '{print $1}' numb.txt)
rm -rf numb.txt
c=1
n=$(($n+1))
while [ $c -le $n ]
do
  awk 'FNR == '$c' {print}' adrs.txt > bd.txt
  sh conble.sh
  c=$(($c+1))
done
#rm -rf bd1.txt
#rm -rf bd2.txt
#rm -rf bd3.txt
