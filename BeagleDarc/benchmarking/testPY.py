#/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P8_13", GPIO.OUT)
while True:
    try:
        GPIO.output("P8_13",GPIO.HIGH)
        GPIO.output("P8_13",GPIO.LOW)
    except KeyboardInterrupt, e:
        print "Quitting ..."
        GPIO.output("P8_13",GPIO.LOW)
        break

