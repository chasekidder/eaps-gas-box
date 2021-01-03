#include <SDISerial.h>
#include <Wire.h>
#include <SPI.h>
#include <stdlib.h>

// CONSTANTS
#define SDI12_DATA_PIN 2
#define MAX_DATA_LEN 64

#define DELIMETER "|"
#define BOL '<'
#define EOL '>'

// GLOBAL VARIABLES
char rx_data[MAX_DATA_LEN];
char tx_data[MAX_DATA_LEN];

boolean new_command = false;
bool receiving = false;
uint8_t i = 0;

// GLOBAL OBJECTS
SDISerial SDI12(SDI12_DATA_PIN);

// FUNCTION DECLARATIONS
void recv_serial_data();

//void handle_uart(char*);
//void send_uart_data();
//void recv_uart_data();

void handle_sdi12(char*);
void send_sdi12(char*);

void handle_i2c(char*);
void send_i2c(char*);
void recv_i2c(char*);

//void handle_spi(char*);
//void send_spi();
//void recv_spi();

// FUNCTION DEFINITIONS
void setup() {  

    // Initialize communication protocols
    SDI12.begin();
    Wire.begin();
    SPI.begin();
    Serial.begin(9600);
    delay(200);
}

void loop() {
    char* protocol;
    char* cmd;

    // Check for new commands
    recv_serial_data();
    //Serial.println(rx_data);

    if (new_command) {

        // Split recieved data into protocol and command strings
        protocol = strtok(rx_data, DELIMETER);
        cmd = strtok(NULL, DELIMETER);

        //Serial.println(protocol);
        //Serial.println(cmd);
        

        if (strcmp(protocol, "SPI") == 0) {
            //Serial.println("Using SPI!");
            //handle_spi(cmd);
        }
        
        else if (strcmp(protocol, "I2C") == 0) {
            //Serial.println("Using I2C!");
            handle_i2c(cmd);
        }
        
        else if (strcmp(protocol, "SDI12") == 0) {
            //Serial.println("Using SDI-12!");
            handle_sdi12(cmd);
            
        }
        
        else if (strcmp(protocol, "UART") == 0) {
            //Serial.println("Using UART!");
            //handle_uart(cmd);
        }
        
        else {
            Serial.println(F("ERROR: PROTOCOL NOT DEFINED"));  
        }  

        new_command = false;
    }

}


// Serial Data Communication
void recv_serial_data() {
    // TODO: Refactor this to not need a global i and receiving variable
    // It needs to check and wait for each character otherwise we can miss 
    // them. Maybe put a loop in here and block main()?
    
    char recv;

    // Check if there is a byte available at the serial port
    if (Serial.available() > 0 && new_command == false) {
        recv = Serial.read();
        //Serial.println(recv);

        if (receiving == true) {

            // Check for End Of Line character and end string
            if (recv == EOL) {
                rx_data[i] = '\0'; 
                receiving = false;
                i = 0;
                new_command = true;
            }

            // Add new character to string
            else {
                rx_data[i] = recv;
                i++;
            }
        }

        // Check for Beginning Of Line character
        else if (recv == BOL) {
            receiving = true;
        }
    }
}


// SDI-12 Protocol
void handle_sdi12(char* cmd){
    send_sdi12(cmd);
    Serial.println(rx_data);
}

void send_sdi12(char* cmd){
    char* temp;

    // Send command to SDI-12 bus and retrieve response
    temp = SDI12.sdi_query(cmd, 500);
    //Serial.println(temp);
    sprintf(rx_data,"%s", temp ? temp:"ERROR: NO RESPONSE");
}


// I2C Protocol
void handle_i2c(char* cmd){
    uint8_t rd_wr = 0;
    rd_wr = cmd[0];

    // Check if command is a read or a write
    switch (rd_wr)
    {
    case 'R':
        //Serial.println("Reading Data");
        recv_i2c(cmd);
        break;

    case 'W':
        //Serial.println("Writing Data");
        send_i2c(cmd);
        break;
    
    default:
        Serial.println(F("ERROR: READ WRITE BYTE NOT VALID")); 
        break;
    }

}

void send_i2c(char* cmd){
    uint8_t device_address = 0;
    uint8_t i = 2;
    
    device_address = cmd[1];

    // Send command bytes to device
    Wire.beginTransmission(device_address);
    while(cmd[i] != '\0'){
        Serial.println(cmd[i]);
        Wire.write(cmd[i]);
        i++;
    }
    Wire.endTransmission();
}

void recv_i2c(char* cmd){
    uint8_t device_address = 0;
    uint8_t num_bytes_to_read = 0;
    uint8_t data_size = 0;
    uint8_t j = 4;

    device_address = cmd[1];
    num_bytes_to_read = cmd[2];
    data_size = cmd[3];
    
    //Serial.println(device_address);
    //Serial.println(num_bytes_to_read);
    //Serial.println(data_size);

    //Serial.println("Beginning Transmission");
    // Send command bytes to device
    Wire.beginTransmission(device_address);
    while(j < (data_size + 4)){
        //Serial.println(cmd[j]);
        Wire.write(cmd[j]);
        j++;
    }
    Wire.endTransmission();

    delay(20);

    // Request results from device
    Wire.requestFrom(device_address, num_bytes_to_read);

    j = 0;
    data_size = 0;

    // Read data from i2c buffer
    while (Wire.available()) {
        rx_data[j] = Wire.read();
        //Serial.println(rx_data[j]);
        j++;
        data_size++;
    }

    for(j = 0; j < data_size; j++){
        Serial.print(rx_data[j]);  
    }

    Serial.print("\r\n");
    
}
