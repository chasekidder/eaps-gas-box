#include "globals.hpp"
#include "serial.hpp"
#include "i2c.hpp"
#include "sdi12.hpp"
#include "analog.hpp"

#define MY_DEBUG

// CPP LIBRARY OBJECTS
SDISerial SDI12(CONSTANT::SDI12_PIN);
AltSoftSerial UART1; // TX 9, RX 8
//Adafruit_GPS GPS(&Wire);

// REGISTERS
IntegerBytes analogRegister[16] = { 0 };
IntegerBytes GPS_data[CONSTANT::MAX_DATA_LEN] = { 0 };
char SDI12_data[CONSTANT::MAX_DATA_LEN] = { 0 };
char UART0_data[CONSTANT::MAX_DATA_LEN] = { 0 };
char UART1_data[CONSTANT::MAX_DATA_LEN + 16] = { 0 };
char command[CONSTANT::MAX_DATA_LEN] = { 0 };

// GLOBAL VARIABLES
uint8_t command_code = 0;

uint8_t UART0_i = 0;
uint8_t UART0_data_ready = 0;
uint8_t UART0_data_requested = 0;

uint8_t UART1_i = 0;
uint8_t UART1_data_ready = 0;
uint8_t UART1_data_requested = 0;
uint8_t UART1_receiving = 0;

uint8_t SDI12_data_ready = 0;
uint8_t SDI12_data_requested = 0;

uint8_t pumpState = 1;

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
    /*  Controls the pump state by verifying the gas line pressure.
    *   Returns:
    *       None
    */
    int pressure = 0;
    pressure = ((analogRegister[2].int16 * 60) / (4));

    if (pressure < 15){
        pumpState = 0;
    }
    else pumpState = 1;

    // Write pump activity state
    digitalWrite(CONSTANT::PUMP_PIN, pumpState);
}

void setup() {
  // Debug configuration
    #ifdef MY_DEBUG
        Serial.begin(CONSTANT::UART0_BAUD);
        Serial.println("Nano Reset!");
        Serial.println("Debug Enabled...");
    #endif

  // Setup I2C Communications
  Wire.begin(CONSTANT::I2C_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  // Setup SDI-12 Communications
  SDI12.begin();

  // Setup UART1 Communications
  UART1.begin(CONSTANT::UART1_BAUD);

  // Setup GPS Communications
  //GPS.begin(0x10);
  //GPS_init();
  //queryGPS();

  // Discard first analogRead() output
  analogRead(A0);

  pinMode(CONSTANT::PUMP_PIN, OUTPUT);

  // Initialize O2 Sensor to POLL Mode
  UART1.print("M 1\r\n");

}

void loop() {

    // Check Serial Ports for Data
    readUART0();
    readUART1();

    // Sample the SDI-12 sensors
    if (!SDI12_data_ready && SDI12_data_requested) {
        querySDI12();
    }

    // Sample the O2 sensor
    if (!UART1_data_ready && UART1_data_requested) {
        UART1.print(command);
        UART1_data_requested = 0;
    }

    // May not need this at all
    delay(0.01);

    // Check the ADC values of the analog sensors
    sampleAnalogSensors();
    
    // Check the pump
    //checkPumpPressure();
    
     
}
