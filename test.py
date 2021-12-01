import serial
import time

a = 1001
b = 1002
c = 1003


ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.1)
ser.flush()

while True:
    #motor_pwms = find_pwm(input_angle_rads, input_mag)
    
    #pwm_1 = motor_pwms[0].to_bytes(2, 'big')
    #pwm_2 = motor_pwms[1].to_bytes(2, 'big')
    #pwm_3 = motor_pwms[2].to_bytes(2, 'big')
    pwm_1 = a.to_bytes(2, 'big')
    pwm_2 = b.to_bytes(2, 'big')
    pwm_3 = c.to_bytes(2, 'big')
    ser.write(pwm_1)
    #print("Hello1")
    ser.write(pwm_2)
    #print("Hello2")
    ser.write(pwm_3)
    #print("Hello3")
    ser.write(bytes('p', 'ascii'))
    
    #print("Hello4")
    line = ser.readline().decode('utf-8').rstrip()

    if line != "":
        print(line)
        
    time.sleep(0.1)
