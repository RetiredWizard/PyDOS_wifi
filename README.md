## PyDOS Generalized Wifi API library (pydos_wifi.py)

Whenever possible PyDOS and the bundled external programs work equally well on MicroPython or CircuitPython and on any of the supported micro controller chip families. To assist in reaching this goal PyDOS_wifi, a simplified Wifi library, is being developed which provides a unified Wifi API that works the same under both MicroPython and CircuitPython on ESP32xx, Pico W and Arduino Nano based Microcontrollers.

The currently exposed network API is:

*class* **PyDOS_wifi**

**NOTE:** PyDOS_wifi currently only support "station mode" activities.

`Pydos_wifi:`*`PyDOS_wifi`*

Instance of class object contained within the library available upon libary import.

`esp:`*`adafruit_esp32spi.ESP_SPIcontrol`*

adafruit_esp32spi.ESP_SPIcontrol object when run in CircuitPython on a Arduino Nano Connect, None in all other cases.

`ipaddress:`*`str`*

IP address obtained by microcontroller board after connecting to a network.

`response:`*`class response`*

Native *response* object after the most recent Pydos_wifi.get(url) call.

`timeout=15000:`*`int`*

Timeout in milliseconds used for network operations when option is available in native API.

`wlan:`*`network.WLAN(network.STA_IF)`*

Station network.WLAN object when run in MicroPython, None in CircuitPython.

`connect(*,ssid:str,passwd:str) -> `*`bool`*

Attempts to connect to an access point using the passed in ssid and password.

`get(*,text_url:str,headers:dict=None,getJSON:bool=False) -> `*`class response`*

Sends an html *GET* command to either port 80 or 443, depending on the HTTP(S) included in the text_url. The specific class of the returned response varies depending on; which Python is running, if the **getJSON** flag is set and if a wifi coprocessor is being utilized. The Pydos_wifi methods **next** and **json** can be used to access the response data without regard to the Python version or microcontroller board type.

When running MicroPython, if the **json** method is going to be used to access the response, the **getJSON** flag must be set to True. If the **next** method is going to be use **getJSON** must be False. On CircuitPython, the **getJSON** parameter isn't required but may be used for compatibility.

Once a response has been retrieved via a call to *get* another call to *get* cannot be made without a closing the response. The response can be closed directly using *response.close()* if the native response supports it (MicroPython and non-coprocessor CircuitPython boards) but attempting to close a CircuitPython response directly currently results in the stream being read until it ends or times out which unless the retrieved html stream is relativly small may effectivly hang the board. *Pydos_wifi.close()* can be used in all cases without hanging the board but requires reconnecting to the AP using *Pydos_wifi.connect* after its use.

`getenv(*,tomlKey:str) -> `*`str`*

Returns the value associated with the *tomlkey* parameter retrieved from the settings.toml file (or .env file if settings.toml doesn't exist) - depreciated, will be removed in the future.

`is_connected(*) -> `*`bool`*

Flag indicating whether microcontroller is currently connected to an access point/network.

`json(*) -> `*`dict`*

When using MicroPython, the previous **get** must have been called with the getJSON flag set to True.

Returns the HTTP content parsed into a json dictionary. This attempts to read all available content and parse it as json. If the data is larger than will fit into memory or is not properly formatted the operation will fail (not gracefully... :).

`next(*,size:int=256) -> `*`bytes`*

When using MicroPython, the previous **get** must have been called with default getJSON value or getJSON set to False.

Returns the next *size* bytes of the HTTP content as bytes. This is useful in scanning HTTP streams that are larger than would fit in available microcontroller memory.

When using MicroPython, reads attempting to get more data than is available will hang the board (for at least 60 seconds). Either make sure the *size* of data read is less than is available in the stream or set *size* to a single byte (1). If there is no data available to read when the next method is called it will return a btye string of length zero (b'') after Pydos_wifi.timeout milliseconds have elapsed. The zero length byte string can be tested for in order to determine the end of data within a loop, assuming you are reading just one byte at a time. **Note** reading the stream one byte at a time is considerably slower than reading larger chunks.


The following example programs should run unmodified on ESP32/Pico W/Nano Connect boards running either CircuitPython or MicroPython.

**EXAMPLE WIFI PROGRAM**
```py
from pydos_wifi import Pydos_wifi  
ssid = Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID')  
pswd = Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')  
result = Pydos_wifi.connect(ssid, pswd) 
text_url = "http://wifitest.adafruit.com/testwifi/index.html"  
response = Pydos_wifi.get(text_url)  
# since not using ssl can read data without testing for end of stream  
print(Pydos_wifi.next(1000).decode('utf-8'))  
Pydos_wifi.close()  
```

**EXAMPLE READING SSL DATA**
```py
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
```