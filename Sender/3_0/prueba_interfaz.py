#####################IMPORTS#######################
from pyPS4Controller.controller import Controller
import pygame
import pprint
import os
import socket
import json
import time
import os
from decimal import Decimal
import PySimpleGUI as sg
import pickle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

BUFFER_SIZE = 1024
server_palanca = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_palanca.bind(("127.0.0.1", 8051))
server_palanca.listen(0)

def get_mot ():
    
    cli, addr =server_palanca.accept()
    dato = pickle.loads(cli.recv(1024))
    cli.close()
    return dato




mot=[0,0]
layout = [[sg.Text(mot,key='mot')]]
# Create the window
window = sg.Window("5G LASER", layout)

# Create an event loop
while True:
    event, values = window.read(timeout=10)
    window.Refresh()
    # End program if user closes window or
    # presses the OK button
    mot=get_mot()

    window['mot'].Update(mot)


    if event == sg.WIN_CLOSED:
        break

window.close()