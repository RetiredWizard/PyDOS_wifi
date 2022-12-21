## PyDOS, PyBASIC, edit... All the functionality of the 1981 IBM PC on a PI Pico?

**MicroPython/CircuitPython DOS-like shell for microcontroller boards:**  
**(RP2040, ESP32, ESP32 PICO-D4, ESP32-S2/S3, nRF52840, SAMD51, stm32L4+, NXM ARM Cortex-M7)**  

**Check out the demo video at https://www.youtube.com/watch?v=Az_oiq8GE4Y**

To start the shell type **import PyDOS** at the REPL prompt.

At the PyDOS prompt a python program (.py) or batch (.bat) file can be run by simply entering the filename with or without
the extension.

**setup.bat** in the root folder, will prompt the user to indicate the board they are using.
The setup batch file will then copy the programs and libraries appropriate for the user's
 platform to the root and /lib folders of the Microcontroller flash.

## Implemented DOS Commands:  
(syntax and descriptions taken from https://home.csulb.edu/~murdock/dosindex.html)

PyDOS requires all switches to immediatly following the command with no spaces between the command or switches.

If a command argument contains spaces the argument must be enclosed in quotes.

**REM [comment]** - Used in batch files to insert remarks (that will not be acted on).

**DIR[/P][/W][/S] [path][filename]** - Displays directory of files and directories stored on flash.
- /P Pauses after each screenful of information (Q or C to abort listing)  
- /W Uses wide list format, displaying file/folder names only  
- /S Displays files recursively, traversing any subdirectories  

**DATE** - Displays the current date.

**TIME** - Displays the current time.

**MEM[/D]** - Displays available RAM and performs a garbage collection operation  
- /D Include debug information when supported by microcontroller board

**VER** - Displays PyDOS version

**ECHO [ON|OFF][message]** - Displays messages or turns on or off the display of commands in a batch file.

**PAUSE** - Suspends execution until a key is pressed.

**GOTO label** Causes unconditional branch to the specified label. (labels are defined as :label in batch files)

**IF [NOT] EXIST filename (command) [parameters]**  
**IF [NOT] (string1)==(string2) (command) [parameters]** - Allows for conditional operations in batch processing.  
**IF [NOT] ERRORLEVEL (number) (command) [parameters]**  

**SET[/P][/A] (variable)=[(string|prompt)]** - Inserts strings into the command environment. The set values can be used later by programs.  
- /A specifies that the string to the right of the equal sign is a numerical expression that is evaluated  
- /P displays the specified prompt string before setting the value of a variable to a line of input entered by the user  
*DOS specific environment variables:*
    - LIB - The Python search path for importing libraries (the current directory is always searched first but not included in the LIB variable)  
    - PATH - The directory search list for executing python scripts and DOS batch files (the current directory is always searched first but not included in the PATH variable)
    - PROMPT - The DOS prompt string
    - _scrHeight - The number of lines on the terminal or screen
    - _scrWidth - The number of columns on the terminal or screen
    - errorlevel - The result code from the previous BAT file or pexec command executed

**PROMPT [prompt text]** - Changes or displays the DOS command prompt. Supported strings "$R,$D,$T,$P,$G,$C,$F,$A,$B,$E,$H,$L,$Q,$S,$V,$_,$."  
**PATH [path1;path2;...]** - Changes or displays the directory search list for executing python scripts and DOS batch files

**RENAME (REN, MOVE, MV) [path]filename [path]filename** - Changes the filename under which a file is stored.

**DELETE (DEL)[/S] [path]filename** - Deletes files from disk.  
- /S Delete specified files from all subdirectories

**TYPE (MORE)[/P] [path]filename** - Displays the contents of a file.  
- /P Pauses after each screenful of information (Q or C to abort listing)

**CD [[d:]path]** - Displays working (current) directory and/or changes to a different directory.  
**CD ..** - Changes to parent directory of current directory.

**MKDIR (MD) path** - Creates a new subdirectory.

**RMDIR (RD)[/S] path** - Removes a subdirectory.  
- /S Removes all directories and files in the specified directory and the directory itself

**COPY[/Y] [path]filename [path][filename]** - copies files.  
- /Y Suppresses prompting to confirm you want to overwrite an existing destination file

**EXIT** - In a batch file returns to PyDOS, at PyDOS prompt terminates PyDOS and returns to REPL.

**PEXEC[/Q] [python command]** - Executes a single python command.
- /Q Supresses error message if error condition occurs (errorlevel variable is set)

An **autoexec.bat** batch file will automatically execute when PyDOS starts.

### External programs included:

**pydospins.py** - Displays the GPIO pins for sound output and I2C for the particular board PyDOS is running on.

**PyBasic.py** - a Basic interpreter from https://github.com/richpl/PyBasic. Tweaked and modified to run on Micropython and Circuitpython.
	basicparser.py, basictoken.py, flowsignal.py, lexer.py, program.py, basicdata.py
	
**runasthread.py** (Micropython only) - This program will attempt to launch a python program on the second RP2040 core. Threading is
experimental on Micropython so it's not difficult to crash the microcontroller using this program. I have not found a way to kill
a thread started on the second core so be sure any threads you launch will shutdown on their own or monitor a global variable or
thread.lock to respond to a shutdown request (see the badblink.py for an example).

**runvm.py** - This program is used to launch Python programs that require more memory
than is available while running PyDOS. **runvm** will write a **code.py**/**main.py**
file which launches the specfied python program after the next soft reboot. The program then
uses **supervisor.reload()** for CircuitPython or **sys.exit** for MicroPython to
perform a reboot (sys.exit requires a Ctrl-D to complete the operation). The specified python
program is "wrapped" in some code that passes any command line arguments and the PyDOS
environment variables to the newly booted environment as well as code that restores the
original **code.py**/**main.py** files and causes a second soft reboot returning control to
PyDOS.

**edlin.py** - line editor inspired by DOS edlin. Intial program structure of line editor by Joesph Long
    https://github.com/j-osephlong/Python-Text-Editor
    
**edit.py** - shell to load full screen editor from https://github.com/robert-hh/Micropython-Editor

**xcopy.py[/S][/Y][/V] [path]filename [path][filename]** - a more robust version of the copy command  
- /S Copies specified files from directories and subdirectories, except for empty ones  
- /Y Suppresses prompting to confirm you want to overwrite an existing destination file
- /V Performs a verification read of the copied file to ensure it matches the source

**fileview.py** - scrollable text file viewer

**sdmount.py [[mount path][,pydos spi bus#]]** - mounts an sd card to the file system  
**sdumount.py [mount path]** - dismounts an sd card from the file system

**setdate.py** - initalizes the real time clock to an entered date  
**settime.py** - initalizes the real time clock to an entered time  
**ntpdate.py** (ESP32xxx, Pico W and MicroPython Nano Connect) - sets the time and date using the Internet NTP protocol

**diff.py** - performs a file comparison

**sound.py** - outputs a sound to a speaker cicruit connected to GPIO pin defined in lib/pydos_bcfg.py  
**tsound.py** - test program that plays a short sound sequence  
**piano.py** - emulates a small piano keyboard

**i2cscan.py** - scans the I2C bus and displays any found device addresses

CircuitPython LCD libraries from https://github.com/dhylands/python_lcd  
**lcdprint.py** - displays text on an I2C LCD display  
**lcdscroll.py** - scrolls text on an I2C LCD display  
**temperature.py** - displays temperature value from onboard temperature sensor to screen and I2C LCD display

**basicpython.py** - Shell modeled after basic interpreter shell from https://github.com/tannewt/basicpython

**blink.py** - program to blink onboard LED

**rgbset.py** - program to set the rgb color of an onboard neopixel or dotstar  
**rgbblink.py** - program to blink an onboard neopixel or dotstar  
**rgbrainbow.py** - program to color cycle an onboard neopixel or dotstar  

**reboot.py** - performs a soft reboot (Micropython requires a Ctrl-D to complete)

**keys.bat** - (Keyboard Featherwing only) Displays keyboard mappings for hidden keys and functions  
**ui.bat** - (Keyboard Featherwing only) Switches between using the Keyboard Featherwing and USB Serial port for PyDOS I/O

**fs.py** - (Circuitpython only) By selecting the "RO" option the flash mode is set such that when the microcontroller
is power cycled or hard reset, the host computer will have read/write access to the flash and the microcontoller will be
restricted to read only access. To give PyDOS access to the flash after switching to this mode the boot.py file must be
replaced or modified from the host computer so that it contains the following instructions:

    import storage
    storage.remount("/",False)
    
and then power cycled or hard reset.


## Hardware (Pin) customization file (pydos_bcfg.py)


The setup.bat file will identify the board being used from **board.board_id** or
**sys.implementation._machine** and attempt to copy a customization file from the cpython or mpython /boardconfigs directory. If a matching config file is not found the default /lib/pydos_bcfg.py file will be used.

The pydos_bcfg.py file acts as a library which contains a single dictionary opject, Pydos_pins.

The recognized keys of the Pydos_pins dictionary are:  

**TUPLES (pin number, Text description of identified pin)**
led - Micropython may use text identifer (i.e. "led") rather than pin number
sndPin  
neoPixel  
neoPixel_Pow  
dotStar_Clock  
dotStar_Data  
dotStar_Extra  
dotStar_Pow  
I2C_NUM - MicroPython hardware I2C number  
SCL  
SDA  

**LIST OF TUPLES**
* First tuple in list used for machine/board SD dedicated SPI (board.SD_SPI)  
* Last tuple in list used for machine/board general use SPI (board.SPI)  
SPI_NUM - MicroPython hardware SPI number  
SCK  
MOSI  
MISO  
CS  

**CALCULATED DATA**

sndGPIO - digitalio.DigitalInOut(sndPin)  
KFW - Flag indicating use of Keyboard FeatherWing (True/False)  
I2CbbqDevice - I2C device being used for the KFW keyboard  
SD - list of sdcard objects  
SDdrive - list of mount points for mounted SD cards


## PyDOS Generalized Wifi API library (pydos_wifi.py)

Whenever possible PyDOS and the bundled external programs work equally well on MicroPython or CircuitPython and on any of the supported micro controller chip families. To assist in reaching this goal a simplified Wifi library is included which provides a unified Wifi API that works the same under both MicroPython and CircuitPython on ESP32xx, Pico W and Arduino Nano based Microcontrollers.

The currently exposed network API is:

*class* **PyDOS_wifi**

**NOTE:** PyDOS_wifi currently only support "station mode" activities.

Pydos_wifi:*PyDOS_wifi*

Instance of class object contained within the library available upon libary import.

esp:*adafruit_esp32spi.ESP_SPIcontrol*

adafruit_esp32spi.ESP_SPIcontrol object when run in CircuitPython on a Arduino Nano Connect, None in all other cases.

ipaddress:*str*

IP address obtained by microcontroller board after connecting to a network.

response:*class response*

Native *response* object after the most recent Pydos_wifi.get(url) call.

timeout=15000:*int*

Timeout in milliseconds used for network operations when option is available in native API.

wlan:*network.WLAN(network.STA_IF)*

Station network.WLAN object when run in MicroPython, None in CircuitPython.

connect(*,ssid:*str*,passwd:*str*) -> *bool*

Attempts to connect to an access point using the passed in ssid and password.

get(*,text_url:*str*,headers:*dict*=None,getJSON:*bool*=False) -> *class response*

Sends an html *GET* command to either port 80 or 443, depending on the HTTP(S) included in the text_url. The specific class of the returned response varies depending on; which Python is running, if the **getJSON** flag is set and if a wifi coprocessor is being utilized. The Pydos_wifi methods **next** and **json** can be used to access the response data without regard to the Python version or microcontroller board type.

When running MicroPython, if the **json** method is going to be used to access the response, the **getJSON** flag must be set to True. If the **next** method is going to be use **getJSON** must be False. On CircuitPython, the **getJSON** parameter isn't required but may be used for compatibility.

Once a response has been retrieved via a call to *get* another call to *get* cannot be made without a closing the response. The response can be closed directly using *response.close()* if the native response supports it (MicroPython and non-coprocessor CircuitPython boards) but attempting to close a CircuitPython response directly currently results in the stream being read until it ends or times out which unless the retrieved html stream is relativly small may effectivly hang the board. *Pydos_wifi.close()* can be used in all cases without hanging the board but requires reconnecting to the AP using *Pydos_wifi.connect* after its use.

getenv(*,tomlKey:*str*) -> *str*

Returns the value associated with the *tomlkey* parameter retrieved from the settings.toml file (or .env file if settings.toml doesn't exist) - depreciated, will be removed in the future.

is_connected(*) -> *bool*

Flag indicating whether microcontroller is currently connected to an access point/network.

json(*) -> *dict*

When using MicroPython, the previous **get** must have been called with the getJSON flag set to True.

Returns the HTTP content parsed into a json dictionary. This attempts to read all available content and parse it as json. If the data is larger than will fit into memory or is not properly formatted the operation will fail (not gracefully... :).

next(*,size:*int*=256) -> *bytes*

When using MicroPython, the previous **get** must have been called with default getJSON value or getJSON set to False.

Returns the next *size* bytes of the HTTP content as bytes. This is useful in scanning HTTP streams that are larger than would fit in available microcontroller memory.

When using MicroPython, reads attempting to get more data than is available will hang the board (for at least 60 seconds). Either make sure the *size* of data read is less than is available in the stream or set *size* to a single byte (1). If there is no data available to read when the next method is called it will return a btye string of length zero (b'') after Pydos_wifi.timeout milliseconds have elapsed. The zero length byte string can be tested for in order to determine the end of data within a loop, assuming you are reading just one byte at a time. **Note** reading the stream one byte at a time is considerably slower than reading larger chunks.


The following example programs should run unmodified on ESP32/Pico W/Nano Connect boards running either CircuitPython or MicroPython.

**EXAMPLE WIFI PROGRAM**

from pydos_wifi import Pydos_wifi  
ssid = Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID')  
pswd = Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')  
result = Pydos_wifi.connect(ssid, pswd) 
text_url = "http://wifitest.adafruit.com/testwifi/index.html"  
response = Pydos_wifi.get(text_url)  
# since not using ssl can read data without testing for end of stream  
print(Pydos_wifi.next(1000).decode('utf-8'))  
Pydos_wifi.close()  


**EXAMPLE READING SSL DATA**

from pydos_wifi import Pydos_wifi  
# .5 second timeout, Pydos_wifi.next will wait this long before returning b''  
# if this is too short, could find false end of data on slow networks  
Pydos_wifi.timeout = 500 # default is 15000 (15 seconds)  
ssid = Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID')  
pswd = Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')  
result = Pydos_wifi.connect(ssid, pswd) 
text_url = "https://httpbin.org/get"  
response = Pydos_wifi.get(text_url)  
# If running on CircuitPython this loop can be replaced with **getRes = Pydos_wifi.next(1000)**  
getRes = b''  
nxtByte = None  
while nxtByte != b'':  
    nxtByte = Pydos_wifi.next(1)  
    getRes += nxtByte  

print(getRes.decode('utf-8'))  
Pydos_wifi.close()  


## Installation

If the board you're using has limited flash storage you can delete either the **cpython** (if you're not using CircuitPython) or **mpython**
(if you're not using MicroPython) folder from the downloaded repository files. Within the remaining Python folder (**cpython** or **mpython**) are folders
for specific micro controller boards, you can free up further space by deleting anything other than the board you are using (the "Pico W" and "Arduino Nano Connect" boards use the ESP folder). Finally, after running
the **setup.bat** file in PyDOS you can delete both the **cpython** and **mpython** folders as they are only used by the **setup.bat**
script. For very limited Flash boards you may want to delete the **PyBasic** folder until after setup is run. Once setup has ben run, delete the **cpython** and/or **mpython** folders from
the microcontroller and copy as much of the **PyBasic** directory as space permits, copying just the *.py files is all that's needed for PyBasic to run.

**Building custom CircuitPython firmware**

For CircuitPython the first thing you should do is compile a custom CircuitPython image, the steps for doing so are described in the Adafruit learning guide
at: https://learn.adafruit.com/building-circuitpython/build-circuitpython.  Upon downloading the latest version of CircuitPython from the github repository,
modify the **py/circuitpy_mpconfig.h** file and change the value on the line that reads "#**define MICROPY_ENABLE_PYSTACK**" from "(1)" to "(0)". On an 
ESP32S2 microcontroller it's also necessary to modify the **py/mpconfig.h** file and change the value on the line that reades "**#define MICROPY_STACKLESS**"
from "(0)" to "(1)". You can find custom UF2 images for some boards as release resources here: https://github.com/RetiredWizard/PyDOS/releases. If you're using a board not included you
can open a Github issue on this repository to request it.

An earlier version of the build process is demonstrated in the YouTube video at: https://www.youtube.com/watch?v=sWy5_B3LL8c, but be sure to check the Adafruit
guide and use the updated instructions.

**PyDOS will run without using this custom CircuitPython image however PyBasic and some of the other applications will not run as well since PyDOS will be memory limited.**

**CircuitPython Setup**

To install the custom CircuitPython image, put your microcontroller board in "bootloader" mode and copy the compiled .UF2 file to the USB mass storage device that
shows up on your host computer.

After the .UF2 file is copied to the microcontroller board it should re-boot and a new USB mass storage device should appear. 

To copy PyDOS to the Microcontroller, simply drag the PyDOS directory structure
(after removing the **mpython** folder if space is a concern) to the root directory of the device that appears on the host computer.
Your microcontroller now has PyDOS installed.

If the copy worked without any errors, you should power cycle the microcontroller board so that the file system is configured to allow
the microcontroller to have Read/Write access.

**PyDOS has Read/Write access and the host computer will only have ReadOnly access. This change won't take effect until you have completed the power cycle mentioned above, so be
sure that the PyDOS files are all copied before turning the power off on your microcontroller board. If the copy is interrupted for any reason you can delete the boot.py
file in the root of the microcontroller flash and try the copy again. 

If you find yourself locked out of the flash from the host computer and PyDOS is not running, the easiest way to recover is to
connect to the REPL, remove the boot.py file and then power cycle the microcontroller board. 

        import os
        os.remove("boot.py")
**
To interact with the microcontroller you will need to connect using a terminal program. On a PC you can use putty and on linux minicom works well. To start minicom
on linux type the command:

          Term=linux minicom -b 115200 -o -D /dev/ttyACM0
	  
You should be presented with the REPL prompt (>>>), if not, press return or Ctrl-C.

At the REPL prompt type "**import PyDOS**" to start PyDOS and then type **setup** to run the customization script.

--------------------------------------------------------------------------------------------------------------------
**Building custom Micropython firmware**

Although you can use a standard Micropython image downloaded from Micropython.org to run PyDOS, there are two reasons you may want to build a custom
Micropython firmware file. 

The first is if you wan to connect up an old school serial terminal to the REPL rather than the standard serial over USB connection. Instructions for building 
Micropython with this modification can be found in section 2.2 of the Raspberry Pi Pico Python SDK at https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf.

The second is that PyDOS uses a recursive routine to process wildcard operations and the default stack in Micropython limits the recursion depth that can be obtained **(With more recent versions of Micropython this has become much less of an issue)**.
This means that PyDOS has to limit wildcard operations, one impact of this is that files with longer file names may not appear
in directory listings when wildcards are used. To eliminate this issue a custom Micropython image can be built with the the MICROPY_STACKLESS parameter in **py/mpconfig.h**
changed from **0** to **1**. 

**MicroPython Setup**

Once your microcontroller has Micropython installed and running the best way
to copy the PyDOS files and interact with the repl is to use Thonny. Adafruit has a good learning guide for getting started with Thonny here:
https://learn.adafruit.com/circuitpython-libraries-on-micropython-using-the-raspberry-pi-pico/micropython-installation. 

Download PyDOS from the github repository and after deleting the **cpython** folder if space is an issue, use the Thonny upload command as described in the Adafruit 
learning guide to copy the downloaded files to the microcontroller.

To interact with the microcontroller connect over the serial USB port (COMn: /dev/ttyACMx, etc) using a terminal program like puTTY or minicom. You can use the Thonny shell as well
however, it does not support the basic ansi escape sequences used by some of the PyDOS functions.
One thing to note is that if you
connect to your microcontroller with a terminal program after using Thonny, you may need to press CTRL-B to exit the raw REPL mode that 
Thonny uses to transfer and execute files.

Another option is to use MPRemote. Detailed documentation on installing and using MPRemote can be found 
at https://docs.micropython.org/en/latest/reference/mpremote.html.

To install PyDOS on the microcontroller board download PyDOS from the github repository and after deleting the **cpython** folder if space is an issue, set your current
directory to the root folder of the downloaded PyDOS repository and use the following command:

	mpremote fs cp -r * :
	
To interact with the microcontroller you can connect to the REPL by simply typing **mpremote** and pressing return several times until the REPL prompt
(>>>) is displayed.

At the REPL prompt type "**import PyDOS*** to start PyDOS and then type **setup** to run the customization script.


**To Do**
*Possible updates depending on RAM impact*

- support for connected color displays  
- support for touch screens  
- Rename should allow wildcards in filenames, i.e. "rename *.bas *.txt" or "rename code.py *.sav"  
- Quiet, /Q switches to DEL, RMDIR, COPY, XCOPY commands
- PgUp/PgDwn support in fileview.py
