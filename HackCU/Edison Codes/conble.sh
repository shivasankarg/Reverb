lin=`cat bd.txt`

devname=`/home/root/bluez-5.24/test/./test-device name $lin` 
echo $devname
ch="HRM1"

if [ "$devname" == "$ch" ]
then
	echo "BMP180"
	#/home/root/bluez-5.24/test/./test-device trusted $lin
	a=`/home/root/bluez-5.24/test/./test-device connect $lin`     #connects to the device (lin)
	if [ $a ]                          #if not connected, variable a will have error values, so it throws the statement "failed connecting"... 
	then
		echo "failed connecting"           #if connected, then variable a will have no value, and runs the test heartrate code
	else
		sleep 3
		python /home/root/bluez-5.24/test/test_1.py -b $lin &  #runs the code in background
		hcitool con
	fi
elif [ "$devname" == "ACCL" ]
then
	echo "$devname"
	#/home/root/bluez-5.24/test/./test-device trusted $lin
	a=`/home/root/bluez-5.24/test/./test-device connect $lin`
	if [ $a ]
	then
		echo "failed to connect"
	else
		/home/root/bluez-5.24/test/././test-cyclingspeed -b $lin &
	fi
fi
