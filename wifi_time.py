import sys
import time
from pydos_wifi import Pydos_wifi

if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import rtc

def wifi_time(passedIn=""):
    envVars['errorlevel'] = '1'

    if Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID') is None:
        raise Exception("WiFi secrets are kept in settings.toml, please add them there by using setenv.py!")

    if not Pydos_wifi.connect(Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'), Pydos_wifi.getenv('CIRCUITPY_WIFI_PASSWORD')):
        raise Exception("Wifi Connection Error")

    print("Connected to %s!" % Pydos_wifi.getenv('CIRCUITPY_WIFI_SSID'))
    # We should have a valid IP now via DHCP
    print("My IP address is", Pydos_wifi.ipaddress)

    print("Attempting to set Date/Time")

    response = Pydos_wifi.get("http://worldtimeapi.org/api/ip",None,True)
    time_data = Pydos_wifi.json()

    if passedIn == "":
        tz_hour_offset = int(time_data['utc_offset'][0:3])
        tz_min_offset = int(time_data['utc_offset'][4:6])
        if (tz_hour_offset < 0):
            tz_min_offset *= -1
    else:
        tz_hour_offset = int(passedIn)
        tz_min_offset = 0

    unixtime = int(time_data['unixtime'] + (tz_hour_offset * 60 * 60)) + (tz_min_offset * 60)
    ltime = time.localtime(unixtime)

    if sys.implementation.name.upper() == "MICROPYTHON":
        machine.RTC().datetime(tuple([ltime[0]-(time.localtime(0)[0]-1970)]+[ltime[i] for i in [1,2,6,3,4,5,7]]))
    else:
        rtc.RTC().datetime = ltime

    print("\nTime and Date successfully set")
    envVars['errorlevel'] = '0'

    Pydos_wifi.close()

if __name__ != "PyDOS":
    passedIn = input("Enter your current timezone offset (enter for default): ")
    if 'envVars' not in dir():
        envVars = {}

wifi_time(passedIn)
