# Arduino Continuous Integration Server
## Author: Kenneth Hancock

Pretty simple server to allow mutiple people to work on one Arduino chip my uploading to a server connected to the arduino chip.

## This tool is not completed yet -- Its very rough right now.


## Requirements - Pre Start-up
*Make sure you have the Arduino app installed on the system!*

Also make sure the user running the server -- whatever user you are using is added to the dialout group
so you don't get permission issues when the server tries uploading to the arduino.  This can be done with
the following:

*Existing User*
```bash
sudo adduser YOURUSERNAME dialout
```

*New User*
```bash
sudo usermod -a -G dialout NEWUSER
```

## Start-up
To run type the following from within the directory:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

