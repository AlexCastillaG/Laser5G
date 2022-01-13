#!/usr/bin/env python

#Variables
#Se importa el módulo
import socket
import time
import pygame
#Creación de un objeto socket (lado cliente)
#Variables
host = 'localhost'
port = 8050
 
input_palanca=0


def send(input_palanca): #send the information to a client
    
    try:
        input_palanca=(input_palanca-1)/2

        MESSAGE = bytes(str(input_palanca), encoding = "utf-8")


        sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_STREAM)  # TCP
        sock.connect((host,port))
        sock.send(MESSAGE)
        data = sock.recv(1024)
        sock.close()
        print(input_palanca)
    except:
        print("fallo de conexion")




class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = {0: 1.0}#initilizate the axis you will use in this dictionary
    button_data = None
    marcha_atras=False

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()




    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0: 0}#initilizate the axis you will use in this dictionary

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False



        while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value, 2)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        
                        self.button_data[event.button] = not self.button_data[event.button]
                        if event.button == 7:
                            self.marcha_atras=True

                    elif event.type == pygame.JOYBUTTONUP:
                    
                        self.button_data[event.button] = not self.button_data[event.button]
                        if event.button == 7:
                            self.marcha_atras=False
        
                time.sleep(0.01)
                input_palanca=self.axis_data.get(0)
                if(not self.marcha_atras):
                    send(input_palanca)
                elif(self.marcha_atras):
                    send(3)
                #
if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
    #Cerramos la instancia del objeto servidor
