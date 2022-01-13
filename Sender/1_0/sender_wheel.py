from pyPS4Controller.controller import Controller
import pygame
import pprint
import os
import socket
import json
import time
import os
from decimal import Decimal


#####################WIFICONF#######################
TCP_IP = "192.168.2.130"
TCP_PORT = 5005
BUFFER_SIZE = 1024
server_palanca = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_palanca.bind(("127.0.0.1", 8050))
server_palanca.listen(0)




#globalvars


def get_palanca ():
    
    cli, addr =server_palanca.accept()
    dato = cli.recv(1024).decode("ascii")
    cli.close()
#    cli.send(dato.encode("ascii"))
    return dato

def get_speed(input_wheel,velocidad,last_vel):
    
    peso=0.5
    
    try:
        velocidad=-float(velocidad)
    except:
        
        velocidad=-last_vel[0]

    if(velocidad>0):
            velocidad=velocidad*1000 
            vel_rigth= (velocidad)*(peso+input_wheel)
            vel_left= (velocidad)*(1-(peso+input_wheel))
            if(vel_rigth>488):
                vel_rigth=488
            if(vel_left>488):
                vel_left=488
    elif(velocidad==0):
            vel_rigth= (500+velocidad)*(peso+input_wheel/2)-250
            vel_left= (500+velocidad)*(1-(peso+input_wheel/2))-250

    else:
            velocidad=-velocidad*1000 
            vel_rigth= -(velocidad)*(peso+input_wheel)
            vel_left= -(velocidad)*(1-(peso+input_wheel))
            if(vel_rigth<-488):
                vel_rigth=-488
            if(vel_left<-488):
                vel_left=-488

    return [int(512+vel_rigth)/4,int(512+vel_left)/4]  

def send(speed): #send the information to a client

    speed_l=str(int(speed[0])).zfill(4)
    speed_r=str(int(speed[1])).zfill(4)
    MESSAGE = bytes(str(speed_l+","+speed_r), encoding = "utf-8")

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_STREAM)  # UDP
    sock.connect((TCP_IP,TCP_PORT))
    sock.send(MESSAGE)
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    pprint.pprint(data)


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: -1.0, 4: -1.0}#initilizate the axis you will use in this dictionary
    button_data = None
    hat_data = None
    deadman=False
    current_speed=[512,512]

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(1)
        self.controller.init()



    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: -1.0}#initilizate the axis you will use in this dictionary

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value, 2)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        
                        self.button_data[event.button] = not self.button_data[event.button]
                        if event.button == 3:
                            self.deadman=True

                    elif event.type == pygame.JOYBUTTONUP:
                    
                        self.button_data[event.button] = not self.button_data[event.button]
                        if event.button == 3:
                            self.deadman=False

                    # Insert your code on what you would like to happen for each event here!
                    # In the current setup, I have the state simply printing out to the screen.

                palanca =get_palanca()  
                volante =self.axis_data.get(0)
                self.current_speed = get_speed(volante,palanca,self.current_speed)               
                time.sleep(0.01)
                pprint.pprint(self.current_speed)
                #send(self.current_speed)
                


                
if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
