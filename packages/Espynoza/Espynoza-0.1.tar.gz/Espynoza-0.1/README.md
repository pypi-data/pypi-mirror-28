# Remark:
**Info will be completed a.s.a.p., but if you happen to stumble on this project, feel free to use.**


Please be patient, doc. will be worked on before first public announcement

# Introduction
Espynoza is a framework for writing, configuring and managing applications on ESP8266 microcontroller boards.

Espynoza supports remote uploading of files/sources via USB cable, or via Wifi/MQTT once the basic software is installed. Multiple MQTT servers may be configured as well as distinct Wifi Access Points.

All user actions are made through a command-line interface, *Espynoza.py* (use --help for details). Configuration is made via Python files (basically variable assignments). Configuration files exist on the global level, as well as for the individual target devices.

The framework, running on the target device, handles initial connection to the Wifi network, and then establishes a connection with the specified MQTT broker. The host server may then send commands to the target device, using standard Python syntax, and will receive data produced on the target. The frameworks main loop calls (user-definable) handlers to perform actions such as setting outputs and reading sensor data. A watchdog will reboot the target if the board hangs.

Right now, some simple sample handlers are provided with Espynoza, more will follow soon. The aim is to create a library that will allow the user to build a system by writing a configuration file for simple cases, but that may be extended by writing small code fragments in Python for more special cases.

Special care has been been taken to use as little memory as possible on the target devices. Python files may be compiled on the host system before being uploaded to avoid out of memory conditions during system startup. Only the files needed for the targets configuration are loaded into RAM.

(BTW, in case you wonder why some things are designed the way they are, I plan to write a web/database-based application to make using Espynoza easier. But first things first...)

## Version
Current version is *0.1*, the initial commit.
This version should be considered alpha quality, even though the code should work if Espynoza and all needed libraries and tools are installed correctly.
Right now, the number of available handlers is limited to simple digital and analog IO, as well as some I2C or similar serial communication protocol devices. More will follow as soon as the basic code is stable.

# Download and Install
## Requirements
* Hardware
  * Host computer
    * PC running Linux (maybe other OS)
    * or a Raspberry Pi running Linux (Ubuntu Jessie works)
    * Python >= 3.6 (3.6 minimum, as format strings are used)
  * Target
    * ESP6288
    * (more to come)

* Software packages
  * git
  * MicroPython
  * Mosquitto (and paho-mqtt)
  * ampy (from Adafruit)
  * esptool.py
  * (esp-open-sdk -- optional, needed to build custom runtimes, no support yet)

## Install

*Remark*: the following instructions worked for me, your mileage may vary. Please drop me a note if you have problems, I will try to help, and amend these instructions.

**Espinoza**: clone Espynoza from GitHub using this command:
```
git clone https://github.com/finalstate/Espynoza.git
```
This will create a directory called Espynoza containig the Espynoza.py cli tool, a basic configuration file and a number of sub-directories.

Moreover you will need to install the following packages to use Espynoza. Install them in some convenient place on your disk, not into the Espinoza directory.

**MicroPython**: the MicroPython language files, and its compiler. Install this using Github, and build the compiler yourself (the pre-build one provided for download is notoriously out of date, and your code might not work with it):
```
git clone https://github.com/micropython/micropython.git
cd micropython/mpy-cross
make
```
This will create the mpy-cross compiler executable. Open the file *EspyConfig.py* in the Espynoza root directory. There you will find the following line:
```
C_MpyCross = './bin/mpy-cross'
```
You may either change this to point to your brand-new compiler, or create the bin sub-directory and create a symbolic link to the compiler in this directory (or use your own strategy, Espynoza is designed to be flexible).

**Mosquitto**: the MQTT broker used as a communication hub for Espynoza (and potentially many more sub-systems of your IoT installation.)

If you use Debian or Ubuntu, the following should work:

```
sudo su
apt-get update
apt-get upgrade
apt-get install mosquitto mosquitto-clients
```

Please refer to the mosquitto documentation for configuration and usage. The out-of-the-box config should be OK if you are happy without security settings...

## Clone from GitHub

*Remark*: the following instructions worked for me, your mileage may vary. Please drop me a note if you have problems, I will try to help, and amend these instructions.

**Espinoza**: clone Espynoza from GitHub using this command:
```
git clone https://github.com/finalstate/Espynoza.git
```
This will create a directory called Espynoza containig the Espynoza.py cli tool, a basic configuration file and a number of sub-directories.

Moreover you will need to install the following packages to use Espynoza. Install them in some convenient place on your disk, not into the Espinoza directory.

**esptool**: This tool is used to flash the target flash memory, and to upload the MicroPython firmware
```
sudo pip3 install esptool
```

**ampy**: This library is used to initially upload Python files to the target board. Install like this:
```
sudo pip3 install adafruit-ampy
```

**paho-mqtt**: a Python library for using MQTT. Again, we install using pip:

```
sudo pip3 install paho-mqtt
```

# Tutorial
Here is a simple tutorial to get you started with Espynoza. First, we will set up some basic hardware, and then install the software on it to get a feeling for how Espinoza works and what it can do for us.

