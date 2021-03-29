#include "i2c.hpp"

void receiveEvent(int bytes){
    /*  Reads I^2C command code and writes recieved commands into 
    *   the command register.
    *
    *   Returns:
    *       None
    */ 

    // Get the command code
    command_code = Wire.read();

    // Write the new command string to the command register
    if (command_code == REGISTER::COMMAND_REG){
          uint8_t i = 0;
          while(Wire.available() > 0){
              command[i] = Wire.read();  
              i++;
          }
          command[i] = '\0';
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
     *      A_READ_6: 2 bytes
     *      A_READ_7: 2 bytes
     *      SDI12_READ: 32 bytes
     *      UART1_READ: 32 bytes (out of 48 total)
     * 
     * Returns:
     *      Void
     */
    
    switch(command_code){
        // Send A0 Analog Reading via I^2C
        case CMD_CODE::A_READ_A0:
            // Send 2 bytes of data
            Wire.write(analogRegister[0].int8[0]);
            Wire.write(analogRegister[0].int8[1]);
            break; 

        // Send A1 Analog Reading via I^2C
        case CMD_CODE::A_READ_A1:
            // Send 2 bytes of data
            Wire.write(analogRegister[1].int8[0]);
            Wire.write(analogRegister[1].int8[1]);
            break; 

        // Send A2 Analog Reading via I^2C
        case CMD_CODE::A_READ_A2:
            // Send 2 bytes of data
            Wire.write(analogRegister[2].int8[0]);
            Wire.write(analogRegister[2].int8[1]);
            break; 

        // Send A3 Analog Reading via I^2C
        case CMD_CODE::A_READ_A3:
            // Send 2 bytes of data
            Wire.write(analogRegister[3].int8[0]);
            Wire.write(analogRegister[3].int8[1]);
            break; 

        // Send A4 Analog Reading via I^2C
        case CMD_CODE::A_READ_A4:
            // Send 2 bytes of data
            Wire.write(analogRegister[4].int8[0]);
            Wire.write(analogRegister[4].int8[1]);
            break; 

        // Send A5 Analog Reading via I^2C
        case CMD_CODE::A_READ_A5:
            // Send 2 bytes of data
            Wire.write(analogRegister[5].int8[0]);
            Wire.write(analogRegister[5].int8[1]);
            break; 
        
        // Send A6 Analog Reading via I^2C
        case CMD_CODE::A_READ_A6:
            // Send 2 bytes of data
            Wire.write(analogRegister[6].int8[0]);
            Wire.write(analogRegister[6].int8[1]);
            break; 

        // Send A7 Analog Reading via I^2C
        case CMD_CODE::A_READ_A7:
            // Send 2 bytes of data
            Wire.write(analogRegister[7].int8[0]);
            Wire.write(analogRegister[7].int8[1]);
            break;

        // Request data from the SDI-12 bus and send over I^2C
        case CMD_CODE::SDI12_READ:
            if (SDI12_data_ready){
                // Send 32 bytes of data
                Wire.write(SDI12_data, CONSTANT::MAX_DATA_LEN); 
                SDI12_data_ready = 0;
            }
            else if(SDI12_data_requested){
                //Do nothing because we're waiting for the sensor
                Wire.write(0x0F);
            }
            else {
                // Request new data
                if(!SDI12_data_requested){
                    SDI12_data_requested = 1;
                }
                
                Wire.write(0x0F);
            }
            
            break;  

        // Request data from the UART1 Serial port and send over I^2C
        case CMD_CODE::UART1_READ:
            if (UART1_data_ready){
                // Only send 32 bytes from the register because of a 
                // limitation in the Python smbus2 library.
                Wire.write(UART1_data, CONSTANT::MAX_DATA_LEN);
                UART1_data_ready = 0;     
            }
            else if(UART1_data_requested){
                // Do nothing because we're waiting for the sensor
                Wire.write(0x0F);
            }
            else {
                // Request new data
                if(!UART1_data_requested && !UART1_receiving){
                    UART1_data_requested = 1;
                }
                
                Wire.write(0x0F);
            }
            
            break; 
      
    }
}