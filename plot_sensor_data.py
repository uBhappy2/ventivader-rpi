import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import board
import busio
import adafruit_bmp280


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = []
y = []

# Initialize communication with sensor
i2c = busio.I2C(board.SCL,board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)


# This function is called periodically from FuncAnimation
def animate(i, x, y):

    # Read pressure
    pressure = (int(round(sensor.pressure, 4))*1.02)-1033

    # Add x and y to lists
    x.append(dt.datetime.now().strftime('%H:%M:%S'))
    y.append(pressure)

    # Limit x and y lists to 100 items
    x = x[-100:]
    y = y[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(x, y)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Pressure data')
    plt.ylabel('Pressure (cm H2O)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(x, y), interval=10)
plt.show()