## Hardware setup
You need to get hold of an ESP6288 development board. Any board that has a USB port for uploading should work. We will, for the purpose of this tutorial, connect an LED to Port xxx to play with output lines, and a simple wire to Port yyy to try out input lines. Please note that we will use the Dnn numbering scheme as printed on (most?) boards when dealing with hardware, but will use the pin numbers as used in the official ESP documentation when writing software.

## Software configuration
Lets try to keep this simple for now. EspyConfig.py should be OK for this tutorial if you dont have done anything special during installation. Lets go into the *etc/* sub-directory. There, we find a file called *DemoDeviceList.py*. (We may use it as is, or we may make a copy of it that we call *DeviceList.py*. The later will be used if it exists. Do this if you do not want to run into problems when pulling the newest Espinoza library).

Open this file in your preferred text editor. It contains the configuration of your IoT installation as a whole. Later on, we will see how an individual target device is configured. We will need to make some changes in this file, specifically the Wifi and MQTT settings, and the basic settings of our target devices.

So, lets start with WiFi setup. Change the following network settings so they fit your local network:
```python
C_Network = {
              'DNS'     : '192.168.1.1', 
              'Gateway' : '192.168.1.1',
              'Netmask' : '255.255.255.0',
            }
```

In this tutorial, we will suppose that you have a single Wifi router. Uncomment the following line (leave the first one as is, it doesn't bother us right now), and change the name of the Hotspot and the Password to your settings:
```python
C_WifiPasswords = {
                    ''         : '**PWD**',
                  
#                   'HotSpot1' : '**PWD**',
                  }
```

If your MQTT broker is configured to use a login and password, comment the first line, and uncomment the second one. Change the IP address you see to the one used by your MQTT broker. Change login and password if appropriate.
```python
C_MQTTCredentials = {
                      '192.168.1.99' : (None,   None     ),
#                     '192.168.1.98' : ('esp', '*******' ),
                    }
```

And finally, we need to add our target to the device descriptor. Copy one of the lines and modify it like this:
```python
C_DeviceDescriptor = {
                      # Target     : (Config,      AP, IP Address,      Broker,          Description                ),
                        'Tutorial' : ('Tutorial',  '', '192.168.1.42',   '192.168.1.99', 'Tutorial board'           ),
                                                   
                        'SimpleIO' : ('SimpleIO',  '', '192.168.1.100', '192.168.1.215', 'Blink and rotary encoder' ),
                     ...
```
Change the dictionaries key to the name you want to give to your board. The associated parameter list begins with the name of the target configuration that we will define below. Here, we give it the same name as the target, but if you have several targets that use the same configuration (such as temperature sensors in different rooms), you may use different target board names, and reuse the same configuration file. Next comes the SSID name of the Access Point you want the device to connect to. Then, find and enter an address in your LAN that is not used, here, I used 192.168.1.42. The second quad.dot.address is the address of the broker this particular board uses, change it to the one you used above. Finally, there is a string describing the board, change it to whatever you like, it is currently only used for documentation purposes.

Btw, if you leave the AP name empty, the target will scan the Ether for access points and try to use those found, one by one, starting with the strongest, until a connection works. Of course, you will then need to set the password for the Access Point in the *<Demo>DeviceList.py* file, and booting the board will take longer. Also, more RAM will be used. But hey, it will work, and having multiple access points for redundancy, or better signal coverage, also has its advantages. (Unfortunately, right now, with auto-detection, all access points must have the same password. Stay tuned...)

Save the file, it should be OK for now. But we are not done yet with the configuration...

Make a copy of file *Newbie.py*, name it *Tutorial.py*. That's to say, use the config name you defined in the *<Demo>DeviceList.py* file. Open this file in your editor, and change the following items:
**C_Handlers**: we will configure our IO here. Insert the following lines:
```python
C_Handlers = {
               'DigitalOut': { 'Period' : 250,   'Params' : (('Led',    True ), ) }
               'DigitalIn' : { 'Period' :    1,  'Params' : (('Wire',    500 ), ) },
             }
```
Now, what does this mean. Lets see item by item.

*DigitalOut* and *DigitalIn* are handler names. Think of them as drivers for your input and output devices. If you are curious, see the files *DigitalOut.py* and *DigitalIn.py* in the *usr/* directory.

The 'Period' parameter indicates how often the handlers 'periodic' method should be called. It is the number of milliseconds that the target should wait between two calls to the handlers 'periodic' method. The *DigitalOut* handler will blink the Led we connected every 500 ms (250 ms between individual togglings), and the *DigitalIn* pin will be read every millisecond.

Next, we have the Parameters. These are different for all handlers, see the source file of the given Handler for a description. For *DigitalOut*, they are: The pin name to use, and if the Led should blink. We will see later what else than blinking we can do with this handler. *DigitalIn*s first parameter is also the pin name. The second parameter is used for debouncing, any changes happening at intervals (in milliseconds) shorter than this will be ignored.

**C_Pins**:
Finally, we need to define our pins:
```python
# Pin  : ESP pin id, 
# Mode : 0=IN | 1=OUT | 2=OPEN_DRAIN, 
# Value: if  IN: 1=PULL_UP | None=None)
#        if OUT: 0=OFF | 1=ON | None=leave (default state)
C_Pins = {
           'Led'  : (0,  1, 0), 
           'Wire' : (1,  0, None),
         }
```

This dictionaries keys are the names of the Pins, as we used them above. The first parameter is the pin number. Here, we use the Espressif numbering, not the Dx stuff from the Arduino world. The second parameter defines if the pin is used as an Input or as an Output. Finally, the 'Wire' input pin has a third value which indicates whether it is configured as a PULL_UP input or not.

And this concludes the configuration of our target. Next, we need to get it on our target, and then we may finally play with it.

## Running it
First, we need to prepare the board, i.e. flash it and upload the firmware. This is, of course, only possible via an USB connection, so we need to plug the board into the computer running Espynoza. Once we have done this, we execute the following command:
```
./Espynoza.py -t Tutorial -v --usb --flash
```
We pass the following parameters:
  * -t Tutorial -> This is the name of the board, and _not_ the the configuration name
  * -v -> verbose. We get some information about what the tool is currently doing
  * --usb -> upload via USB.
  * --flash -> the command, here telling the tool to flash and init the board

Btw, if you want to see the commands and options the tool implements, simply type
```
./Espynoza.py --help
```
Flashing the target takes some time, so be patient.

Once the flashing done, we are ready to transfer the base software. Make sure your Mosquitto instance is running, it will be used from now on. The first time, we still need to do this over USB, however, so here we go
```
./Espynoza.py -t Tutorial -v --usb --base
```
Again, this takes some time, but now, we get a more fine-grained status report. Please be aware that this step may fail from time to time, as ampy, the tool used for the serial/USB transfer, is not very reliable. If you get an error, simply try again, normally it works on second or third attempt.


The board is automatically rebooted when done. If your board has the blue status light, it will blink during boot, and stay out once a Access Point has been contacted. If you monitor your MQTT traffic, you will notice some messages coming from your board. Try it with this command (add username/password if necessary):
```
mosquitto_sub  -v -q 1 -t '#'
```

We're almost done now. For one thing, we will no longer need the USB connection, so you may connect your board to a simple power supply if you like.

What still needs to be done is the uploading of the handlers. We do this with the following command:
```
./Espynoza.py -t Tutorial -v --handlers
```
Notice that we no longer use the --usb option, we are now 'over the air'. If you monitor MQTT traffic, you will also see _a lot_ of traffic, some strange stuff. This is your handlers, pre-compiled on your host. Python sources, with the exception of the main.py stub, is by default pre-compiled, if you prefer the put the raw sources onto your target, for whatever reason, use the --source option.

Oh, and if you want to reload the base software onto the target, you may do so OTA now.
```
./Espynoza.py -t Tutorial -v --base
```
You may change and upload the configuration with
```
./Espynoza.py -t Tutorial -v --configure
```
again OTA.

If you connected your Led correctly, it should blink now, at 2Hz. Try changing this frequency, change the configuration and upload it. The board should automatically reboot, and the tool should show the progress.

Connecting your input wire to the 3V or GND pin should trigger some message sending. If so, input also works. Play around with the debouncing interval...

But there is more: we can interactively play with the system, OTA:
```
./Espynoza.py -t Tutorial -v -c "1+2"
```
This returns the result, 3. And
```
./Espynoza.py -t Tutorial -v -c "gc.mem_free()"
```
tells us how much memory is still available on the target. In fact, we may execute any legal Python statement using Espynoza.py. And this is also the way to interact with the IO drivers. Execute:
```
./Espynoza.py -t Tutorial -v -c "User.Handlers['DigitalOut']['Handler'].set('Led',1)"
```
This will put the Led on. Well, it would, but the Led blinks. So, switch of the blinking in the configuration file *Tutorial.py*, reload the config, and try again. And passing 0 to the set function turns it of again.

Have a look at your MQTT output. You will find this line:
```
esp/SimpleIO/cmd User.Handlers['DigitalOut']['Handler'].set('Led',1)
```

The topic is _esp/SimpleIO/cmd_ and the message is the Python code that puts the Led on. Sending this command using _any_ MQTT client will put the Led on. Do you have a MQTT client on your smartphone? Try it out. Perhaps not the most user-friendly way for IoT interactions, put I am sure you see the potential.

Have a look at the file *usr/DigitalOut.py*. As you can see, set(...) is a method of the handler. There is also a toggle method. Try it out using Espynoza.py. Add your own method to DigitalOut, and try it. Or better, copy the handler to another file, change your config to use your version instead and then modify your private copy. This will avoid loosing your work when upgrading Espinoza.

## Troubleshooting
To be completed 


# Architecture overview
## File organization

# Reference

# Contributing

# Known issues
- out of order file chunk transfers
- dir name ESP is sub-optimal

# Upcoming
(help welcome :-) )

* custom firmware building support
* https support for mqtt connections
* cli commands: rename board, move target to another broker

* ESP32 support (if and when MicroPython supports the stuff needed)
