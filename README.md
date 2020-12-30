# eaps-gas-box

## Install & Setup
1. Install Python3, Pip3, and Venv 
    * ``` sudo apt install python3 python3-pip python3-venv ```
2. Create a Python3 venv in the repo folder
    * ``` python3 -m venv .venv ```
3. Activate the venv.
    * ``` source .venv/bin/activate ```
4. Install project requirements
    * ``` pip3 install -r requirements.txt ```

## Running the project
### From terminal
``` gunicorn wsgi:app ```

### As a service
1.  Copy the gasbox.service file to /etc/systemd/system/
    * ``` cp gasbox.service /etc/systemd/system/ ```
2. Copy the nginx site file to /etc/nginx/sites-available
3. Link the nginx site file to /etc/nginx/sites-enabled

