#include "analog.hpp"

void sampleAnalogSensors(){
    /*  Samples all ADC pins and writes to the analog register.
    *   Returns:
    *       None
    */
    uint8_t i = 0;

    // Pin number offset for the Arduino Nano ADC pins
    uint8_t j = 14;

    for (i = 0; i < 8; i++){
        analogRegister[i].int16 = analogRead(j);
        j++;
    }

}