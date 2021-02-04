# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import machine
import time

frequency = 5000

led = machine.PWM(machine.Pin(15), frequency)
buzzer = machine.PWM(machine.Pin(14), frequency)

while True:
	for duty_cycle in range(0,500):
		led.duty(duty_cycle)
		buzzer.duty(duty_cycle)
		time.sleep_ms(10)
	
	led.duty(0)
	buzzer.duty(0)
	time.sleep_ms(1000)


