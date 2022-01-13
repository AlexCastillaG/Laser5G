#####################IMPORTS#######################
import socket
import os
import time
import threading
import time
import PySimpleGUI as sg
import pickle
import traceback
from PySimpleGUI.PySimpleGUI import Titlebar
#####################VARIABLES#######################
BUFFER_SIZE = 1024
server_palanca = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_palanca.bind(("127.0.0.1", 8051))
server_palanca.listen(0)
mot=[0,0]

#####################GUI#######################
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

layout = [[sg.Image("logoiteam.png",size=(250,125),background_color="white")],
[sg.Image("barco.png",size=(250,200),background_color="white")],
[sg.Text("Motor Derecho: "+str(mot[0])+"%"+"                                               "+"Motor Izquierdo: "+str(mot[1])+"%",key='mot',background_color="white",text_color="black")]
]

# Create the window
window = sg.Window("5G LASER", layout,size=(600,400),element_justification='c',background_color="white")

#####################METHODS#######################

def to_percentage(input):

    motI=input[0]
    motD=input[1]

    if motI>=1500:
        motI=(motI-1500)/5
    elif motI<1500:
        motI=(motI-1500)/5

    if motD>=1500:
        motD=(motD-1500)/5
    elif motD<1500:
        motD=(motD-1500)/5

    output= [motI,motD]
    return output

def start_GUI():

    while True:
        event, values = window.read(timeout=10)
        window.Refresh()
        # End program if user closes window or
        # presses the OK button
        mot=get_mot()
        #print(mot)
        mot=to_percentage(mot)
        window['mot'].Update("Motor Derecho: "+str(mot[0])+"%"+"                                               "+"Motor Izquierdo: "+str(mot[1])+"%")



        if event == sg.WIN_CLOSED:
            break

    window.close()

def get_mot ():
    
    cli, addr =server_palanca.accept()
    dato = pickle.loads(cli.recv(1024))
    cli.close()
    return dato

def run_wheel():
    os.system("python sender_wheel2_0.py")
    
def run_level():
    os.system("python palanca2_0.py")

def start_program():
    wheel=threading.Thread(target=run_wheel)
    wheel.start()

    level=threading.Thread(target=run_level)
    level.start()

    GUI=threading.Thread(target=start_GUI)
    GUI.start()

    wheel.join()
    level.join()
    GUI.join()



#####################MAIN#######################

if __name__ == "__main__":
    start_program()
