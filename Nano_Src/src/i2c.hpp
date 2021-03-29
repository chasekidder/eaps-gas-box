#ifndef Nano_i2c_hpp
#define Nano_i2c_hpp

#include "globals.hpp"
#include <Arduino.h>
#include <Wire.h>
#include <AltSoftSerial.h>

extern uint8_t command_code;
extern char command[];

extern IntegerBytes analogRegister[];

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

extern char SDI12_data[];
extern uint8_t SDI12_data_ready;
extern uint8_t SDI12_data_requested;

class CMD_CODE {

    public:
        constexpr static uint8_t A_READ_A0 = 0x10;
        constexpr static uint8_t A_READ_A1 = 0x11;
        constexpr static uint8_t A_READ_A2 = 0x12;
        constexpr static uint8_t A_READ_A3 = 0x13;
        constexpr static uint8_t A_READ_A4 = 0x14; // I^2C Pin SDA
        constexpr static uint8_t A_READ_A5 = 0x15; // I^2C Pin SCL
        constexpr static uint8_t A_READ_A6 = 0x16;
        constexpr static uint8_t A_READ_A7 = 0x17;

        constexpr static uint8_t SDI12_READ = 0x20;
        constexpr static uint8_t UART0_READ = 0x30;
        constexpr static uint8_t UART1_READ = 0x31;


};

void receiveEvent(int);
void requestEvent();


#endif