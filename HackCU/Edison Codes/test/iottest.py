from __main__ import *
import sys
from time import sleep  
import urllib2
    
# main() function
def main():
    # use sys.argv if needed
    if len(sys.argv) < 2:
        print('Usage: python tstest.py PRIVATE_KEY')
        exit(0)
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]
   
    while True:
        try:
            RH, T = y, x
			print x
			print y
			if x is 0
				continue
			if y is 0
				continue
            f = urllib2.urlopen(baseURL +"&field1=%s&field2=%s" % (RH, T))
            print f.read()
            f.close()
            sleep(5)
        except:
            print 'exiting.'
            break

# call main
if __name__ == '__main__':
    main()