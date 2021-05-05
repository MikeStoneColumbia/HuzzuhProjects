from machine import I2C, Pin, RTC
import ssd1306
import time


'''
    Button B: Will toggle between time and setting time
    Button A: Will move the pointer
    Button C: Will increment the time @ pointer

    Initial conditions:
    Screen is filled with 0's
    Time will be set by machine
    
    Vars:
    oled     : screen
    rtc      : clock
    timeMode : determines if clock runs or settings
    button_b : toggle button
    button_a : pointer button
    button_c : increment button
    date     : current return value from rtc.datetime()
'''

timeMode = True
date_pointer = -1
i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
rtc = RTC()
rtc.datetime((2000, 1, 1, 1,0,0,0,10))
date = []
set_alarm = []


def change_date(pin):
    global timeMode
    global date_pointer
    global col
    global date
    global set_alarm
    if timeMode:
        set_alarm = date[:] #making a new alarm
    else:
         if set_alarm[0:3] <= date[0:3] and set_alarm[4:] <= date[4:]: # invalid alarm
             set_alarm = []
             print("can't set an alarm in the past")
         else:
            print("alarm set for :")
            print(set_alarm)
    date_pointer = -1
    col = 0
    timeMode = not timeMode # switching modes

button_a = Pin(13, Pin.IN, Pin.PULL_UP)
button_b = Pin(12, Pin.IN, Pin.PULL_UP)
button_c = Pin(2, Pin.IN, Pin.PULL_UP)
button_b.irq(trigger=Pin.IRQ_FALLING, handler = change_date) 
buzzer = Pin(15,Pin.OUT)
buzzer.off()

year_month_date = ''
hour_min_seconds = ''
col = 0

