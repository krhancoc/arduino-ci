# Arduino Continuous Integration Server
## Author: Kenneth Hancock

Pretty simple server to allow mutiple people to work on one Arduino chip my uploading to a server connected to the arduino chip.

## This tool is not completed yet -- Its very rough right now.


## Requirements - Pre Start-up
1.  Arduino App 
2.  Python 2.7
3.  Pip 


### Dialout Group
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

Log out and log in if you had to do this.

### Edit the ino.ini file
Inside the bin/ directory is a file called ino.ini, it is here you should edit so it matches the configuration you currently
have.  Meaning update the model and the serial port.

You can find the serial port by doing the following:
1.  Open a terminal with the Arduino chip not connected  
2.  Type `df` you'll see a list of devices  
3.  Now connect your device and type `df` again, inspect where it has changed - that will be the arduino device  
4.  It should follow a pattern like /dev/ttyACM[0-9].  Once you it copy and past the "/dev/tty.." where the file says SERIAL\_PORT  
## Start-up
To run type the following from within the directory:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

