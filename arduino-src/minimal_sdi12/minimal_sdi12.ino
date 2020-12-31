#include <string.h>
#include <ctype.h>

#include <SDISerial.h>
#include <Wire.h>
#include <SPI.h>

// CONSTANTS
#define DELIMETER "|"
#define DATA_PIN 2
#define MAX_RX_LEN 64
#define MAX_CMD_LEN 48
#define MAX_PROTOCOL_LEN 16
#define MAX_TX_LEN 64

const char bol = '<';
const char eol = '>';

// PROTOCOL SETUP
SDISerial SDI12(DATA_PIN);

// GLOBAL VARIABLES
char rx_data[MAX_RX_LEN];
char tx_data[MAX_TX_LEN];

boolean new_cmd = false;

/* SDISerial Methods:
    void sdi_cmd(cmd (str))
    char* sdi_query(query (str), timeout (int))
*/

void recv_serial_data() {
    static boolean receiving = false;
    static byte i = 0;
    char recv;
 
    while (Serial.available() > 0 && new_cmd == false) {
        recv = Serial.read();

        if (receiving == true) {
            if (recv != eol) {
                rx_data[i] = recv;
                i++;
                if (i >= MAX_RX_LEN) {
                    i = MAX_RX_LEN - 1;
                }
            }
            else {
                rx_data[i] = '\0'; 
                receiving = false;
                i = 0;
                new_cmd = true;
            }
        }

        else if (recv == bol) {
            receiving = true;
        }
    }
}

void send_via_protocol(char* protocol, char* cmd) {
    if (strcmp(protocol, "SPI") == 0) {
        byte command = 0x00;
        byte data_register = 0x00;
        
        // Write to register here
    }
    
    else if (strcmp(protocol, "I2C") == 0) {
        char response[MAX_TX_LEN];
        static byte i = 0;
        byte slave_id = 0;
        byte num_rx_bytes = 0;
        
        //PARSE CMD HERE
      
        Wire.requestFrom(slave_id, num_rx_bytes);

        while (Wire.available()) { 
          response[i] = Wire.read(); 
          i++;
        }
        response[i] = '\0';

        sprintf(tx_data,"%s",response ? response:F("ERROR: NO RESPONSE\r\n"));
        Serial.println(tx_data);
    }
    
    else if (strcmp(protocol, "SDI12") == 0) {
        //Serial.println(cmd);
        char* response = SDI12.sdi_query(cmd, 5000);
        sprintf(tx_data,"%s",response ? response:"ERROR: NO RESPONSE\r\n");
        Serial.println(tx_data);
    }
    
    else if (strcmp(protocol, "UART") == 0) {
          //Serial.println(cmd);
          // Do something for UART here
    }
    
    else {
        Serial.println(F("ERROR: PROTOCOL NOT DEFINED"));  
    }  

    
}




void setup(){
      // Open SDI-12 Sensor Comms
      SDI12.begin();

      // Open I2C Sensor Comms
      Wire.begin();

      // Open SPI Sensor Comms
      SPI.begin();
      
      // Open UART RPi Comms 
      //Serial.begin(9600);
      Serial.begin(115200);
      
      // Allow Sensor Intialization
      delay(1000);//3 seconds should be more than enough
}


void loop(){
    char* protocol;
    char* cmd;
  
    recv_serial_data();

    // If command recieved, forward it on over selected protocol
    if (new_cmd) {

        protocol = strtok(rx_data, DELIMETER);
        cmd = strtok(NULL, DELIMETER);
        
        send_via_protocol(protocol, cmd);
        
        new_cmd = false;
    }
}
