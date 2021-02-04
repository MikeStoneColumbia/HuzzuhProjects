from machine import I2C, Pin
import ssd1306

i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.text("something",0,0)
oled.show()
