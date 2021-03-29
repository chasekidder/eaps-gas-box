/*  globals.hpp
*   Author: Chase Kidder
*   Date: 03.22.2021
*/
#ifndef Nano_globals_hpp
#define Nano_globals_hpp

#include <Arduino.h>

typedef union floatUnion_t {
    float f;
    uint8_t bytes[sizeof(float)];
} FloatBytes;

typedef union uint16Union_t {
    unsigned int int16;
    unsigned char int8[sizeof(uint16_t)];
} IntegerBytes;


class REGISTER {
    public:
        constexpr static uint8_t COMMAND_REG = 0x00;
        constexpr static uint8_t PUMP_CTRL_REG = 0x50;

        constexpr static uint8_t GPS_DAY = 0x40;
        constexpr static uint8_t GPS_MONTH = 0x41;
        constexpr static uint8_t GPS_YEAR = 0x42;
        constexpr static uint8_t GPS_HOUR = 0x43;
        constexpr static uint8_t GPS_MINUTE = 0x44;
        constexpr static uint8_t GPS_SECOND = 0x45;
        constexpr static uint8_t GPS_MILLISECOND = 0x46;
        constexpr static uint8_t GPS_LATITUDE = 0x47;
        constexpr static uint8_t GPS_LONGITUDE = 0x48;
        constexpr static uint8_t GPS_ANGLE = 0x49;
        constexpr static uint8_t GPS_ALTITUDE = 0x4A;
};

class CONSTANT {
    public:
        constexpr static uint8_t I2C_ADDRESS = 0x14;
        constexpr static uint8_t MAX_DATA_LEN = 32;

        constexpr static uint8_t PUMP_PIN = 9;
        constexpr static uint8_t SDI12_PIN = 11;

        constexpr static uint32_t UART0_BAUD = 115200;
        constexpr static uint32_t UART1_BAUD = 9600;

};


#endif