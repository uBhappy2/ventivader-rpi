#import important packages

from tkinter import *
import time
from tkinter import font
import tkinter.messagebox as messagebox
import serial
from time import sleep 
import RPi.GPIO as GPIO
import board
import busio
import adafruit_bmp280
import ventilator_functionsd as mm
import board
import busio
import adafruit_bmp280
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Initialize Raspberry pi pins for solenoids

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT) #inhale solenoid
GPIO.setup(17, GPIO.OUT) #exhale solenoid

# Initialize communication with sensor
i2c = busio.I2C(board.SCL,board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)



class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()



#Create init_window
    def init_window(self):

# Define title of master widget
        self.master.title("Ventilator Control")


# Allow the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=2)
        
# Create font family:
        Timestitle = font.Font(family="Myriad Pro", size=30, weight='bold')
        Buttons = font.Font(family = 'Myriad Pro', size = 15)
        MainButtons = font.Font(family = 'Myriad Pro', size = 35, weight = 'bold')
        ButtonsLarger = font.Font(family = 'Myriad Pro', size = 30, weight = 'bold')
        Labels = font.Font(family = 'Myriad Pro', size = 12)
        
#Create labels

        self.title = Label(root, text='The VentiVader', fg = 'Black', font = Timestitle )

        self.title.place(x=230,y=0)


        self.lvarit = Label(root,text = 'Inhale time (s)', fg='Purple',
                          font = Labels)
        self.lvarit.place(x=350, y=100)
        
        self.lvarih = Label(root,text = 'Inhale hold (s)', fg='Purple',
                          font = Labels)
        self.lvarih.place(x=350, y=150)
        
        self.lvaret = Label(root,text = 'Exhale time (s)', fg='Green',
                           font = Labels)
        self.lvaret.place(x=350, y=200)
        
        self.lvareh = Label(root,text = 'Exhale hold (s)', fg='Green',
                           font = Labels)
        self.lvareh.place(x=350, y=250)
        
        self.lvarVt = Label(root,text = 'Ventilation cycles (#)', fg='Green',
                           font = Labels)       
        self.lvarVt.place(x=350, y=300)
        


#create entry variables

        
        varIt=Entry(root)
        varIh=Entry(root) 
        varEt=Entry(root)
        varEh=Entry(root)
        varVt=Entry(root)
        
# Create figure for plotting
        x = []
        y = []
        func_id = None


# Define functions
        
        #Function to constantly read pressure sensor data and plot in a new background window
        def read_data():
            global func_id
            plt.ion()
            new_value = int(round(sensor.pressure, 4))*1.02
            if new_value == '':
                pass
            else:
                y.append(new_value)
                x.append(dt.datetime.now().strftime('%H:%M:%S'))
                # Format plot
                plt.xticks(rotation=45, ha='right')
                plt.subplots_adjust(bottom=0.30)
                plt.title('Pressure data')
                plt.ylabel('Pressure (cm H2O)')
                plt.plot(x,y,'r-')
                plt.show()
                plt.pause(0.0001)
            func_id = root.after(100, read_data)
            
        #Function to open and close inhale solenoid valve (input is inhalation time and inhale hold)
        def inhale():
            ti= varIt.get()
            ti1 = float(ti)
            tih = varIh.get()
            ti2 = float(tih)
            print('Temperature: {} degrees C'.format(sensor.temperature))
            print('Pressure: {} cm H2O'.format(int(sensor.pressure)*1.02))
            mm.insol(ti1,ti2)
            print('Temperature: {} degrees C'.format(sensor.temperature))
            print('Pressure: {} cm H2O'.format(int(sensor.pressure)*1.02))
        
        #Function to open and close exhale solenoid valve (input is exhalation time and exhale hold)
        def exhale():
            te= varEt.get()
            te1=float(te)
            teh = varEh.get()
            te2 = float(teh)
            print('Temperature: {} degrees C'.format(sensor.temperature))
            print('Pressure: {} cm H2O'.format(int(sensor.pressure)*1.02))
            mm.exsol(te1,te2)
            print('Temperature: {} degrees C'.format(sensor.temperature))
            print('Pressure: {} cm H2O'.format(int(sensor.pressure)*1.02))
        
        #Function to define breaths per minute from the following user inputs: inhalation time, inhale hold, exhalation time, exhale hold
        def bpm():
            ti= varIt.get()
            ti1 = float(ti)
            tih = varIh.get()
            ti2 = float(tih)
            te= varEt.get()
            te1=float(te)
            teh = varEh.get()
            te2 = float(teh)
            bpm = 60/(ti1+ti2+te1+te2)
            print('Breaths per minute at these settings: {} bpm'.format(bpm))
        
        #Function to ventilate by cylcing inhale and exhale solenoids as many times as given by ventilation cycles
        def ventilate():
            ti= varIt.get()
            ti1 = float(ti)
            tih = varIh.get()
            ti2 = float(tih)
            te= varEt.get()
            te1=float(te)
            teh = varEh.get()
            te2 = float(teh)
            vt = varVt.get()
            vt1 = int(vt)
            bpm = 60/(ti1+ti2+te1+te2)
            print('Breaths per minute at these settings: {} bpm'.format(bpm))
            j= 1
            for j in range(1,vt1+1):
                print('inhale {}:'.format(j))
                mm.insol(ti1,ti2)
                print('exhale {}:'.format(j))
                mm.exsol(te1,te2)
            # Print critical information
            print('Breaths per minute at these settings: {} bpm'.format(bpm))
            print('Total inhalation time: {} s'.format(ti1))
            print('Total exhalation time: {} s'.format(te1))

        #Function to clean GPIO pin assignments after ventilation
        def clean():
            GPIO.cleanup()
        
        #Function to close pressure sensor data plot
        def closeplot():
            global func_id
            root.after_cancel(func_id)
            plt.close()
            global x,y
            del x[:]
            del y[:]
            

# Create buttons

        inhaleButton = Button(self, text="Inhale",
                                font = Buttons, command = inhale)
        exhaleButton = Button (self, text="Exhale",
                                 font = Buttons, command = exhale)
        ventilatorButton = Button(self, text='Ventilate', font = MainButtons,
                                     command = ventilate)
        BPMButton = Button(self, text='BPM', font = Buttons,
                                     command = bpm)
        cleanButton = Button(self, text='Clean', font = ButtonsLarger,
                                     command = clean)
        exitButton = Button(self, text='Exit', font = ButtonsLarger,
                                     command = root.destroy)
        plotButton = Button(self, text = 'Plot', font = Buttons, command = read_data)
        closeplotButton = Button(self, text = 'Close Plot', font = Buttons, command = closeplot)

# Place the buttons
        varIt.place(x=550,y=100)
        varIh.place(x=550,y=150)
        varEt.place(x=550, y=200)
        varEh.place(x=550, y=250)
        varVt.place(x=550, y=300)
        
        inhaleButton.place(x=50,y=130)
        exhaleButton.place(x=50,y=180)
        BPMButton.place(x=50, y=230)
        plotButton.place(x = 50, y = 280)
        closeplotButton.place(x = 50, y = 330)
        
        ventilatorButton.place(x = 250, y = 400)
        
        
        
        exitButton.place(x = 600, y = 500)
        cleanButton.place(x=50, y=500)



global root

root = Tk()

#size of the window
root.geometry("800x800")

app = Window(root)
root.mainloop()
