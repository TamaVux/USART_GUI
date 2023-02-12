from tkinter import *
import serial
import time
import sys
import glob


#### ================ #### SEND TEXT TO SCREEN #### ================ ####
def send_text(screen,string):
    screen.config(state=NORMAL)
    screen.insert(END,string)
    screen.config(state=DISABLED)

#### ================ #### GET PORTS #### ================ ####
def get_port():        
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port, desc, hwid in sorted(ports):
            port_name = "{}: {} [{}]".format(port, desc, hwid)
            print(port_name)
            port_list.append(port_name)
    return port_list
#### ================ #### CONNECTION BUTTON #### ================ ####
def connectBtn(screen,data_usart):
    port = data_usart[1]
    baud = data_usart[0]
    if port != '-':
        send_text(screen,'\nTry Connecting to: {} at {}.........'.format(port,baud))
        try: 
            serialConnection = serial.Serial(port,baud,timeout=4)
            send_text(screen,'\nConnected to: {} at {} !!!'.format(port,baud))
        except:
            send_text(screen,'\nFailed to connecting to: {} at {}'.format(port,baud))
    else: send_text(screen,'Please select port !!!')
#### ================ #### DISCONNECT BUTTON #### ================ ####
def disconnectBtn(screen,data_usart):
    port = data_usart[1]
    baud = data_usart[0]
    send_text(screen,'\nDisconnecting to: {}'.format(port))

    return

#### ================ #### REFRESH BUTTON #### ================ ####
def refreshBtn():
    get_port()

    return

#### ================ #### SEND(1,2) BUTTON  #### ================ ####
def sendButtons(screen,value):
    send_text(screen,'\nSend: {}'.format(value))
    return
#### ================ #### GET USART DATA TO SCREEN #### ================ ####
def dataToScreen():

    return

#### ================ #### SETUP PLOT #### ================ ####
def setup_plot(plot,xlabel,ylabel,title):
    
    return 
