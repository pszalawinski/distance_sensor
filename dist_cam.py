import RPi.GPIO as GPIO
import time
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_LED_RED = 27
GPIO_LED_GREEN = 22

chan_list = [GPIO_TRIGGER, GPIO_LED_GREEN, GPIO_LED_RED]

camera = PiCamera()

GPIO.setup(chan_list, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':

    try:
        while True:
            dist = distance()
            if distance() < 10:
                GPIO.output(GPIO_LED_RED, GPIO.HIGH)
                GPIO.output(GPIO_LED_GREEN, GPIO.LOW)
                camera.start_preview()
                time.sleep(1)
                camera.stop_preview()
                camera.capture('foo.jpg')
            else:
                GPIO.output(GPIO_LED_RED, GPIO.LOW)
                GPIO.output(GPIO_LED_GREEN, GPIO.HIGH)
            print(dist)
            time.sleep(1)


    except KeyboardInterrupt:
        print("Measurement stopped")
        GPIO.cleanup()
