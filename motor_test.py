import RPi.GPIO as GPIO
import time

motor_pin = 31

def setup():
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motor_pin, GPIO.OUT)
    GPIO.output(motor_pin, GPIO.LOW)
    pwm = GPIO.PWM(motor_pin, 50)
    pwm.start(0)

def loop():
    pwm.ChangeDutyCycle(0)
    time.sleep(10)
    pwm.ChangeDutyCycle(1)
    # for duty in range(0, 50):
    #     pwm.ChangeDutyCycle(duty)
    #     time.sleep(0.25)
    while True:
        continue

def destroy():
    pwm.stop()
    GPIO.output(motor_pin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
