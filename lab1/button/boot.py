from machine import Pin, ADC, PWM
import time

pressed = False

def handle(pin):
	global pressed
	pressed = True

frequency = 10000
button = Pin(12,Pin.IN,Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler = handle)
light = ADC(0)
led = PWM(Pin(15), frequency)
buzzer = PWM(Pin(14), frequency)

while True:
	if pressed:
		first = button.value()
		time.sleep_ms(10)
		second = button.value()
		light_val = light.read()
		led.duty(light_val)
		buzzer.duty(light_val)
		if not first and second:
			pressed = False
			led.duty(0)
			buzzer.duty(0)
