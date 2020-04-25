#import important packages

import serial
import time
from tkinter import *
from time import sleep
from tkinter import font
import tkinter.messagebox as messagebox
import RPi.GPIO as GPIO
import board
import busio
import adafruit_bmp280
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Initialize BMP280 sensor and print starting temperature/pressure

i2c = busio.I2C(board.SCL,board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

#Print startin temperature and pressure
print('Temperature: {} degrees C'.format(sensor.temperature))
print('Pressure: {} cm H2O'.format(int(sensor.pressure)*1.02))


# Initialize GPIO pins for solenoids
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT) #inhale solenoid
GPIO.setup(17, GPIO.OUT) #exhale solenoid

# Define functions

# Inputs are inhale/exhale ratio and breaths per minute
def breathe(ie,bpm,ht):
    cycle = 60/(bpm)
    It = cycle/(1+ie)
    Et = cycle - It - 0.1
    GPIO.output(17, GPIO.HIGH)
    time.sleep(It)
    print('Pressure at inahle: {} cm H2O'.format(int(sensor.pressure)*1.02))
    GPIO.output(17, GPIO.LOW)
    time.sleep(ht)
    GPIO.output(4, GPIO.HIGH)
    time.sleep(Et)
    print('Pressure at exhale: {} cm H2O'.format(int(sensor.pressure)*1.02))
    GPIO.output(4, GPIO.LOW)
    time.sleep(0.1)

# Inputs are 
# inhale time, inhale/exhale ratio, breaths per minute
# inhale hold time, exhale hold time (both hardcoded to 0.1)     
def breathe_mobile(iTime,ieRatio,bpm,iHold,eHold):
    cycle = 60/(bpm)
    eTime = 1/ieRatio 
    GPIO.output(17, GPIO.HIGH)
    time.sleep(iTime)
    print('Pressure at inahle: {} cm H2O'.format(int(sensor.pressure)*1.02))
    GPIO.output(17, GPIO.LOW)
    time.sleep(iHold)
    GPIO.output(4, GPIO.HIGH)
    time.sleep(eTime)
    print('Pressure at exhale: {} cm H2O'.format(int(sensor.pressure)*1.02))
    GPIO.output(4, GPIO.LOW)
    time.sleep(eHold)


#Function to ventilate used by mobile apps by cycling inhale and exhale solenoids as many times as given by ventilation time
def ventilate_mobile(characteristics):
  if self.parameterValidations(characteristics)
   iTime = characteristics[0]
   ieRatio = characteristics[1]
   bpm = characteristics[2]
   flowRate = characteristics[3]
   ventTime = characteristics[4]    
  
   print('Breaths per minute: {} bpm'.format(bpm))
   print('I/E ratio: {}'.format(ieRatio))
   print('Inhale time: {} s'.format(iTime))
   print('Flow rate: {} ml/s'.format(flowRate))
   print('Ventilation time: {} s'.format(ventTime)) 

   ventCycles = (ventTime * bpm)/60
   cycle = 1

   for cycle in range(1, ventCycles+1):
      print('Breath {}:'.format(cycle))
      self.breathe_mobile(iTime, ieRatio, bpm, 0.1, 0.1)

  else
    print('Parameters validation failure!!')


def parameterValidations(self, parameters)

  # validate all the parameters for type, size, length, Properties

  return true

    
#Function to ventilate by cylcing inhale and exhale solenoids as many times as given by ventilation cycles
def ventilate():
    IE= varIE.get()
    ie = float(IE)
    BPM = varBPM.get()
    bpm = float(BPM)
    Ht = varHt.get()
    ht = float(Ht)
    Vc = varVc.get()
    vc = int(Vc)
    time = (60/bpm)*vc
    j= 1
    for j in range(1,vc+1):
      print('Breath {}:'.format(j))
      mm.breathe(ie,bpm,ht)
      # Print critical information
      print('Breaths per minute: {} bpm'.format(bpm))
      print('I/E ratio: {}'.format(ie))
      print('Total time: {} s'.format(time))



#Function to clean GPIO pin assignments after ventilation
def clean():
    GPIO.cleanup()


