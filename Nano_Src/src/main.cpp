#include <Arduino.h>
#include <SDISerial.h>
#include <AltSoftSerial.h>
#include <Wire.h>

#define BAUD 115200
#define MY_DEBUG true

#define RS486_BAUD 19200
#define UART1_BAUD 9600

typedef union floatUnion_t {
    float f;
    uint8_t bytes[sizeof(float)];
} Float_t;

typedef union uint16Union_t {
    unsigned int int16;
    unsigned char int8[sizeof(uint16_t)];
} Uint16_t;

// PROGRAM CONSTANTS
constexpr uint8_t I2C_ADDRESS = 0x14;


// I2C COMMAND CODES
constexpr uint8_t COMMAND_REG = 0x00;

constexpr uint8_t A_READ_A0 = 0x10;
constexpr uint8_t A_READ_A1 = 0x11;
constexpr uint8_t A_READ_A2 = 0x12;
constexpr uint8_t A_READ_A3 = 0x13;
constexpr uint8_t A_READ_A4 = 0x14; // I^2C Pin SDA
constexpr uint8_t A_READ_A5 = 0x15; // I^2C Pin SCL
constexpr uint8_t A_READ_A6 = 0x16;
constexpr uint8_t A_READ_A7 = 0x17;

constexpr uint8_t SDI12_READ = 0x20;
constexpr uint8_t SDI12_POLL = 0x21;

constexpr uint8_t UART0_READ = 0x30;
constexpr uint8_t UART1_READ = 0x31;

constexpr uint8_t UART0_POLL = 0x32;
constexpr uint8_t UART1_POLL = 0x33;

constexpr uint8_t DATA_LEN = 64;

// Globals

Uint16_t analogRegister[16] = { 0 };

char SDI12_data[12];
char UART0_data[12];
char UART1_data[12];

char command[DATA_LEN];
uint8_t command_code = 0;


uint8_t uart0_i = 0;

// UART0
uint8_t UART0_i = 0;
uint8_t UART0_data_ready = 0;
uint8_t UART0_data_requested = 0;

// UART1
uint8_t UART1_i = 0;
uint8_t UART1_data_ready = 0;
uint8_t UART1_data_requested = 0;

//SDI12
SDISerial SDI12(11);
uint8_t SDI12_data_ready = 0;
uint8_t SDI12_data_requested = 0;

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
    Serial.println("i2c recieve");
}

void requestEvent(){
    /* Responds to a data request from the I^2C Master. Sends
     * back requested data based on register requested.
     * 
     * Number of bytes sent to Master:
     *      A_READ_0: 2 bytes
     *      A_READ_1: 2 bytes
     *      A_READ_2: 2 bytes
     *      A_READ_3: 2 bytes
     *      A_READ_4: 2 bytes
     *      A_READ_5: 2 bytes
     *      SDI12_READ: 12 bytes
     *      SDI12_POLL: 1 byte
     *      UART1_READ: 12 bytes
     *      UART1_POLL: 1 byte
     * 
     * Returns:
     *      Void
     */
    
    switch(command_code){
        case A_READ_A0:
            Wire.write(analogRegister[0].int8[0]);
            Wire.write(analogRegister[0].int8[1]);
            break; 

        case A_READ_A1:
            Wire.write(analogRegister[1].int8[0]);
            Wire.write(analogRegister[1].int8[1]);
            break; 

        case A_READ_A2:
            Wire.write(analogRegister[2].int8[0]);
            Wire.write(analogRegister[2].int8[1]);
            break; 

        case A_READ_A3:
            Wire.write(analogRegister[3].int8[0]);
            Wire.write(analogRegister[3].int8[1]);
            break; 

        case A_READ_A4:
            Wire.write(analogRegister[4].int8[0]);
            Wire.write(analogRegister[4].int8[1]);
            break; 

        case A_READ_A5:
            Wire.write(analogRegister[5].int8[0]);
            Wire.write(analogRegister[5].int8[1]);
            break; 
        
        case A_READ_A6:
            Wire.write(analogRegister[6].int8[0]);
            Wire.write(analogRegister[6].int8[1]);
            break; 

        case A_READ_A7:
            Wire.write(analogRegister[7].int8[0]);
            Wire.write(analogRegister[7].int8[1]);
            break;

        case SDI12_READ:
            if (SDI12_data_ready){
                Serial.print(SDI12_data);
                Wire.write(SDI12_data, 12); 
            }
            else {
                Wire.write(0x00);
            }
            
            break;  

        case UART1_READ:
            if (UART1_data_ready){
                Serial.print(UART1_data);
                Wire.write(UART1_data, 12);    
                UART1_data_requested = 0;     
            }
            else {
                Wire.write(0x00);
            }
            
            break; 
      
    }
    Serial.println("I2C");
}

void queryUART1(){
    UART1.print(command);  
}



uint16_t readAnalog(uint8_t pin){
    uint16_t value = analogRead(pin);
    return value;
}

void sampleAnalogSensors(){
    uint8_t i = 0;
    uint8_t j = 14;
    for (i = 0; i < 8; i++){
        analogRegister[i].int16 = analogRead(j);
        j++;
    }

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

  // Discard first analogRead() output
  analogRead(A0);

}

void loop() {
    char c;
    delay(1); 

    // Check SW Serial Port
    if (UART1.available() > 1){
        c = UART1.read();
        UART1_data[UART1_i] = c;
        UART1_i++;

        if(c == '\n'){
            UART1_data[UART1_i] = '\0';  
            UART1_i = 0;
            UART1_data_ready = 1;
        }
    }

    // Check HW Serial Port
    if (Serial.available() > 1){
        c = Serial.read();
        UART0_data[UART0_i] = c;
        UART0_i++;

        if(c == '\n'){
            UART0_data[UART0_i] = '\0';  
            UART0_i = 0;
            UART0_data_ready = 1;
            Serial.println("got cmd");
        }
    }

    // Check the ADC values of the analog sensors
    sampleAnalogSensors();

    // Sample the UART1 O2 sensor
    if (!UART1_data_ready && !UART1_data_requested) {
        UART1.print("A\r\n");
        UART1_data_requested = 1;
    }

    // Sample the SDI-12 sensors
    if (!SDI12_data_ready && !SDI12_data_requested) {
        char * response;
        //response = SDI12.sdi_query("", 250);
        //ssprintf(); 
        SDI12_data_requested = 1;
    }

    // Print values to computer for verification
    if (UART1_data_ready){
        //asdf
        UART1_data_ready = 0;
    }


    
    
     
}
