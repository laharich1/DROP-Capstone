from math import *
from numpy import interp
from numpy import degrees
import serial
import time

a = 1001
b = 1002
c = 1003

def send_angle_r(input_angle_rads, input_mag):
    
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.1)
    ser.flush()
    
    
    #while True:
    motor_pwms = find_pwm(input_angle_rads, input_mag)
    
    pwm_1 = motor_pwms[0].to_bytes(2, 'big')
    pwm_2 = motor_pwms[1].to_bytes(2, 'big')
    pwm_3 = motor_pwms[2].to_bytes(2, 'big')
    ser.write(pwm_1)
    ser.write(pwm_2)
    ser.write(pwm_3)
    ser.write(bytes('p', 'ascii'))
    
    line = ser.readline().decode('utf-8').rstrip()
    if line != "":
        print(line)
        
    time.sleep(0.5)
    #input_angle_rads += 0.1
    #input_angle_rads %= 2*pi

def find_pwm(theta, r):
    motor_1_pwm = 0
    motor_2_pwm = 0
    motor_3_pwm = 0
    phi_1 = 0
    phi_2 = 0
    c1 = 0
    c2 = 0
    
    if(r <= 1):
        theta += 0.41965
        theta %= 2*pi
        
        #print("Angle", degrees(theta),"Mag:", r)

        #Find unit vectors according to angle
        
        #0 to 120
        if(0 <= theta and theta < (2*pi)/3):
            phi_1 = 0
            phi_2 = (2*pi)/3
        #120 to 240
        elif((2*pi)/3 <= theta and theta <= (4*pi)/3):
            phi_1 = (2*pi)/3
            phi_2 = (4*pi)/3
        #240 to 360
        else:
            phi_1 = (4*pi)/3
            phi_2 = 0
            
        #print("Phi_1 = ", phi_1)
        #print("Phi_2 = ", phi_2)
        
        
        #v1 = c1*cos(radians(phi_1)), c1*sin(radians(phi_1))
        #v2 = c2*cos(radians(phi_2)), c2*sin(radians(phi_2))
        
        #v1 + v2 = r*cos(theta) + r*sin(theta)
        
        #c1*cos(phi_1) + c2*cos(phi_2) = r*cos(theta)
        #c1*sin(phi_1) + c2*sin(phi_2) = r*sin(theta)
        
        #Values for C1 and C2 based on above definitions
        c2 = (r*sin(theta)*cos(phi_1) - r*cos(theta)*sin(phi_1))/(sin(phi_2)*cos(phi_1) - cos(phi_2)*sin(phi_1))
        c1 = (r*cos(theta) - c2*cos(phi_2))/cos(phi_1)
        

        
        c1 = int(interp(c1, [0, 1], [1000,1600]))
        c2 = int(interp(c2, [0, 1], [1000,1600]))
        
        #Min value that motor spins at, makes sure that not only one motor spins
        
        #print("PWM 1:", c1, "PWM 2", c2)
        
        if(phi_1 == 0 and phi_2 == (2*pi)/3):
            return (c1, c2, 1000)
        elif(phi_1 == (2*pi)/3 and phi_2 == (4*pi)/3):
            return (1000, c1, c2)
        elif(phi_1 == (4*pi)/3 and phi_2 == 0):
            return (c2, 1000, c1)
    else:
        return (1000, 1000, 1000)

#send_angle_r(3.76991, 1)