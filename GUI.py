from locale import atof, atoi

import serial
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime as dt
from matplotlib.widgets import Button
from string import *
from matplotlib.widgets import TextBox


# Open serial port on COM17
s = serial.Serial(port='COM17', baudrate=115200)

window_list = [1, 3, 5, 15, 30, 75, 150, 300, 750, 1500, 3000, 7500, 15000]
buffer_list = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
window_i = 7
buffer_i = 0
ticks = 0
playNode = 0


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
xs_record = []
ys_record = []

# Booleans for button presses
isPlaying = False
isRecording = False
isPaused = False


class Buttons:

    def increase_scale(self, event):
        global window_i
        window_i += 1
        if window_i == len(window_list):
            window_i = 0
        print(window_list[window_i])

    def decrease_scale(self, event):
        global window_i
        window_i -= 1
        if window_i < 0:
            window_i = len(window_list)-1
        print(window_list[window_i])

    def snapshot(self, event):
        plt.savefig("graph_snapshot.png")
        print("got here")

    def play(self, event):
        global isPlaying
        if isPlaying:
            isPlaying = False
        else:
            isPlaying = True
        print("isPlaying = ", isPlaying)

    def record(self, event):
        global isRecording
        if isRecording:
            isRecording = False
        else:
            isRecording = True
        print("isRecording = ", isRecording)

    def pause(self, event):
        global isPaused
        if isPaused:
            isPaused = False
        else:
            isPaused = True
        print("isPaused = ", isPaused)


# Returns the byte rate in bytes/sec that is read from UART
def calc_byte_rate():
    start_t = time.time()
    count = 0
    while time.time() < start_t + 1:
        int.from_bytes(s.read(1), "little", signed=True)
        count += 1
    return count


# Prints the rawData from ADC
def print_raw_data():
    while True:
        rawData = int.from_bytes(s.read(1), "little", signed=True)
        print(rawData)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    global playNode


    # Read data from serial
    buffer_val = s.inWaiting()
    if buffer_val > 40000:
        s.reset_input_buffer()
    rawData = int.from_bytes(s.read(1), "little", signed=True)
    voltData = rawData / 0xFF


    # Add x and y to lists
    if not isPlaying:
        xs.append(dt.datetime.now().strftime('%S.%f'))
        ys.append(voltData)

    global window_list
    global window_i

    window_size = window_list[window_i]
    window_size = int(window_size)

    if isRecording:
        xs_record.append(xs)
        ys_record.append(ys)



    # Limit x and y lists to window_size of items
    xs = xs[-(window_size+1):]
    ys = ys[-(window_size+1):]


    # X axis time scaling
    count = 0
    if window_i >= 0 and window_i < 3:
        for i in range(len(xs)):
            xs[i] = str(count * 100)
            count += 1
        units = '(us)'
    if window_i >= 3 and window_i < 12:
        for i in range(len(xs)):
            xs[i] = str(count / 10)
            count += 1
        units = '(ms)'
    if window_i == 12:
        for i in range(len(xs)):
            xs[i] = str(count / 1000)
            count += 1
        units = '(s)'



    if isPlaying:
        for i in range(0,len(xs)):
            xs[i] = xs_record[playNode]
            ys[i] = ys_record[playNode]
            playNode += 1
            if(playNode == len(xs_record)):
                playNode = 0


    # Draw x and y lists
    xs = [str(round(atof(x), 2)) for x in xs]
    if not isPaused:
        ax.clear()
        ax.plot(xs, ys)

    # Format plot
    ax.set_ylim(-.5, .5)
    ax.set_xlim(0, buffer_list[window_i])
    x_ticks_list = np.arange(0, (buffer_list[window_i] + 1), buffer_list[window_i]/10)
    ax.set_xticks(x_ticks_list)
    #ax.set_xticks(xs, my_xticks)
    plt.subplots_adjust(bottom=0.30)
    ax.set_title('Voltage vs. Time')
    ax.set_ylabel('Voltage (V)')
    ax.set_xlabel('Time ' + units)


def main():
    buttons = Buttons()
    ax_decrease = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax_increase = plt.axes([0.81, 0.05, 0.1, 0.075])
    ax_snip = plt.axes([0.5, 0.05, 0.1, 0.075])
    ax_record = plt.axes([0.1, 0.05, 0.1, 0.075])
    ax_play = plt.axes([0.21, 0.05, 0.1, 0.075])
    ax_pause = plt.axes([0.35, 0.05, 0.15, 0.075])

    btn_decrease = Button(ax_decrease, "<-")
    btn_increase = Button(ax_increase, "->")
    btn_snip = Button(ax_snip, "Snap")
    btn_record = Button(ax_record, "Record")
    btn_play = Button(ax_play, "Playback")
    btn_pause = Button(ax_pause, "Pause/Play")

    btn_decrease.on_clicked(buttons.decrease_scale)
    btn_increase.on_clicked(buttons.increase_scale)
    btn_snip.on_clicked(buttons.snapshot)
    btn_record.on_clicked(buttons.record)
    btn_play.on_clicked(buttons.play)
    btn_pause.on_clicked(buttons.pause)

    # Set up plot to call animate() function periodically

    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=30)
    plt.show()

main()

