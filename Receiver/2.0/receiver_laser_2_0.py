import time
import sys
import os
import serial
import pigpio
import RPi.GPIO as GPIO
import socket,json

########## TCP ##########
TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#PINS


GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings 
motI = 18
motD = 13
frequence = 50
pi = pigpio.pi() # Connect to local Pi.

#CLASSES

def initialization():
    
    pi.set_servo_pulsewidth(motI, 1500)

    pi.set_servo_pulsewidth(motD,1500)
    
def fiveg_control(s):
    try:
        conn, addr = s.accept()
        data= conn.recv(BUFFER_SIZE).decode("utf-8")
        fiveg_data= json.loads(data.decode())
        conn.close()
        fiveg_connect=True
    except:
        fiveg_data=[1500,1500]
        fiveg_connect=False
        
    return fiveg_data

#MAIN
def __init__(s):
    initialization()
    while True:
        datos=fiveg_control(s)
        time.sleep(0.05)
        pi.set_servo_pulsewidth(motI , datos[0])
        pi.set_servo_pulsewidth(motD,datos[1])
 
try:
    __init__(s)
except:
    print("No se ha podido inicializar el programa")
