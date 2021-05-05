import network
import urequests 
import ssd1306
from ubinascii import hexlify
from machine import Pin, I2C

i2c = I2C(Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.fill(0)
oled.show()


key = 'AIzaSyASNzFneA1UhMykmm8VibDHZK4J1ziH01Q'
w_key = '&appid=4e8e219db3de74ce6562e6f56a7195d8'
w_link = 'http://api.openweathermap.org/data/2.5/find?'
link = 'https://www.googleapis.com/geolocation/v1/geolocate?key='

wifi_connection = None

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Fios-PsKV2', 'bey37bunt97pell')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    return sta_if

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def get_json_info(connection):
    connection_name = connection.config("essid")
    for points in connection.scan():
        if connection_name ==  points[0].decode():
            raw_add = hexlify(points[1]).decode()
            format_addr = raw_add[0:2] + ':' + raw_add[2:4] + ':' + raw_add[4:6] + ':' + raw_add[6:8] + ':' + raw_add[8:10] + ':' + raw_add[10:12]
            return (format_addr,points[2])
    return None

def formatJSON(mac,channel):
    header = {"Content-Type":"application/json"}
    json = {
            "macAddress":mac,
            "channel":channel
        }
    return (header, json)

wifi_connection = do_connect()
mac,channel = get_json_info(wifi_connection)
header,json = formatJSON(mac,channel)

request = urequests.request('POST',link+key,headers=header,json=json).json()['location']
cor = 'lat='+str(request['lat'])+'&'+'lng='+str(request['lng'])

weather_response = urequests.request('GET',w_link+cor+w_key).json()

oled.text(weather_response['weather']['description'],0,0)
oled.text(str(weather_response['main']['temp']-273.15)+' Celsius',0,8)
oled.show()




