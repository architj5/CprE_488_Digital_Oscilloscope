import serial
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime as dt


s = serial.Serial(port='COM17', baudrate=115200)
s.close()
s.open()

# while True:
#     rawData = int.from_bytes(s.read(1), "little", signed=True)
#     print(rawData)


# start_t = time.time()
# count = 0
# test = 0
# while time.time() < start_t + 1:
#     rawData = int.from_bytes(s.read(1), "little", signed=True)
#
#     voltData = rawData / 0xFF
#     # print(voltData)
#     count += 1
#
# print(count)


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Read data from serial
    rawData = int.from_bytes(s.read(1), "little", signed=True)
    print(rawData)
    voltData = rawData / 0xFF

    # Add x and y to lists

    xs.append(dt.datetime.now().strftime('%S.%f'))
    ys.append(voltData)

    # Limit x and y lists to 20 items
    xs = xs[-100:]
    ys = ys[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.ylim(-.5, .5)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Voltage vs. Time')
    plt.ylabel('Voltage (V)')


# Set up plot to call animate() function periodically

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=30)
plt.show()


