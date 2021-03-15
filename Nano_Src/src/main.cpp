#include <Arduino.h>
#include <SDISerial.h>
#include <AltSoftSerial.h>
#include <Wire.h>
//#include <Adafruit_GPS.h>

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

constexpr uint8_t UART1_INIT = 0x33;

constexpr uint8_t GPS_DAY = 0x40;
constexpr uint8_t GPS_MONTH = 0x41;
constexpr uint8_t GPS_YEAR = 0x42;
constexpr uint8_t GPS_HOUR = 0x43;
constexpr uint8_t GPS_MINUTE = 0x44;
constexpr uint8_t GPS_SECOND = 0x45;
constexpr uint8_t GPS_MILLISECOND = 0x46;
constexpr uint8_t GPS_LATITUDE = 0x47;
constexpr uint8_t GPS_LONGITUDE = 0x48;
constexpr uint8_t GPS_ANGLE = 0x49;
constexpr uint8_t GPS_ALTITUDE = 0x4A;

constexpr uint8_t PUMP_CTRL_REG = 0x50;

constexpr uint8_t MAX_DATA_LEN = 32;

// Globals

Uint16_t analogRegister[16] = { 0 };

char SDI12_data[MAX_DATA_LEN];
uint8_t SDI12_response_length = 0;

char UART0_data[12];
char UART1_data[12];

char command[MAX_DATA_LEN];
uint8_t command_code = 0;

Uint16_t GPS_data[MAX_DATA_LEN] = { 0 };

// UART0
uint8_t UART0_i = 0;
uint8_t UART0_data_ready = 0;
uint8_t UART0_data_requested = 0;

// UART1
uint8_t UART1_i = 0;
uint8_t UART1_data_ready = 0;
uint8_t UART1_data_requested = 0;
uint8_t UART1_receiving = 0;

//SDI12
SDISerial SDI12(11);
uint8_t SDI12_data_ready = 0;
uint8_t SDI12_data_requested = 0;

//UART1
AltSoftSerial UART1; // TX 9, RX 8

//GPS
//Adafruit_GPS GPS(&Wire);

// Pump Control
uint8_t pumpPin = 9;
uint8_t pumpActive = 1;


void receiveEvent(int bytes){
    command_code = Wire.read();

    if (command_code == COMMAND_REG){
          uint8_t i = 0;
          while(Wire.available() > 0){
              command[i] = Wire.read();  
              i++;
          }
          command[i] = '\0';
          //Serial.print(command); // I2C breaks if this print isn't here... idk man
    }
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
     *      SDI12_READ: 32 bytes
     *      SDI12_POLL: 1 byte
     *      UART1_READ: 32 bytes
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

        // case SDI12_POLL:
        //     if (SDI12_data_ready){
        //         Wire.write(0x0F);
        //     }
        //     else if (!SDI12_data_requested){
        //         SDI12_data_requested = 1;
        //         Wire.write(0x02);
        //     }
        //     else {
        //         Wire.write(0x03);
        //     }

        case SDI12_READ:
            if (SDI12_data_ready){
                //Serial.print(SDI12_data);
                Wire.write(SDI12_data, MAX_DATA_LEN); 
                SDI12_data_ready = 0;
            }
            else if(SDI12_data_requested){
                //Do nothing because we're waiting for the sensor
                Wire.write(0x0F);
            }
            else {
                if(!SDI12_data_requested){
                    SDI12_data_requested = 1;
                }
                
                Wire.write(0x0F);
            }
            
            break;  

        case UART1_INIT:
            UART1.write(command);
            Wire.write(0x01);

        case UART1_READ:
            if (UART1_data_ready){
                //Serial.print(UART1_data);
                Wire.write(UART1_data, MAX_DATA_LEN);    
                UART1_data_ready = 0;     
            }
            else if(UART1_data_requested){
                //Do nothing because we're waiting for the sensor
                Wire.write(0x0F);
            }
            else {
                if(!UART1_data_requested && !UART1_receiving){
                    UART1_data_requested = 1;
                }
                
                Wire.write(0x0F);
            }
            
            break; 
      
    }
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

// void GPS_init(){
//     // Output RMC + GGA Data
//     GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA); 

//     // Set update rate
//     GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); 
// }

// void queryGPS(){
//     // Recieve and parse newest NMEA message
//     if (GPS.newNMEAreceived()) {
//         GPS.lastNMEA(); 
//         if (!GPS.parse(GPS.lastNMEA())) return; 
//     }
//     Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
//     Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
// }

void checkPumpPressure(){
    int pressure = 0;
    pressure = ((analogRegister[2].int16 * 60) / (4));

    if (pressure < 15){
        pumpActive = 0;
    }
    else pumpActive = 1;

    digitalWrite(pumpPin, pumpActive);
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

  // Setup GPS Communications
  //GPS.begin(0x10);
  //GPS_init();
  //queryGPS();

  // Discard first analogRead() output
  analogRead(A0);

  pinMode(pumpPin, OUTPUT);

}

void loop() {
    char c;

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
            UART1_receiving = 0;
        }
    }

    // Sample the UART1 O2 sensor
    if (!UART1_data_ready && UART1_data_requested && !UART1_receiving) {
        UART1.print("A\r\n");
        UART1_data_requested = 0;
        UART1_receiving = 1;
    }

    // Sample the SDI-12 sensors
    if (!SDI12_data_ready && SDI12_data_requested) {
        char * response;
        response = SDI12.sdi_query(command, 250); 
        
        sprintf(SDI12_data, "%s", response);

        SDI12_data_requested = 0;
        SDI12_data_ready = 1;
    }

    // Print values to computer for verification
    if (UART0_data_ready){
        UART0_data_ready = 0;
    }

    delay(0.01);

    // Check the ADC values of the analog sensors
    sampleAnalogSensors();
    
    // Check the pump
    //checkPumpPressure();
    
     
}
