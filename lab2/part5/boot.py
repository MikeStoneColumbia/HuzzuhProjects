from machine import Pin, I2C
import ssd1306
import time
import ustruct

scl = Pin(14)
sda = Pin(12)
cs = Pin(13, Pin.OUT)
cs.value(1)
i2c_accel = I2C(scl = scl, sda = sda, freq = 10000)

i2c = I2C(Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

device = i2c_accel.scan()
slave_address = ''

for item in device:
    arr = i2c_accel.readfrom_mem(item,0,1)
    if arr[0] == 0xe5:
        slave_address = item
        break

def write(addr, info):
    arr = bytearray([info])
    i2c_accel.writeto_mem(slave_address, addr, arr)

def read(addr):
    return i2c_accel.readfrom_mem(slave_address,addr,1)

def getVals():
    format = '<h'
    arr1 = read(0x32)
    arr2 = read(0x33)
    buf = bytearray([arr1[0], arr2[0]])
    x, = ustruct.unpack(format,buf)
    x = x*3.9

    arr1 = read(0x34)
    arr2 = read(0x35)
    buf = bytearray([arr1[0], arr2[0]])
    x, = ustruct.unpack(format,buf)
    y = x*3.9

    arr1 = read(0x36)
    arr2 = read(0x37)
    buf = bytearray([arr1[0], arr2[0]])
    z, = ustruct.unpack(format,buf)
    z = z*3.9

    return (x,y,z)

write(0x31, 0x2B)
write(0x2c,0x0A)
write(0x2E,0x00)
write(0x1e,0x00)
write(0x1f,0x00)
write(0x20,0x00)
write(0x2d,0x28)
time.sleep(1)

text = 'Part 5'
text_len = len(text) * 8
x_cor = 40
y_cor = 12
oled.text(text, x_cor, y_cor)
oled.show()

def scroll_up():
    global y_cor
    oled.fill(0)
    if y_cor == 0 or y_cor - 8 < -9 :
        y_cor = 32
    else:
        y_cor -= 4

    oled.text(text,x_cor, y_cor)
    oled.show()

def scroll_down():
    global y_cor

    oled.fill(0)
    if y_cor + 4 > 33:
        y_cor = 0
    
    y_cor += 4
    oled.text(text,x_cor, y_cor)
    oled.show()

def scroll_left():
    global x_cor
    oled.fill(0)
    print(x_cor)
    if x_cor - 4 < -text_len - 1:
        x_cor = 128
    else:
        x_cor -= 4
    oled.text(text,x_cor, y_cor)
    oled.show()

def scroll_right():
    global x_cor
    oled.fill(0)
    #print(x_cor)
    if x_cor + 4 > 129:
        x_cor = 0
    else:
        x_cor += 4
    oled.text(text,x_cor, y_cor)
    oled.show()

while True:
    print(getVals())
    x_val, y_val, z_val = getVals()

    if y_val > 0 and y_val - x_val > 200 and z_val < 900:
        scroll_up()
    
    elif y_val < 0 and abs(y_val) - x_val > 200 and z_val < 900:
        scroll_down()
    
    elif x_val > 0 and y_val> 0 and abs(y_val) - abs(x_val) <= 50 and z_val < 900:
        scroll_left()
    
    elif y_val < 0 and x_val < 0 and z_val < 900:
        scroll_right()
    
    
    