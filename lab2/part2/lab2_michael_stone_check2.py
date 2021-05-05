from machine import I2C, Pin, ADC
import ssd1306
import time

light = ADC(0)
i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

max_brightness = 255
max_light = 1024

oled.fill(0)
oled.text("Some Text",0,0)
oled.show()


while True:
    # read light, find out percent exposure, adjust brightness 
    # more exposure = more brightness
    oled.contrast(int(max_brightness * (light.read()/max_light))) 
    print("exposure: " + str(light.read()))
    print("brightness: " + str(int(max_brightness * (light.read()/max_light))))
    time.sleep_ms(1000)