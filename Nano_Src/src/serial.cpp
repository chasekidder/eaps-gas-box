#include "serial.hpp"

void readUART0() {
    char c = 0;

    if (Serial.available() > 1){
        c = Serial.read();
        UART0_data[UART0_i] = c;
        UART0_i++;

        if(c == '\n'){
            UART0_data[UART0_i] = '\0';  
            UART0_i = 0;
            UART0_data_ready = 1;       
        }
    }

    return;
}

void readUART1() {
    char c = 0;

    if (UART1.available() > 1){
        c = UART1.read();
        UART1_data[UART1_i] = c;
        UART1_i++;
        UART1_receiving = 1;

        if(c == '\r'){
            UART1_data[UART1_i] = '\0';
            UART1_i = 0;
            if(UART1_data_requested) UART1_data_ready = 1;
            UART1_receiving = 0;
            Serial.println("Response Recieved!");
            Serial.println(UART1_data);
        }
    }

    return;
}

