#!/bin/sh
echo Initializing
rfkill block bluetooth
rfkill block wifi
hciconfig hci0 down
rfkill unblock bluetooth
rfkill unblock wifi
hciconfig hci0 up
sh wifi_connect.sh Caesar 123456789
sleep 5
python /home/root/bluez-5.24/test/scandev.py &
sleep 8
sh kill_scandev.sh
grep -r -w "Address:" /home/root/adrs.txt > bd1.txt
awk 'length($0) < 27' bd1.txt > bd2.txt
wc -l bd2.txt > numb.txt
n=$(awk '{print $1}' numb.txt)
rm -rf numb.txt
c=1
n=$(($n+1))
while [ $c -lt $n ]
do
  awk 'FNR == '$c'{print $2}' bd2.txt > bd.txt
  sh conble.sh
  c=$(($c+1))
done
rm -rf bd1.txt
rm -rf bd2.txt
rm -rf bd3.txt
