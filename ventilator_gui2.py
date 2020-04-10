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
import ventilator_functions2 as mm
import board
import busio
import adafruit_bmp280
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Initialize Raspberry pi pins for solenoids

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) #inhale solenoid
GPIO.setup(4, GPIO.OUT) #exhale solenoid

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


        self.lvarie = Label(root,text = 'I/E ratio (1:x)', fg='Purple',
                          font = Labels)
        self.lvarie.place(x=350, y=100)
        
        self.lvarie = Label(root,text = 'Hold time (s)', fg='Purple',
                          font = Labels)
        self.lvarie.place(x=350, y=150)
        
        self.lvarbpm = Label(root,text = 'Respiration rate (BPM)', fg='Purple',
                          font = Labels)
        self.lvarbpm.place(x=350, y=200)
        
        self.lvarVc = Label(root,text = 'Ventilation cycles (#)', fg='Green',
                           font = Labels)       
        self.lvarVc.place(x=350, y=250)


#create entry variables

        
        varIE = Entry(root)
        varHt = Entry(root)
        varBPM = Entry(root) 
        varVc = Entry(root)
        
        
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
        
        #Function to close pressure sensor data plot
        def closeplot():
            global func_id
            root.after_cancel(func_id)
            plt.close()
            global x,y
            del x[:]
            del y[:]
            

# Create buttons


        ventilatorButton = Button(self, text='Ventilate', font = MainButtons,
                                     command = ventilate)
        cleanButton = Button(self, text='Clean', font = ButtonsLarger,
                                     command = clean)
        exitButton = Button(self, text='Exit', font = ButtonsLarger,
                                     command = root.destroy)
        plotButton = Button(self, text = 'Plot', font = Buttons, command = read_data)
        closeplotButton = Button(self, text = 'Close Plot', font = Buttons, command = closeplot)

# Place the buttons
        varIE.place(x=550,y=100)
        varHt.place(x=550,y=150)
        varBPM.place(x=550, y=200)
        varVc.place(x=550, y=250)

        
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

