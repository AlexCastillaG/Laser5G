import time
import sys
import os
import serial
import pigpio
import RPi.GPIO as GPIO
import socket,json
from subprocess import Popen

########## TCP ##########
TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#CLASS
class rf(object):
    motI=""
    motD=""
    fiveg=False

rf.fiveg=False

#FNC
def recorreString(mystring):
    num=0
    motI=""
    motD=""
    relay=""
    for i in mystring:
        if(i=="," and num==0):
            num=1
        elif(i=="," and num==1):
            num=2
        if(i!="," and num==0):
            motI=motI+i
        if(i!="," and num==1):
            motD=motD+i
        if(i!="," and num==2):
            if(i=="1" or i=="2" or i=="0"):
                relay=relay+i
    if (relay!=""):
        if (int(relay)==2000):
            fiveg=True
        else:
            fiveg=False
    else:
        fiveg=False
    rf.motI=motI
    rf.motD=motD
    rf.fiveg=fiveg
    return rf


#MAIN
def __init__(s):
    count=0
    arduino_connect=True
    while True:
        ser = serial.Serial('/dev/ttyS0', 9600)
        try:
            arduino = serial.Serial('/dev/ttyACM0', 9600)            
            arduino_connect=True
        except:
            arduino_connect=False
            arduino=""
        try:
            x=ser.readline()
            x=x.decode("ascii")
            rf=recorreString(x)
        except:
            print("Fallo decode")
            rf.fiveg=False
            rf.motI="0512"
            rf.motD="0512"
        if(rf.fiveg):          
            datos=fiveg_control(arduino,arduino_connect,s)
            print(" \n########################################")
            if(datos[1]):
                print("# Control Mode: 5G" + " | Connected: "+str(datos[1])+"   #")
            else:
                print("# Control Mode: 5G" + " | Connected: "+str(datos[1])+"  #")
            print("# Motor Speed: "+str(datos[0])+"               #")
            if(arduino_connect):
                print("########################################")
            else:
                print("########################################  Arduino No Conectado")
        else:
            datos=rf_control(rf,arduino,arduino_connect)
            print(" \n########################################")
            print("# Control Mode: RF"+"                     #")
            print("# Motor Speed: "+datos+"               #")
            if(arduino_connect):
                print("########################################")
            else:
                print("########################################  Arduino No Conectado")      
        count+=1
        time.sleep(0.05)

def rf_control(rf,arduino,arduino_connect):
    try:
        if (int(rf.motI)>500 and int(rf.motI)<520):
            rf.motI="508"
        if (int(rf.motD)>500 and int(rf.motD)<520):
            rf.motD="508"  
        if (int(rf.motI)>880):
            rf.motI="1020"
        if (int(rf.motD)>880):
            rf.motD="1020"
        if (int(rf.motI)<110):
            rf.motI="1"
        if (int(rf.motD)<110):
            rf.motD="1"
    except:
        print("Dato no enviado")
        rf.motI="508"
        rf.motD="508"
    try:
        datos=str(int(int(rf.motI)/4)).zfill(4)+","+str(int(int(rf.motD)/4)).zfill(4)+"\n"
    except:
        print("Dato no actualizado")
    if(arduino_connect):
        try:
            arduino.write(str(datos).encode())
            datos=str(int(int(rf.motI)/4)).zfill(4)+","+str(int(int(rf.motD)/4)).zfill(4)
        except:
            print("Dato no enviado")
    return datos
    
def fiveg_control(arduino,arduino_connect,s):
    try:
        conn, addr = s.accept()
        fiveg_data= conn.recv(BUFFER_SIZE).decode("utf-8")
        conn.close()
        '''data, addr= sock.recvfrom(64)
        message= json.loads(data.decode())
        vel_left=message.get("vel_left")
        vel_rigth=message.get("vel_rigth")
        fiveg_data=str(vel_left).zfill(4)+","+str(vel_rigth).zfill(4)'''
        fiveg_connect=True
    except:
        fiveg_data="0127,0127"
        fiveg_connect=False
        
    datos=str(fiveg_data)+"\n"
    if(arduino_connect):
        try:
            arduino.write(datos.encode())
        except:
            print("Dato no enviado")
    datos=str(fiveg_data)
    return datos,fiveg_connect
    
try:
    __init__(s)
except:
    print("No se ha podido inicializar el programa")
