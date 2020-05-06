import serial
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime as dt
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox


# Open serial port on COM17
s = serial.Serial(port='COM17', baudrate=115200)

window_list = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
window_i = 9
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


# Returns the byte rate in bytes/sec that is read from UART
def calc_byte_rate():
    start_t = time.time()
    count = 0
    while time.time() < start_t + 1:
        rawData = int.from_bytes(s.read(1), "little", signed=True)

        voltData = rawData / 0xFF
        # print(voltData)
        count += 1
    return count


# Prints the rawData from ADC
def print_raw_data():
    while True:
        rawData = int.from_bytes(s.read(1), "little", signed=True)
        print(rawData)


def increase_scale():
    global window_i
    window_i += 1


def decrease_scale():
    global window_i
    window_i -= 1

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read data from serial
    buffer_val = s.inWaiting()
    if buffer_val > 50000:
        s.reset_input_buffer()
    rawData = int.from_bytes(s.read(1), "little", signed=True)
    voltData = rawData / 0xFF

    # Add x and y to lists

    xs.append(dt.datetime.now().strftime('%S.%f'))
    ys.append(voltData)


    global window_list
    global window_i

    xlabel = 'Milli-seconds (ms)'
    window_size = window_list[window_i]
    if window_size > 500:
        window_size = window_list[window_i] / 1000
        xlabel = "Seconds (s)"

    window_size = int(window_size)

    # Limit x and y lists to 20 items
    xs = xs[-(window_size+1):]
    ys = ys[-(window_size+1):]
    my_xticks = []

    for i in range(0, window_size):
        if i % (window_size / 10) == 0:
            my_xticks.append(i)
        else:
            my_xticks.append("")

    my_xticks.append(window_size)

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.ylim(-.5, .5)
    plt.xlim(0, window_size)
    plt.xticks(xs, my_xticks, ha='center')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Voltage vs. Time')
    plt.ylabel('Voltage (V)')
    plt.xlabel(xlabel)


def main():
    ax_decrease = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax_increase = plt.axes([0.81, 0.05, 0.1, 0.075])
    btn_decrease = Button(ax_decrease, "<-")
    btn_increase = Button(ax_increase, "->")
    btn_decrease.on_clicked(decrease_scale())
    btn_increase.on_clicked(increase_scale())
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=30)
    plt.show()

main()

