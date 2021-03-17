import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


def led_control(msg):
    try:
        green_status = msg.split("-")[0]
        red_status = msg.split("-")[1]
        print("greenled:", green_status, "  -   ", "redled : ", red_status)
    except:
        green_status = "off"
        red_status = "off"
    if green_status == "on":
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)

    elif green_status == "off" and red_status == "on":
        GPIO.output(24, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
# GPIO.cleanup()
