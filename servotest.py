from gpiozero import AngularServo, LED
from time import sleep

servo = AngularServo(2, min_pulse_width=0.0006, max_pulse_width=0.0023)
green_led = LED(3, active_high=False)


while (True):
    # servo.angle = 9
    # sleep(0.2)




    servo.angle = 90
    print ("90")
    green_led.on()
    sleep(2)
    servo.angle = 0
    print ("0")
    green_led.off()
    sleep(2)

    # servo.angle = -90
    # print ("-90")
    # sleep(2)