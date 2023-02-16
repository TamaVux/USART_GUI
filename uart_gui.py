from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from usart_com import SerialCom

import threading
import serial
import serial.tools.list_ports
import time
import sys
import glob
import pandas as pd

#global varible
USART_VARIBLE = {
    'BAUDRATE': [4800,8800,9600,19200,115200],
    'PORT': ['-'],
    'PARITY':['NONE','ODD','EVEN','MARK','SPACE'],
    'DATABITS':[8,7,6,5],
    'STOPBIT':[1,2],
    'DATAS': [],
    'STATUS': False,
}

PLOT_VARIBLE = {
    'TITLE': '',
    'XLABEL': '',
    'YLABEL':'',
    'FIG_SIZE':(7,5),
}

SIZE = {
    'S10': 10,
    'S20': 20,
    'S30': 30,  # FOR ENTRY 
    'S50': 50
}
class Usart:
    def __init__(self,window):
        # ########## ================ #### INITIALIZE MAIN LAYOUT #### ================ ######### #            
        # ================  Main window ================ #
        self.window = window
        self.window.title('USART')
        #self.window.geometry('900x900')
        # ================  Data frame ================ #
        self.data_screen = LabelFrame(self.window,text='Datas',padx=5,pady=5)
        self.data_screen.grid(row=0,column=0,rowspan=2,sticky="W",padx=5,pady=5)
        # ================  Setting frame ================ #
        self.settingframe = LabelFrame(self.window,text='Settings',padx=5,pady=5)
        self.settingframe.grid(row=0,column=1,sticky="W",padx=5,pady=5)
        # ================  Status frame ================ #
        self.status_frame = LabelFrame(self.window,text='Status',padx=5,pady=5)
        self.status_frame.grid(row=1,column=1,sticky="W",padx=5,pady=5)
        # ================  Plot frame ================ #
        self.plot_frame = LabelFrame(self.window,text='Plot',padx=5,pady=5)
        self.plot_frame.grid(row=2,column=0,columnspan=3,sticky="W",padx=5,pady=5)
        # ########## ================ #### DATA FRAME #### ================ ########## # 
        # ================  Screen frame ================ #
        self.screen_frame = Frame(self.data_screen)
        self.screen_frame.grid(row=0,column=0,columnspan=3)
        # ================  Screen scrollbar ================ #
        self.text_scroll = Scrollbar(self.screen_frame)
        self.text_scroll.pack(side=RIGHT,fill=Y)
        # ================  Screen ================ #
        self.screen = Text(self.screen_frame,
            height=10,
            width=50,
            bg='black',
            fg='white',
            insertbackground='yellow',
            yscrollcommand=self.text_scroll.set)
        self.screen.pack(side=LEFT)
        self.screen.config(state=DISABLED)
        # ================  Configure Scrollbar on screen ================ #
        self.text_scroll.config(command=self.screen.yview)
        # ================  Data send buttons ================ #
        # ==== Send data 1 ==== #
        Label(self.data_screen,text='Data1').grid(row=1,column=0)
        data_e1 = Entry(self.data_screen,width=SIZE['S30'],bg='grey',fg='white')
        data_e1.grid(row=1,column=1)
        send_btn1 = Button(self.data_screen,text='Send',
            command=lambda: self.sendButtons(data_e1.get()))
        send_btn1.grid(row=1,column=2)
        # ==== Send data 2 ==== #
        Label(self.data_screen,text='Data2').grid(row=2,column=0)
        data_e2 = Entry(self.data_screen,width=SIZE['S30'],bg='grey',fg='white')
        data_e2.grid(row=2,column=1)
        send_btn2 = Button(self.data_screen,text='Send',
            command=lambda: self.sendButtons(data_e2.get()))
        send_btn2.grid(row=2,column=2)

        # ########## ================ #### SETTING FRAME #### ================ ########### # 
        self.baudVar = IntVar()
        self.portVar = StringVar()
        self.parityVar = StringVar()
        self.databitsVar = IntVar()
        self.stopbitVar = IntVar()
        # ================  Baudrate ================ #
        self.baudVar.set(USART_VARIBLE['BAUDRATE'][1])
        Label(self.settingframe,text='Baudrate:').grid(row=0,column=0,sticky="W")
        self.baudDrop = OptionMenu(self.settingframe,self.baudVar,*USART_VARIBLE['BAUDRATE'])
        self.baudDrop.config(width=SIZE['S20'])
        self.baudDrop.grid(row=0,column=1)
        # ================  Port ================ #
        self.portVar.set(USART_VARIBLE['PORT'][0])
        Label(self.settingframe,text='Port:').grid(row=1,column=0,sticky="W")
        self.portDrop = OptionMenu(self.settingframe,self.portVar,*USART_VARIBLE['PORT'])
        self.portDrop.config(width=SIZE['S20'])
        self.portDrop.grid(row=1,column=1)
        # ================  Parity ================ #
        self.parityVar.set(USART_VARIBLE['PARITY'][0])
        Label(self.settingframe,text='Parity:').grid(row=2,column=0,sticky="W")
        self.parityDrop = OptionMenu(self.settingframe,self.parityVar,*USART_VARIBLE['PARITY'])
        self.parityDrop.config(width=SIZE['S20'])
        self.parityDrop.grid(row=2,column=1)
        # ================  Databits ================ #
        self.databitsVar.set(USART_VARIBLE['DATABITS'][0])
        Label(self.settingframe,text='Data bits:').grid(row=3,column=0,sticky="W")
        self.databitsDrop = OptionMenu(self.settingframe,self.databitsVar,*USART_VARIBLE['DATABITS'])
        self.databitsDrop.config(width=SIZE['S20'])
        self.databitsDrop.grid(row=3,column=1)
        # ================  Stopbit ================ #
        self.stopbitVar.set(USART_VARIBLE['STOPBIT'][0])
        Label(self.settingframe,text='Stop bits:').grid(row=4,column=0,sticky="W")
        self.stopbitDrop = OptionMenu(self.settingframe,self.stopbitVar,*USART_VARIBLE['STOPBIT'])
        self.stopbitDrop.config(width=SIZE['S20'])
        self.stopbitDrop.grid(row=4,column=1)

        # ================  Refresh ================ #      
        self.refresh_btn = Button(self.settingframe,text='Refresh',width=SIZE['S10'],
            bg='blue',
            fg='yellow',
            command=self.refreshBtn)
        self.refresh_btn.grid(row=0,column=2)
        # ================  Connect ================ #
        self.connect_btn = Button(self.settingframe,text='Connect',width=SIZE['S10'],
            bg='green',
            fg='yellow',
            command=lambda: self.connectBtn())
        self.connect_btn.grid(row=1,column=2)
        # ================  Disconnect ================ #
        self.disconnect_btn = Button(self.settingframe,text='Disconnect',width=SIZE['S10'],
            bg='red',
            fg='yellow',
            command=lambda: self.disconnectBtn())
        self.disconnect_btn.grid(row=2,column=2)


        # ########## ================ #### STATUS FRAME #### ================ ########## # 
        sta_C = Canvas(self.status_frame,width=20,height=20)
        sta_C.grid(row=0,column=0)
        sta_C.create_rectangle(0, 0, 20, 20, fill='blue')
        sta_C_label = Label(self.status_frame,text='Connected').grid(row=0,column=1)

        sta_TX = Canvas(self.status_frame,width=20,height=20)
        sta_TX.grid(row=0,column=2)
        sta_TX.create_rectangle(0, 0, 20, 20, fill='blue')
        sta_TX_label = Label(self.status_frame,text='TX').grid(row=0,column=3)

        sta_RX = Canvas(self.status_frame,width=20,height=20)
        sta_RX.grid(row=0,column=4)
        sta_RX.create_rectangle(0, 0, 20, 20, fill='blue')
        sta_RX_label = Label(self.status_frame,text='RX').grid(row=0,column=5)       


        # ########## ================ #### PLOT FRAME #### ================ ########## # 
        # ================ plot screen ================ #
        self.plot_screen_frame = Frame(self.plot_frame)
        self.plot_screen_frame.grid(row=0,column=1,rowspan=3,padx=5,pady=5)

        self.setup_plot(PLOT_VARIBLE['TITLE'],PLOT_VARIBLE['XLABEL'],PLOT_VARIBLE['YLABEL'])
        # ================  Setup plot frame ================ #
        self.set_plot_frame = Frame(self.plot_frame)
        self.set_plot_frame.grid(row=0,column=0,padx=5,pady=5)

        Label(self.set_plot_frame,text='X Label').grid(row=0,column=0,padx=5,pady=5)
        x_label = Entry(self.set_plot_frame,width=SIZE['S30'],bg='grey',fg='white')
        x_label.grid(row=0,column=1,padx=5,pady=5)

        Label(self.set_plot_frame,text='Y Label').grid(row=1,column=0,padx=5,pady=5)
        y_label = Entry(self.set_plot_frame,width=SIZE['S30'],bg='grey',fg='white')
        y_label.grid(row=1,column=1,padx=5,pady=5)

        Label(self.set_plot_frame,text='Plot title').grid(row=2,column=0,padx=5,pady=5)
        title_label = Entry(self.set_plot_frame,width=SIZE['S30'],bg='grey',fg='white')
        title_label.grid(row=2,column=1,padx=5,pady=5)

        set_plot = Button(self.set_plot_frame,text='Set',
            width=SIZE['S10'],
            command=lambda: self.setup_plot(title_label.get(),x_label.get(),y_label.get()))
        set_plot.grid(row=3,column=0,columnspan=2,padx=5,pady=5)    

        # ########## ================ #### INIT FUNCTIONS #### ================ ########## #
        self.get_port()
        self.ser = serial.Serial()   
        uart_reader = threading.Thread(target = self.start_receive_data)
        uart_reader.start()      

    # ########## ================ #### GUI FUNCTIONS #### ================ ########## #   
    # ================  Send text to screen ================ #
    def send_text(self,string):
        self.screen.config(state=NORMAL)
        self.screen.insert(END,string)
        self.screen.see('end')
        self.screen.config(state=DISABLED)

    # ================  Update option menu ================ #
    def update_OptionMenu(self,menu,var):
        #pass (self.option,self.optionVar)
        menu = menu['menu']
        menu.delete(0, "end")
        for string in USART_VARIBLE['PORT']:
            menu.add_command(label=string, 
                            command=lambda value=string: var.set(value))
                
    # ================  Get ports ================ #
    def get_port(self):   
        USART_VARIBLE['PORT'] = ['-']     
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            port_name = "{}: {}".format(port, desc)
            #print(port_name)
            USART_VARIBLE['PORT'].append(port)
        self.update_OptionMenu(self.portDrop,self.portVar)
        return USART_VARIBLE['PORT']
    # ================  Updata Gui ================ #
    def updata_gui(self):
        while True:
            self.send_text(USART_VARIBLE['DATAS'])
            time.sleep(0.2)
    # ================  Setup serial port ================ #
    def setup_serial(self):
        portStr = self.portVar.get()
        baudStr = self.baudVar.get()
        parityStr = self.parityVar.get()
        databitsStr = self.databitsVar.get()
        stopbitStr = self.stopbitVar.get()
        # Port
        self.ser.port = portStr
        # Baudrate
        self.ser.baudrate = baudStr
        # Parity
        if (parityStr=="NONE"):
            self.ser.parity = serial.PARITY_NONE
        elif(parityStr=="ODD"):
            self.ser.parity = serial.PARITY_ODD
        elif(parityStr=="EVEN"):
            self.ser.parity = serial.PARITY_EVEN
        elif(parityStr=="MARK"):
            self.ser.parity = serial.PARITY_MARK
        elif(parityStr=="SPACE"):
            self.ser.parity = serial.PARITY_SPACE
        # Stopbit
        if (stopbitStr == 1):
            self.ser.stopbits = serial.STOPBITS_ONE
        elif (stopbitStr == 2):
            self.ser.stopbits = serial.STOPBITS_TWO
        # Databits
        if (databitsStr == 8):
            self.ser.bytesize = serial.EIGHTBITS
        elif (databitsStr == 7):
            self.ser.bytesize = serial.SEVENBITS
        elif (databitsStr == 6):
            self.ser.bytesize = serial.SIXBITS
        elif (databitsStr == 5):
            self.ser.bytesize = serial.FIVEBITS

        self.ser.timeout = 1
    # ================  Start serial communication ================ #       
    def start_receive_data(self):
        while USART_VARIBLE['STATUS'] == True:
            if (self.ser.in_waiting > 0):
                rawdata = self.ser.read(self.ser.in_waiting).decode('ascii')
                USART_VARIBLE['DATAS'].append(rawdata)
                self.window.after(0,self.send_text(rawdata))

            
            self.window.update_idletasks()
            self.window.update()                
        print('Disconnected !')
    # ================  Connection button ================ #
    def connectBtn(self):
        port = self.portVar.get()
        baud = self.baudVar.get()
        self.setup_serial()

        if port != '-':
            self.send_text('\nTry Connecting to: {} at {}.........'.format(port,baud))
            try: 
                self.ser.open()
                self.send_text('\nConnected to: {} at {} !!!'.format(port,baud))
                #if (self.ser.isOpen()):
                USART_VARIBLE['STATUS'] = True
            except:
                self.send_text('\nFailed to connecting to: {} at {}'.format(port,baud))
        else: 
            self.send_text('\nPlease select port !!!')

        self.start_receive_data()

    # ================  Disconnect button ================ #
    def disconnectBtn(self):
        if (self.portVar.get() != '-'):
            self.ser.close()
            self.send_text('\nDisconnecting to: {}'.format(self.portVar.get()))
            USART_VARIBLE['STATUS'] = False
        else: self.send_text('\nNo connection to Disconnect')
    # ================  Refresh button ================ #
    def refreshBtn(self):
        self.get_port()
    # ================  Send(1,2) buttons ================ #
    def sendButtons(self,value):
        self.send_text('\nSend: {}'.format(value))
        self.ser.write(value.encode())
    # ================  Setup plot ================ #
    def setup_plot(self,title,xlabel,ylabel):
        PLOT_VARIBLE['TITLE'] = title
        PLOT_VARIBLE['XLABEL'] = xlabel
        PLOT_VARIBLE['YLABEL'] = ylabel

        figure = plt.Figure(figsize=PLOT_VARIBLE['FIG_SIZE'], dpi=100)
        ax = figure.add_subplot(111)

        ax.set_title(PLOT_VARIBLE['TITLE'],color='blue')
        ax.set_xlabel(PLOT_VARIBLE['XLABEL'],color='blue')
        ax.set_ylabel(PLOT_VARIBLE['YLABEL'],color='blue')

        plot_screen = FigureCanvasTkAgg(figure, self.plot_screen_frame)
        plot_screen.get_tk_widget().grid(row=0,column=0)
        return 

app = Tk()
Usart(app)

app.mainloop()