from machine import Pin, I2C, RTC
import ssd1306
import socket
import network
import select
import json

i2c = I2C(Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
rtc = RTC()

show_clock = False;
timeout = 0

def display_time(time,cl):
    rtc = RTC()
    time = time.split('\\/')
    year = int('20'+time[0])
    month = int(time[1])
    time = time[2].split(' ')
    day = int(time[0])
    time = time[1].split(':')
    hour = int(time[0])
    minute = int(time[1])
    seconds = int(time[2])
    rtc.datetime((year, month, day, 1,hour,minute,seconds,0))
    print(rtc.datetime())
    date = []
    year_month_date = ''
    hour_min_seconds = ''
    readable = 0
    while True:

        readable = select.select([cl],[],[],0.5)
        date = list(str(x) for x in rtc.datetime()[0:7])
        year_month_date = date[0] + '/' + date[1] + '/' + date[2]
        hour_min_seconds = date[4] + ':' + date[5] + ':' + date[6]
        oled.fill(0)
        oled.text(year_month_date,0,0)
        oled.text(hour_min_seconds, 0, 10)
        oled.show()

def oled_greeting():
    oled.fill(0)
    oled.text("Stone-Watch", 20 ,16)
    oled.show()

def display_msg(msg):
    oled.fill(0)
    oled.text(msg,0,0)
    oled.show()

def response(message,cl):
    cl.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
    cl.send(message.encode())

def execute(command,time):
    if command.lower() == 'turn off':
        global show_clock
        show_clock = False
        oled.fill(0)
        oled.show()
        return '{\'response\': \'turn off success\'}'
    
    elif command.lower() == 'turn on':
        global show_clock 
        show_clock = False
        oled_greeting()
        return '{\'response\': \'turn on success\'}'

    elif command.lower() == 'display time':
        global show_clock
        show_clock = True
        timeout = 0.001
        time = time.split('\\/')
        year = int('20'+time[0])
        month = int(time[1])
        time = time[2].split(' ')
        day = int(time[0])
        time = time[1].split(':')
        hour = int(time[0])
        minute = int(time[1])
        seconds = int(time[2])
        rtc.datetime((year, month, day, 1,hour,minute,seconds,0))
        return '{\'response\': \'display time success\'}'
    
    elif command.lower() == 'stop clock':
        global show_clock
        show_clock = False
        return '{\'response\': \'stop time success\'}'
    
    elif 'display message ' in command.lower():
        global show_clock
        show_clock = False
        display_msg(command.split('display message ')[1])
        return '{\'response\': \'disaply message success\'}'
    
    return '{\'response\': \'invalid command\'}'
    

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


oled_greeting()
do_connect()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
print(addr)

s = socket.socket()
s.bind(addr)
s.listen(100)
print('listening on', addr)

read_list = [s]

while True:
    readable, writeable, errored = select.select(read_list,[],[],timeout)
     
    for soc in readable:
        if soc is s:
            cl, addr = s.accept()
            read_list.append(cl)
        else:
            timeout = 0
            msg = soc.recv(1024).decode()
            print(msg)
            data = msg.split('\r\n')[-1].split('\"')
            command = data[-2]
            time = data[3]
            response(execute(command,time),soc)
            soc.close()
            read_list.remove(soc)

    # cl.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
    # cl.send("message recieved".encode())
    if show_clock:
       
        date = []
        year_month_date = ''
        hour_min_seconds = ''
        date = list(str(x) for x in rtc.datetime()[0:7])
        year_month_date = date[0] + '/' + date[1] + '/' + date[2]
        hour_min_seconds = date[4] + ':' + date[5] + ':' + date[6]
        oled.fill(0)
        oled.text(year_month_date,0,0)
        oled.text(hour_min_seconds, 0, 10)
        oled.show()

        
    
    

