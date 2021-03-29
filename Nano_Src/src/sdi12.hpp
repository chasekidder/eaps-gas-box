#ifndef Nano_sdi12_hpp
#define Nano_sdi12_hpp

#include "globals.hpp"
#include <SDISerial.h>
#include <Arduino.h>

extern uint8_t SDI12_data_requested;
extern uint8_t SDI12_data_ready;
extern char SDI12_data[];
extern SDISerial SDI12;
extern char command[];

void querySDI12();


#endif