#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals
from __main__ import *
import sys
from time import sleep
import urllib2

'''
Heart Rate Monitor test script
'''

from optparse import OptionParser, make_option
import sys
import dbus
import dbus.service
import dbus.mainloop.glib

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
import bluezutils

count = 0
x = 0
y = 0

BUS_NAME = 'org.bluez'
HEARTRATE_MANAGER_INTERFACE = 'org.bluez.HeartRateManager1'
HEARTRATE_WATCHER_INTERFACE = 'org.bluez.HeartRateWatcher1'
HEARTRATE_INTERFACE = 'org.bluez.HeartRate1'


def sendToThingsSpeak(RH, T):
    baseurl = 'https://api.thingspeak.com/update?api_key=RPXNKWI2H2T6TS2T'
    #print("Pressure = ",RH,"\n")
    #print("Temperature = ",T, "\n")
    if RH is 0 or T is 0:
        print("NOT SENT")
    else:
        f = urllib2.urlopen(baseurl + "&field1={0}&field2={1}".format(RH, T))
        print("Sent")
        print(f.read())
        f.close()

class Watcher(dbus.service.Object):
    # print("\nIn Watcher\n")

    @dbus.service.method(HEARTRATE_WATCHER_INTERFACE,
                         in_signature="oa{sv}", out_signature="")
    def MeasurementReceived(self, device, measure):
        global count
        global x
        global y
        # print("Measurement received from %s" % device)
        # print(count)
        #x = 0
        if measure["Value"] < 100:
        #     count = 0
        # else:
        #     count = 1
        # if count is 0:
            # print("Value: ", float(measure["Value"]),"C")
            x = (measure["Value"])
            print(x)
        else:
            # print("Value: ", float(measure["Value"])/10,"kPA")
            y = float(measure["Value"]) / 10
            print(y)
        #print("Pressure MR = ", x, "\n")
        #print("Temperature MR = ", y, "\n")
        count = count + 1
        if count is 2:
            count = 0
            sendToThingsSpeak(x, y)

        if "Energy" in measure:
            print("Energy: ", measure["Energy"])

        if "Contact" in measure:
            print("Contact: ", measure["Contact"])

        if "Interval" in measure:
            for i in measure["Interval"]:
                print("Interval: ", i)


if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # print("\nIn Main\n")
    bus = dbus.SystemBus()

    option_list = [
        make_option("-i", "--adapter", action="store",
                    type="string", dest="adapter"),
        make_option("-b", "--device", action="store",
                    type="string", dest="address"),
    ]

    parser = OptionParser(option_list=option_list)

    (options, args) = parser.parse_args()

    if not options.address:
        print("Usage: %s [-i <adapter>] -b <bdaddr> [cmd]" % (sys.argv[0]))
        print("Possible commands:")
        print("\tReset")
        sys.exit(1)

    managed_objects = bluezutils.get_managed_objects()
    adapter = bluezutils.find_adapter_in_objects(managed_objects,
                                                 options.adapter)
    adapter_path = adapter.object_path

    heartrateManager = dbus.Interface(bus.get_object(BUS_NAME,
                                                     adapter_path), HEARTRATE_MANAGER_INTERFACE)

    path = "/test/watcher"
    heartrateManager.RegisterWatcher(path)

    device = bluezutils.find_device_in_objects(managed_objects,
                                               options.address,
                                               options.adapter)
    device_path = device.object_path

    heartrate = dbus.Interface(bus.get_object(BUS_NAME, device_path),
                               HEARTRATE_INTERFACE)

    watcher = Watcher(bus, path)
    # print("\nIn Main2\n")

    dev_prop = dbus.Interface(bus.get_object(BUS_NAME, device_path),
                              "org.freedesktop.DBus.Properties")

    properties = dev_prop.GetAll(HEARTRATE_INTERFACE)

    if "Value" in properties:
        print("Sensor location: %s" % properties["Value"])
    else:
        print("Sensor location is not supported")

    '''print("%s"%args[0])'''

    if len(args) > 0:
        if args[0] == "Reset":
            reset_sup = properties["ResetSupported"]
            if reset_sup:
                heartrate.Reset()
            else:
                print("Reset not supported")
                sys.exit(1)
        else:
            print("unknown command")
            sys.exit(1)

    mainloop = GObject.MainLoop()
    mainloop.run()
