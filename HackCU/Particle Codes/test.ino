// This #include statement was automatically added by the Particle IDE.
#include "Adafruit_DHT/Adafruit_DHT.h"

// This #include statement was automatically added by the Particle IDE.
#include "ThingSpeak/ThingSpeak.h"

// This #include statement was automatically added by the Particle IDE.
#include "photon-thermistor/photon-thermistor.h"
#include <math.h>
//#include <photon-thermistor.h>

    #include "ThingSpeak/ThingSpeak.h"

//    #include "ThingSpeak.h"

   TCPClient client;
   // On Particle: 0 - 4095 maps to 0 - 3.3 volts
   //#define VOLTAGE_MAX 3.3
   //#define VOLTAGE_MAXCOUNTS 4095.0
#define DHTPIN 1
#define DHTTYPE DHT11
#define pin 4
int photocellPin = 3;
DHT dht(DHTPIN, DHTTYPE);
unsigned long myChannelNumber = 105460;
const char * myWriteAPIKey = "ZLC926VS9GJSCV9W";

Thermistor *thermistor;

void setup() 
{
   ThingSpeak.begin(client);
 thermistor = new Thermistor(A0, 10000, 4095, 10000, 25, 3950, 5, 20);
 pinMode(pin,INPUT);
 dht.begin();
 
}

void loop() {
   delay(2000);
 float tempF = thermistor->readTempF();
 int tempC=(tempF+0.0001-32.01)*float(5.0000/9.0000);
// Particle.publish(String("tempf"), String(tempF));
 float h = dht.getHumidity();
 //Particle.publish(String("H"), String(h));
 int val=digitalRead(pin);
 int inten=analogRead(photocellPin);
int intensity;
 if (inten<1000)
 {
     intensity=0;
 }
 else intensity=1;
 ThingSpeak.setField(1,tempC);
 ThingSpeak.setField(2,h);
 ThingSpeak.setField(3,val);
 ThingSpeak.setField(4,intensity);
 ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
 //Particle.publish("A",String(intensity));
 delay(17000);
 
 
}