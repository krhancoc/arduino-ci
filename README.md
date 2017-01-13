# Arduino Continuous Integration Server for Mac-OS/Linux
## Author: Kenneth Hancock

Pretty simple server to allow mutiple people to work on one Arduino chip my uploading to a server connected to the arduino chip.

**This tool is not completed yet -- Its very rough right now.**


## Requirements - Pre Start-up
1.  [Arduino App](https://www.arduino.cc/en/main/software)
2.  Python 2.7
3.  Pip 


### Dialout Group
Also make sure the user running the server -- whatever user you are using is added to the dialout group
so you don't get permission issues when the server tries uploading to the arduino.  This can be done with
the following:


**Mac**
```bash
dseditgroup -o edit -a USERHERE -t user dialout
```

**Linux**
```bash
sudo adduser USERHERE dialout
```

Log out and log in if you had to do this.

### Edit the ino.ini file
Inside the bin/ directory is a file called ino.ini, it is here you should edit so it matches the configuration you currently
have.  Meaning update the model and the serial port.

You can find the serial port by doing the following:  
1.  Open a terminal with the Arduino chip not connected  
2.  Type `df` you'll see a list of devices  
3.  Now connect your device and type `df` again, inspect where it has changed - that will be the arduino device  
4.  It should follow a pattern like /dev/ttyACM[0-9].  Once you know it. Copy and paste the filesystem column of the chip to where the file says SERIAL\_PORT  
## Start-up
To run type the following from within the directory:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```


### Issues That Can Happen

#### WiFi Library errors build process
There was a point where the program was having problems building with Ubuntu 16.04.1 LTS where the WiFi library that came with the chip was
causing it to error.  Delete or move this from its location (Probably will be in /usr/local/share/arduino/libraries/WiFi/ or
/usr/share/arduino/libraries/WiF, could be both).  The solution to the issue I found [here](https://github.com/amperka/ino/issues/119)


#### Problem with USB
This problem didn't specifically happen to me but I could see it happening.  If you have problems uploading might be a problem with communication
with your usb.  Check out a possible solution [here](https://www.arduino.cc/en/Hacking/DFUProgramming8U2)