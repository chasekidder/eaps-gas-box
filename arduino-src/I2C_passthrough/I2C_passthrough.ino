#include <SDISerial.h>
#include <AltSoftSerial.h>
#include <Wire.h>

#define BAUD 115200
#define MY_DEBUG true

#define RS486_BAUD 19200
#define UART1_BAUD 9600

// PROGRAM CONSTANTS
constexpr uint8_t I2C_ADDRESS = 0x14;
constexpr uint8_t SDI12_DATA_PIN = 2;
constexpr uint8_t RS485_RX_PIN = 4;
constexpr uint8_t RS485_TX_PIN = 5;
//constexpr uint8_t UART1_RX_PIN = 8;
//constexpr uint8_t UART1_TX_PIN = 9;

// I2C COMMAND CODES
constexpr uint8_t COMMAND_REG = 0x00;
constexpr uint8_t A_READ_A0 = 0x10;
constexpr uint8_t A_READ_A1 = 0x11;
constexpr uint8_t A_READ_A2 = 0x12;
constexpr uint8_t A_READ_A3 = 0x13;
constexpr uint8_t A_READ_A4 = 0x14;
constexpr uint8_t A_READ_A5 = 0x15;
constexpr uint8_t SDI12_READ = 0x20;
constexpr uint8_t UART0_READ = 0x30;
constexpr uint8_t UART1_READ = 0x31;
constexpr uint8_t UART0_POLL = 0x32;
constexpr uint8_t UART1_POLL = 0x33;


// Globals
char rx_data[64];
char uart1_data[32];
char command[64];
uint8_t command_code = 0;
uint8_t uart1_i = 0;
uint8_t UART1_data_ready = 0;

//SDI12
SDISerial SDI12(SDI12_DATA_PIN);

//UART1
AltSoftSerial UART1; // TX 9, RX 8



void receiveEvent(int bytes){
    command_code = Wire.read();

    if (command_code == COMMAND_REG){
          uint8_t i = 0;
          while(Wire.available() > 0){
              command[i] = Wire.read();  
              i++;
          }
          command[i] = '\0';
    }
}

void requestEvent(){
    uint16_t response = 0;
    
    switch(command_code){
        case A_READ_A0:
            //TODO: make this send 2 bytes instead of one
            response = readAnalog(14);
            Wire.write(response);
            break; 

        case A_READ_A1:
            response = readAnalog(15);
            Wire.write(response);
            break;  

        case A_READ_A2:
            response = readAnalog(16);
            Wire.write(response);
            break;  

        case A_READ_A3:
            response = readAnalog(17);
            Wire.write(response);
            break;  

        case A_READ_A4:
            response = readAnalog(18);
            Wire.write(response);
            break;   

        case A_READ_A5:
            response = readAnalog(19);
            Wire.write(response);
            break;   

        case SDI12_READ:
            Serial.println(command);
            querySDI12();
            Serial.println(rx_data);
            Wire.write(rx_data); 
            break;  

        case UART1_POLL:
            Serial.print(command);
            UART1.print(command);
            Wire.write(0x00);
            break; 

        case UART1_READ:
            if (UART1_data_ready == 1){
                Wire.write(uart1_data);  
            }
            else{
                Wire.write(0x00);  
            }
            break; 
      
    }
}

void queryUART1(){
    UART1.print(command);  
}

void querySDI12(){
    char* resp = SDI12.sdi_query(command, 500);
    sprintf(rx_data, "%s", resp ? resp:"No response");
}

int readAnalog(uint8_t pin){
    int value = analogRead(pin);
    return value;
}

void setup() {
  // Debug configuration
  if (MY_DEBUG){
      Serial.begin(BAUD);
      Serial.println("Nano Reset!");
  }

  // Setup I2C Communications
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  // Setup SDI-12 Communications
  SDI12.begin();

  // Setup UART1 Communications
  UART1.begin(UART1_BAUD);

}

void loop() {
    char c;
    delay(1); 

    if (UART1.available() > 1){
        c = UART1.read();
        rx_data[uart1_i] = c;
        uart1_i++;

        if(c == '\n'){
            uart1_data[uart1_i] = '\0';  
            uart1_i = 0;
            UART1_data_ready = 1;
        }
    }
     
}