while True:

    if timeMode:

        if len(set_alarm) != 0:
            if set_alarm[0:3] <= date[0:3] and set_alarm[4:] <= date[4:]: #if current date surpasses set alarm
                print("alarm goes off")
                set_alarm = []
                oled.fill(0)
                oled.text("ALARM",44,12)
                oled.show()
                buzzer.on()
                time.sleep_ms(3000)
                buzzer.off()


        date = list(str(x) for x in rtc.datetime()[0:7])
        year_month_date = date[0] + '/' + date[1] + '/' + date[2]
        hour_min_seconds = date[4] + ':' + date[5] + ':' + date[6]
        oled.fill(0)
        oled.text(year_month_date,0,0)
        oled.text(hour_min_seconds, 0, 10)
        oled.show()
    else:
        first_a = button_a.value()
        first_c = button_c.value()
        time.sleep_ms(11)
        second_a = button_a.value()
        second_c = button_c.value()

        if first_a and not second_a: # controls the pointer
            date_pointer += 1
            print(date_pointer)

            if (date_pointer > 6 and col == 10): # loop back
                col = 0
                date_pointer = -1
            
            if (int(set_alarm[2]) >= 10 and int(set_alarm[1]) >= 10) and col == 0:
                if date_pointer > 8 and col == 0: # end of first line
                    col = 10
                    date_pointer = -1

            elif ((int(set_alarm[2]) >= 10 and int(set_alarm[1]) < 10) or (int(set_alarm[2]) < 10 and int(set_alarm[1]) >= 10)) and col == 0:
                if date_pointer > 7 and col == 0: # end of first line
                    col = 10
                    date_pointer = -1
            
            elif date_pointer > 4 and (int(set_alarm[4]) < 10 and int(set_alarm[5]) < 10 and int(set_alarm[6]) < 10) and col == 10:
                col = 0
                date_pointer = -1
            
            elif date_pointer > 5 and col == 10 and ((int(set_alarm[4]) >= 10 and int(set_alarm[5]) < 10 and int(set_alarm[6]) < 10) 
            or (int(set_alarm[4]) < 10 and int(set_alarm[5]) >= 10 and int(set_alarm[6]) < 10) 
            or (int(set_alarm[4]) < 10 and int(set_alarm[5]) < 10 and int(set_alarm[6]) >= 10)):
                col = 0
                date_pointer = -1
            
            elif date_pointer > 7 and col == 10 and ((int(set_alarm[4]) >= 10 and int(set_alarm[5]) >= 10 and int(set_alarm[6]) < 10) 
            or (int(set_alarm[4]) < 10 and int(set_alarm[5]) >= 10 and int(set_alarm[6]) >= 10) 
            or (int(set_alarm[4]) >= 10 and int(set_alarm[5]) < 10 and int(set_alarm[6]) >= 10)):
                 col = 0
                 date_pointer = -1

            if (date_pointer == 4 or date_pointer == 6) and col == 0: # skip special lines
                date_pointer += 1
                if int(set_alarm[1]) >= 10:
                    date_pointer += 1
            
            if date_pointer == 1 and col == 10:
                date_pointer += 1
            
            if col == 10 and date_pointer == 0:
                if int(set_alarm[4]) >= 10:
                    date_pointer += 1
            
            elif (col == 10 and date_pointer == 2):
                if int(set_alarm[4]) >= 10:
                    date_pointer += 1

                if int(set_alarm[5]) >= 10:
                    date_pointer += 1
            
            elif col == 10 and date_pointer >= 3:
                if int(set_alarm[4]) >= 10 and int(set_alarm[5]) >= 10:
                    date_pointer = 6

                elif date_pointer == 4:
                    date_pointer += 1

                if int(set_alarm[6]) >= 10:
                    date_pointer += 1
                
                if int(set_alarm[4]) < 10 and int(set_alarm[5]) < 10:
                    date_pointer += 1

            if date_pointer > 7 and col == 0:
                print("here")
                if (int(set_alarm[2]) < 10):
                    print("newline")
                    date_pointer = -1
                    col = 10
                else:
                    if int(set_alarm[1]) >= 10:
                        date_pointer += 1

                    if int(set_alarm[2]) >= 10:
                        date_pointer += 1

            

            oled.fill(0)
            oled.text('_',date_pointer * 8, col)
            oled.text(year_month_date,0,0)
            oled.text(hour_min_seconds,0,10)
            oled.show()
        if first_c and not second_c:
            if col == 0:
                if date_pointer <= 3:
                    year = [str(char) for char in set_alarm[0]]
                    digit = int(year[date_pointer]) + 1
                    if digit >= 10:
                        digit = 0
                    year[date_pointer] = str(digit)
                    set_alarm[0] = ''.join(year)

                elif date_pointer == 5 and int(set_alarm[1]) < 10:
                    month = int(set_alarm[1]) + 1
                    set_alarm[1] = str(month)
                    if month >= 10:
                        date_pointer += 1
                
                elif date_pointer == 6 and int(set_alarm[1]) >= 10:
                    month = int(set_alarm[1]) + 1
                    if month >= 13:
                        month = 1
                        date_pointer = 5
                    set_alarm[1] = str(month)
                
                elif (date_pointer == 7 and int(set_alarm[2]) < 10) or (date_pointer == 8 and int(set_alarm[2]) < 10 and int(set_alarm[1]) >= 10):
                    day = int(set_alarm[2]) + 1
                    if day >= 10:
                        date_pointer += 1
                    set_alarm[2] = str(day)
                
                elif (date_pointer >= 8) or (date_pointer == 7 and int(set_alarm[2]) >= 10):
                    day = int(set_alarm[2]) + 1
                    month = int(set_alarm[1])
                    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12) and day > 31:
                        day = 1
                        date_pointer -= 1
                    elif (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
                        day = 1
                        date_pointer -= 1
                    elif day > 29 and month == 2:
                        day = 1
                        date_pointer -= 1
                    set_alarm[2] = str(day)
                    
                

            elif col == 10 :
                if date_pointer <= 1:
                    hour = int(set_alarm[4]) + 1
                    if hour > 9 and date_pointer == 0:
                        date_pointer += 1
                    elif hour > 23 and date_pointer == 1:
                        date_pointer = 0
                        hour = 0
                    set_alarm[4] = str(hour)
                
                if (date_pointer == 2 and int(set_alarm[4]) < 10) or (date_pointer == 3) or (date_pointer == 4 and int(set_alarm[5]) > 9 and int(set_alarm[4]) > 9):
                    min = int(set_alarm[5]) + 1
                    if min > 9 and ((date_pointer == 2 and int(set_alarm[4]) < 10) or (date_pointer == 3 and int(set_alarm[4]) > 9)):
                        date_pointer += 1
                    if min > 59:
                        date_pointer -= 1
                        min = 0
                    set_alarm[5] = str(min)
                
                # elif (date_pointer == 4 and int(date[4]) < 10 and int(date[5]) < 10) or (date_pointer == 5 and ((int(date[4] > 9 and int(date[5]) < 10)) or (int(date[4] < 10 and int(date[5]) > 10)))) or (date_pointer >= 6) or (date_pointer == 5 and int(date[4]) > 9 and int(date[5]) > 9):
                #     pass

                elif date_pointer >= 4:
                    second = int(set_alarm[6]) + 1
                    if second > 9 and ((date_pointer == 4 and int(set_alarm[4]) < 10 and int(set_alarm[5]) < 10) or (date_pointer == 5 and ((int(set_alarm[4]) > 9 and int(set_alarm[5]) < 10) )) or (date_pointer == 6 and int(set_alarm[4]) > 9 and int(set_alarm[5]) > 9)):
                        date_pointer += 1
                    if second > 59:
                        date_pointer -= 1
                        second = 0
                    set_alarm[6] = str(second)
                

        if not first_c and second_c:
            print("released")
            #rtc.datetime((int(set[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]), int(date[6]),0))
            year_month_date = set_alarm[0] + '/' + set_alarm[1] + '/' + set_alarm[2]
            hour_min_seconds = set_alarm[4] + ':' + set_alarm[5] + ':' + set_alarm[6]
            oled.fill(0)
            oled.text('_',date_pointer * 8, col)
            oled.text(year_month_date,0,0)
            oled.text(hour_min_seconds,0,10)
            oled.show()



