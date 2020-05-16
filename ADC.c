/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xadcps.h"
#include "xstatus.h"
#include "xuartps.h"
#include "xtime_l.h"

int main()
{


    init_platform();
    xil_printf("Started\r\n");
    XAdcPs_Config *config;
    config = XAdcPs_LookupConfig(XPAR_PS7_XADC_0_DEVICE_ID);
    if (config == NULL) {
    	xil_printf("FAILED\r\n");
    }


    XAdcPs driver;
    XAdcPs_CfgInitialize(&driver, config, config->BaseAddress);

    s16 rawData;
    float voltData;
    int status;
    s16 test;
	test = 0xFF43;

    XAdcPs_SetSequencerMode(&driver, XADCPS_SEQ_MODE_SINGCHAN);
    status = XAdcPs_SetSingleChParams(&driver, XADCPS_CH_VPVN, FALSE, FALSE, TRUE);
    if (status != XST_SUCCESS) {
    	xil_printf("Error!\r\n");
    }

	// UART config
	XUartPs uart_dev;
	XUartPs_Config *uart_config_ptr;
	uart_config_ptr = XUartPs_LookupConfig(XPAR_XUARTPS_0_DEVICE_ID);

	// XPAR_XUARTPS_1_DEVICE_ID
	XUartPs_CfgInitialize(&uart_dev, uart_config_ptr, uart_config_ptr->BaseAddress);

	XUartPs_EnableUart(&uart_dev);
	XUartPs_SetBaudRate(&uart_dev, 115200);


//	XTime current_t, start_t;
//	u64 elapsed_t;
//	int count = 0;
//
//	elapsed_t = COUNTS_PER_SECOND;
//	XTime_GetTime(&start_t);
//	XTime_GetTime(&current_t);
//	while ((current_t - start_t) < elapsed_t) {
//		rawData = XAdcPs_GetAdcData(&driver, XADCPS_CH_VPVN);
//		count++;
//		XTime_GetTime(&current_t);
//	}
//
//	xil_printf("Count: %d", count);


    while(1) {
    	rawData = XAdcPs_GetAdcData(&driver, XADCPS_CH_VPVN);
    	rawData >>= 8;
    	rawData &= 0xFF;
    	// UART send
    	XUartPs_Send(&uart_dev, &rawData, 1);
    }


    cleanup_platform();
}
