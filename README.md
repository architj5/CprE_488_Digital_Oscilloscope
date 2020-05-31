# CprE Digital Oscilloscope
This is the final project of the course CprE 488 (Spring 2020)

- The goal of our final project is to create a digital oscilloscope GUI in Python using the XADC module in Vivado. We will use serial communication over UART to port data to the GUI from SDK.
- Set up the XADC module in Xilinx Vivado and added the ports in the constraint file
- SDK file has initialization and instantiation of XADC module
- ADC.c file also send the data over UART to the COM Port
- Python file reads the data from the COM Port and converts the raw values to the actual voltage values
- Using matplotlib GUI.py plots a real-time GUI that can display the input signal with some functionalities like buttons to pause, scale the signals
