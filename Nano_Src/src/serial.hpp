//#include "globals.hpp"

#ifndef Nano_serial_hpp
#define Nano_serial_hpp
#include "globals.hpp"
#include <Arduino.h>
#include <AltSoftSerial.h>

extern AltSoftSerial UART1; // TX 9, RX 8

extern char UART0_data[];
extern uint8_t UART0_data_ready;
extern uint8_t UART0_receiving;
extern uint8_t UART0_i;
extern uint8_t UART0_data_requested;

extern char UART1_data[];
extern uint8_t UART1_data_ready;
extern uint8_t UART1_receiving;
extern uint8_t UART1_i;
extern uint8_t UART1_data_requested;



void readUART0();
void readUART1();

#endif