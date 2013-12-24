#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep


timeout = 10 #secs

print "NGS"
print "Connector A"

####################################
print "1"
GPIO.setup("P8_20", GPIO.OUT)
GPIO.setup("P9_42", GPIO.OUT)
GPIO.output("P8_20",GPIO.HIGH)
GPIO.output("P9_42",GPIO.HIGH)
PWM.start("P9_16", 50)
PWM.set_duty_cycle("P9_16", 25.5)
PWM.set_frequency("P9_16", 10)
sleep(timeout)
PWM.stop("P9_16")
PWM.cleanup()
GPIO.cleanup()

####################################
print "2"
GPIO.setup("P8_22", GPIO.OUT)
GPIO.setup("P9_42", GPIO.OUT)
GPIO.output("P8_22",GPIO.HIGH)
GPIO.output("P9_42",GPIO.HIGH)
PWM.start("P9_16", 50)
PWM.set_duty_cycle("P9_16", 25.5)
PWM.set_frequency("P9_16", 10)
sleep(timeout)
PWM.stop("P9_16")
PWM.cleanup()
GPIO.cleanup()

####################################
print "3"
GPIO.setup("P8_24", GPIO.OUT)
GPIO.setup("P9_42", GPIO.OUT)
GPIO.output("P8_24",GPIO.HIGH)
GPIO.output("P9_42",GPIO.HIGH)
PWM.start("P9_16", 50)
PWM.set_duty_cycle("P9_16", 25.5)
PWM.set_frequency("P9_16", 10)
sleep(timeout)
PWM.stop("P9_16")
PWM.cleanup()
GPIO.cleanup()

####################################
print "4"
GPIO.setup("P8_6", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_6",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "5"
GPIO.setup("P8_12", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_12",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "6"
GPIO.setup("P8_14", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_14",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "7"
GPIO.setup("P8_16", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_16",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "8"
GPIO.setup("P8_18", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_18",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "9"
GPIO.setup("P8_20", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_20",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "10"
GPIO.setup("P8_22", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_22",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

####################################
print "11"
GPIO.setup("P8_24", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)
GPIO.output("P8_24",GPIO.HIGH)
GPIO.output("P8_11",GPIO.HIGH)
PWM.start("P8_19", 50)
PWM.set_duty_cycle("P8_19", 25.5)
PWM.set_frequency("P8_19", 10)
sleep(timeout)
PWM.stop("P8_19")
PWM.cleanup()
GPIO.cleanup()

