#####################IMPORTS#######################
import socket
import time
import pygame

#####################VARIABLES#######################
host = 'localhost'
port = 8050
input_Palanca=0
usb_Port=0 #0/1
#####################METHODS#######################
def send(input_Palanca): #send the information to a client
    
    try:
        input_Palanca=(input_Palanca-1)/2

        MESSAGE = bytes(str(input_Palanca), encoding = "utf-8")


        sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_STREAM)  # TCP
        sock.connect((host,port))
        sock.send(MESSAGE)
        data = sock.recv(1024)
        sock.close()
        #print(input_Palanca)
    except:
        print("fallo de conexion de la palanca")



#####################CLASS#######################
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
        self.controller = pygame.joystick.Joystick(usb_Port)
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
                input_Palanca=self.axis_data.get(0)
                if(not self.marcha_atras):
                    send(input_Palanca)
                elif(self.marcha_atras):
                    send(3)
                
                
                
#####################MAIN#######################
if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()

