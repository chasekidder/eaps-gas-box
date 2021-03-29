#include "sdi12.hpp"

void querySDI12() {
    Serial.println(command);
    char * response;
    response = SDI12.sdi_query(command, 250); 
    
    sprintf(SDI12_data, "%s", response);

    SDI12_data_requested = 0;
    SDI12_data_ready = 1;
}