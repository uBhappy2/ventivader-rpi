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
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

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
    
    