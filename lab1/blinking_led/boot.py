# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
import time
led1 = machine.Pin(15, machine.Pin.OUT)
led2 = machine.Pin(14, machine.Pin.OUT)
flicks = 0
led1.off()
led2.off()
while True:
	led1.on()
	time.sleep_ms(100)
	led1.off()
	flicks += 1

	if flicks >= 5:
		if(led2.value() == 1):
			led2.off()
		else:
			led2.on()
		flicks = 0

	time.sleep_ms(100)
	flicks += 1
	if flicks >= 5:
		if(led2.value() == 1):
			led2.off()
		else:
			led2.on()
		flicks = 0
