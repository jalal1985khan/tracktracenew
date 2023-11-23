from tkinter import *
import tkinter as tk
import socket
import sys
import datetime
import time
import threading
import pymongo
import tkinter.messagebox
from pymongo import MongoClient
import certifi
from fpdf import FPDF

TITLE_FONT = ("Arial", "25",'bold')
BUTTON_FONT = ("Arial", "15",'bold')

# Create Board Class
class Board(Frame):
    ''' Server '''
    ip_address="0.0.0.0"
    port=2001

    # Constructor
    def __init__(self, master):
        super().__init__(master)
        tk.geometry("450x550")
        tk.resizable(True, True)
        self.master=master #root of application
        #server setting for already logined user
        self.stored_info=[None]*5 #to store info like username, password, ip, port, master key
        #making field content in center
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #aking center content end
        self.buttons = [None] * 3 #for config, status, log
        self.labels = [None] * 2 # userid, password
        self.inputs = [None] *2  #userid, password
        self.opt_buttons=[None] *3 #start, stop server
        self.server_start=None #server  start
        self.server_stop=None  #server stopped
        self.logs_textarea=None #textarea for log
        self.logs_label=None #textarea log label name
        self.server_configuration=[None] * 2 #server information label
        self.server_configuration_input = [None] * 2  # server information input
        self.server_status=None  # server status
        self.status_textarea=None #status
        self.status_label=None  #label in status
        self.distiller_property=[None]*2 #Distiller name, address
        self.distiller_property_inputs=[None]*2 #Distiller name, address input field
        self.login=None #login
        self.master_key_label=None #for master key
        self.master_key_input=None # for master password
        self.master_key_ok_button=None #master key ok button
        self.scanning_server_label=None
        self.server_socket = None #socker object for server
        #self.stop_server = None #to stop the server
        self.server_stop=False #bool
        self.master_key=None # to check for master key
        #Production line settings
        self.transport_receiver_label = None
        self.receiver_name_label = None
        self.receiver_id_label = None
        self.transfer_date_label = None
        self.receiver_name_input = None
        self.receiver_id_input = None
        self.transfer_date_input = None
        self.transfer_button = None
        self.user_type=None #user type
        self.box_id_for_invoice=[]
        self.sender_id=None
        self.receiver_id=None
        #production line settings end
        #global products id
        self.product_id=1
        #end products id
        #database connection
        self.client = MongoClient(
                "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
                tlsCAFile=certifi.where())
        #database connection ended
        #setting started
        self.setting=None
        #setting end
        self.create_widgets()
        self.pack()

    # Create Widgets (buttons, labels, etc.)
    def create_widgets(self):
        # main label
        Label(self, text="Track and Trace", font=TITLE_FONT, padx=50, pady=10).grid(row=0, columnspan=3)
        #Label(self, text="Server", font=TITLE_FONT, padx=50, pady=50).place(relx = 0.5, rely = 0.1,anchor = 'center')
        # buttons
        for c in range(3):  # column variable
            self.server_button(c, c)
    def server_button(self, index, c):
        show_text=""
        if c==0:
            show_text="Status"
            self.buttons[index] = Button(self, font=BUTTON_FONT, text=show_text, width=6, height=1,
                                         command=lambda: self.status_press())
            self.buttons[index].grid(row=1, column=c,padx=20,sticky='nsw',pady=10)

        elif c==1:
            show_text = "Configure"
            self.buttons[index] = Button(self, font=BUTTON_FONT, text=show_text, width=6, height=1,
                                         command=lambda: self.configure_press(index))
            self.buttons[index].grid(row=1, column=c,padx=40,sticky='nsw',pady=10)
        else:
            show_text = "Logs"
            self.buttons[index] = Button(self, font=BUTTON_FONT, text=show_text, width=6, height=1,
                                         command=lambda: self.logs_press())
            self.buttons[index].grid(row=1, column=c,padx=20,sticky='nsw', pady=10)
    def clear_previous_screen(self):
        if self.scanning_server_label!=None:
            self.scanning_server_label.grid_forget()
        if self.status_textarea != None:
            self.status_textarea.grid_forget()
        if self.status_label != None:
            self.status_label.grid_forget()
        if self.logs_textarea != None:
            self.logs_textarea.grid_forget()
        if self.logs_label != None:
            self.logs_label.grid_forget()
        if self.server_status != None:
            self.server_status.grid_forget()
        if self.server_start != None:
            self.server_start.grid_forget()
        #if self.server_stop != None:
        #    self.server_stop.grid_forget()
        if self.login != None:
            self.login.grid_forget()
        if self.master_key_label != None:
            self.master_key_label.grid_forget()
        if self.master_key_input != None:
            self.master_key_input.grid_forget()
        if self.master_key_ok_button != None:
            self.master_key_ok_button.grid_forget()

        for j in range(2):
            if self.server_configuration[j] != None:
                self.server_configuration[j].grid_forget()
            if self.server_configuration_input[j] != None:
                self.server_configuration_input[j].grid_forget()
        for i in range(2):
            if self.labels[i] != None:
                self.labels[i].grid_forget()
            if self.inputs[i] != None:
                self.inputs[i].grid_forget()
        for i in range(3):
            if self.opt_buttons[i] != None:
                self.opt_buttons[i].grid_forget()
        for i in range(2):
            if self.distiller_property[i] != None:
                # self.distiller_property[i].destroy()
                self.distiller_property[i].grid_forget()
            if self.distiller_property_inputs[i] != None:
                # self.distiller_property_inputs[i].destroy()
                self.distiller_property_inputs[i].grid_forget()
        if self.transport_receiver_label!=None:
            self.transport_receiver_label.grid_forget()
        if self.receiver_name_label!=None:
            self.receiver_name_label.grid_forget()
        if self.receiver_id_label!=None:
            self.receiver_id_label.grid_forget()
        if self.transfer_date_label!=None:
            self.transfer_date_label.grid_forget()
        if self.receiver_name_input!=None:
            self.receiver_name_input.grid_forget()
        if self.receiver_id_input!=None:
            self.receiver_id_input.grid_forget()
        if self.transfer_date_input!=None:
            self.transfer_date_input.grid_forget()
        if self.transfer_button!=None:
            self.transfer_button.grid_forget()
        if self.setting != None:
            self.setting.grid_forget()
    def configure_press(self, index):
        self.clear_previous_screen()
        #self.buttons[index].configure(bg="red", text="1")
        if (self.stored_info[0]==None and self.stored_info[1]==None):
            for i in range(2):
                label_text=""
                if i==0:
                    label_text = "UserName:"
                else:
                    label_text = "Password:"
                if self.labels[i]!=None:
                    self.labels[i].grid(row=2 + i, column=0, pady=12)
                else:
                    self.labels[i] =Label(self, text = label_text,width=10,font=('Arial', '14','bold'))
                    self.labels[i].grid(row=2+i, column=0, pady=12)
                if self.inputs[i]!=None:
                    self.inputs[i].grid(row=2 + i, column=1, columnspan=2)
                else:
                    if i==0:
                        self.inputs[i] = Entry(self,width=31,font=('Arial', '14'))
                    else:
                        self.inputs[i] = Entry(self, width=31, font=('Arial', '14'), show="*")
                    self.inputs[i].grid(row=2+i,column=1,columnspan=2)
            if self.login!=None:
                self.login.grid(row=4, column=0, columnspan=3)
            else:
                self.login = Button(self, font=BUTTON_FONT, text="Login", width=5, height=1, pady=5,
                                         command=lambda: self.server_started())
                self.login.grid(row=4, column=0, columnspan=3)
        else:
            #self.start_server()
            self.after_switch_config()
        """self.opt_buttons[1] = Button(self, font=BUTTON_FONT, text="Close", width=5, height=1,
                                     command=lambda: self.config_cancel())
        self.opt_buttons[1].grid(row=4, column=1)"""

    def receiver_setting(self):
        self.transport_receiver_label=Label(self, text='Receiver Settings...', foreground="green",
                                                  font=('Arial', '14', 'bold'))
        self.receiver_name_label=Label(self, text = "Rx Name:",width=10,font=('Arial', '14', 'bold'))
        self.receiver_id_label = Label(self, text = "Rx Id:",width=10,font=('Arial', '14', 'bold'))
        self.transfer_date_label = Label(self, text = "Trans. Date:",width=10,font=('Arial', '14', 'bold'))
        self.receiver_name_input= Entry(self,width=31,font=('Arial', '14'))
        self.receiver_id_input=Entry(self,width=31,font=('Arial', '14'))
        self.transfer_date_input=Entry(self,width=31,font=('Arial', '14'))
        self.transfer_button = Button(self, font=BUTTON_FONT, text="Ok", width=5, height=1, pady=5,
                                        command=lambda: self.start_server())
        self.transfer_date_input.insert(INSERT,datetime.datetime.now().date())
        #self.brand_name_input.insert(INSERT,'Signature')
        #self.brand_quantity_input.insert(INSERT,'90')
        self.transport_receiver_label.grid(row=8, column=0, pady=9)
        self.receiver_name_label.grid(row=9, column=0, pady=9)
        self.receiver_id_label.grid(row=10, column=0, pady=9)
        self.transfer_date_label.grid(row=11, column=0, pady=9)
        self.transfer_button.grid(row=12, column=1, pady=9)
        self.receiver_name_input.grid(row=9, column=1, pady=9,columnspan=2)
        self.receiver_id_input.grid(row=10, column=1, pady=9,columnspan=2)
        self.transfer_date_input.grid(row=11, column=1, pady=9,columnspan=2)
    def insert_data_in_products_data(self, data_set=[]):
        db = self.client.Track_and_Trace_data
        collection = db.products_data
        for data in data_set:
            data={"Distiller's Name":data[4],"Product Id":data[0],"Product Brand":data[1],"Product_quantity":data[2],
                  "Manufacturing Date":data[3]}
            #collection.insertOne(data)
            print(data)
    def database_information(self, ids_data=""):
        ids_data=ids_data.split(',')
        list2 = []
        for x in ids_data:
            list1 = []
            list1.append(x)
            if self.receiver_name_input!=None:
                list1.append(self.receiver_name_input.get())
            if self.receiver_id_input!=None:
                list1.append(self.receiver_id_input.get())
            if self.transfer_date_input!=None:
                list1.append(self.transfer_date_input.get())
            if self.distiller_property_inputs[0]!=None:
                list1.append(self.distiller_property_inputs[0].get())
            list2.append(list1)
        return list2
    def getIpAddressofSystem(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
        s.close()
        return ip
    def start_server(self):
        #self.database_information() #testing for database information
        if self.user_type!="Retailor":
            self.check_for_receiver()
            self.insert_data_in_products_data()
        Board.ip_address = self.getIpAddressofSystem()
        print('new ip address: ', Board.ip_address)
        ### production line element removes
        if self.transport_receiver_label!=None:
            self.transport_receiver_label.grid_forget()
        if self.receiver_name_label!=None:
            self.receiver_name_label.grid_forget()
        if self.receiver_id_label!=None:
            self.receiver_id_label.grid_forget()
        if self.transfer_date_label!=None:
            self.transfer_date_label.grid_forget()
        if self.receiver_name_input!=None:
            self.receiver_name_input.grid_forget()
        if self.receiver_id_input!=None:
            self.receiver_id_input.grid_forget()
        if self.transfer_date_input!=None:
            self.transfer_date_input.grid_forget()
        if self.transfer_button!=None:
            self.transfer_button.grid_forget()
        ###
        #self.clear_previous_screen()
        # self.buttons[index].configure(bg="red", text="1")
        if self.scanning_server_label!=None:
            self.scanning_server_label.grid(row=8,column=0, pady=9)
        else:
            self.scanning_server_label = Label(self, text="Internal Server Setting", font=('Arial', '14', 'bold'),foreground="green")
            self.scanning_server_label.grid(row=8 , column=0, pady=9)
        if self.stored_info[0]==None:
            self.stored_info[0]=self.inputs[0].get()
            #print(self.username)
        if self.stored_info[1]==None:
            self.stored_info[1]=self.inputs[1].get()
            #print(self.password)
        for i in range(2):
            label_text = ""
            if i == 0:
                label_text = "IP Address :"
            else:
                label_text = "Port"
            if self.server_configuration[i]!=None:
                self.server_configuration[i].grid(row=9 + i, column=0, pady=9)
            else:
                self.server_configuration[i] = Label(self, text=label_text, font=('Arial', '14', 'bold'))
                self.server_configuration[i].grid(row=9 + i, column=0, pady=9)
            if self.server_configuration_input[i]!=None:
                self.server_configuration_input[i].grid(row=9 + i, column=1, columnspan=2, pady=7)
                if i==0 and self.server_configuration_input[i].index("end") == 0:
                    self.server_configuration_input[i].insert(INSERT, Board.ip_address)
                else:
                    if self.server_configuration_input[i].index("end")==0:
                        self.server_configuration_input[i].insert(INSERT, 2003)
            else:
                self.server_configuration_input[i] = Entry(self, width=31, font=('Arial', '14'))
                self.server_configuration_input[i].grid(row=9 + i, column=1, columnspan=2, pady=7)
                if i==0 and self.server_configuration_input[i].index("end")==0:
                    self.server_configuration_input[i].insert(INSERT, Board.ip_address)
                else:
                    if self.server_configuration_input[i].index("end")==0:
                        self.server_configuration_input[i].insert(INSERT, 2003)

        if self.opt_buttons[0] != None:
            self.opt_buttons[0].grid(row=11, column=0, pady=9)
        else:
            self.opt_buttons[0] = Button(self, font=BUTTON_FONT, text="Start", width=5, height=1,
                                             command=self.button_starter)
            self.opt_buttons[0].grid(row=11, column=0, pady=9)
        if self.opt_buttons[1] != None:
            self.opt_buttons[1].grid(row=11, column=1, pady=9)
        else:
            self.opt_buttons[1] = Button(self, font=BUTTON_FONT, text="Stop", width=5, height=1,
                                             command=self.button_stop_command)
            self.opt_buttons[1].grid(row=11, column=1, pady=9)
        if self.opt_buttons[2] != None:
            self.opt_buttons[2].grid(row=11, column=2, pady=9)
        else:
            self.opt_buttons[2] = Button(self, font=BUTTON_FONT, text="Terminate", width=5, height=1,
                                             command=self.button_close_command)
            self.opt_buttons[2].grid(row=11, column=2, pady=9)
        if self.setting != None:
            self.setting.grid(row=12, column=0,columnspan=3, pady=9)
        else:
            self.setting = Button(self, font=BUTTON_FONT, text="Setting", width=5, height=1,
                                             command=self.setting_call_method)
            self.setting.grid(row=12, column=0,columnspan=3, pady=9)

    def setting_call_method(self):
        print('self.server_stop',self.server_stop)
        if (self.server_stop==None or self.server_stop==True):
            for i in range(2):
                if self.server_configuration[i]!=None:
                    self.server_configuration[i].grid_forget()
                if self.server_configuration_input[i]!=None:
                    self.server_configuration_input[i].grid_forget()
            for i in range(3):
                if self.opt_buttons[i]!=None:
                    self.opt_buttons[i].grid_forget()
            if self.setting!=None:
                self.setting.grid_forget()
            if self.scanning_server_label!=None:
                self.scanning_server_label.grid_forget()
            self.receiver_setting()
            #self.production_line_setting()
        else:
            print("server running firstly stop it")
    def status_press(self, status=""):
        self.clear_previous_screen()
        #self.buttons[index].configure(bg="red", text="2")
        #self.server_status = Label(self, text=status)
        #self.server_status.grid(row=2)
        if self.status_textarea!=None:
            self.status_textarea.grid(row=3, column=0, columnspan=3)
            #self.status_textarea.delete("1.0", "end")
            self.status_textarea.insert(INSERT, status+'\n')
            self.status_textarea.see("end")
        else:
            self.status_textarea = Text(self, height=30, width=60, )
            self.status_textarea.grid(row=3, column=0, columnspan=3)
            self.status_textarea.insert("end", status)
            self.status_textarea.see("end")
        if self.status_label!=None:
            self.status_label.config(font=("Arial", 14, 'bold'))
            self.status_label.grid(row=2, column=0)
        else:
            self.status_label = Label(self, text="Server Logs", pady=10, padx=0,)
            self.status_label.config(font=("Arial", 14, 'bold'))
            self.status_label.grid(row=2, column=0)
    def logs_press(self, fact=""):
        self.clear_previous_screen()
        #self.buttons[index].configure(bg="red", text="3")
        if self.logs_textarea!=None:
            self.logs_textarea.grid(row=3, column=0, columnspan=3)
            self.logs_textarea.insert("end", fact)
            self.logs_textarea.see("end")
        else:
            self.logs_textarea = Text(self, height=30, width=60,)
            self.logs_textarea.grid(row=3, column=0, columnspan=3)
            self.logs_textarea.insert("end", fact)
            self.logs_textarea.see("end")
        if self.logs_label!=None:
            self.logs_label.config(font=("Arial", 14, 'bold'))
            self.logs_label.grid(row=2, column=0)
        else:
            self.logs_label = Label(self, text="Server Logs",pady=10,padx=0)
            self.logs_label.config(font=("Arial", 14,'bold'))
            self.logs_label.grid(row=2,column=0)

    def server_started(self, ip_address='0.0.0.0', port_no=2002):
        #print(self.username,self.password)
        # self.clear_previous_screen()
        check_for_user=""
        for i in range(2):
            if self.server_configuration_input[i]!=None:
                self.stored_info[2+i]=self.server_configuration_input[i].get()
        if self.server_start != None:
            self.server_start.grid_forget()
        #if self.server_stop != None:
        #    self.server_stop.grid_forget()
        if self.server_start!=None:
            self.server_start.grid(row=5, column=0)
        else:
            self.server_start=Label(self,text='Database Connect...',foreground="green",font=('Arial', '14', 'bold'))
            self.server_start.grid(row=5, column=0, )
        # mongodb connection
        if (self.inputs[0].index("end") == 0 or self.inputs[1].index("end") == 0):
            print("enter valid input")
            self.server_start.grid_forget()
        else:
            """client = MongoClient(
                "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
                tlsCAFile=certifi.where())"""
            db = self.client.get_database('track_and_trace_datahub')
            records = db.user_details
            data = []
            condition1 = {"username": self.inputs[0].get()}
            condition2 = {"password": self.inputs[1].get()}
            query = {"$and": [condition1, condition2]}
            data = records.find_one(query)
            self.sender_id=data['uid']
            if (data!=None and len(data)>0):
                self.master_key=data['master_key']
                for i in range(2):
                    text = ""
                    if i == 0:
                        text = "Registered Name:"
                        dist_data = data["registered_name"]
                    else:
                        text = "User Type:"
                        dist_data = data["usertype"]
                        self.user_type = data["usertype"]
                    if self.distiller_property[i] != None:
                        self.distiller_property[i].grid(row=6 + i, column=0, pady=9)
                    else:
                        self.distiller_property[i] = Label(self, text=text, font=('Arial', '14', 'bold'))
                        self.distiller_property[i].grid(row=6 + i, column=0, pady=9)
                    if self.distiller_property_inputs[i] != None:
                        self.distiller_property_inputs[i].grid(row=6 + i, column=1, columnspan=2, pady=7)
                        if self.distiller_property_inputs[i].index("end")==0:
                            self.distiller_property_inputs[i].insert(INSERT,dist_data)
                    else:
                        self.distiller_property_inputs[i] = Entry(self, width=31, font=('Arial', '14'))
                        self.distiller_property_inputs[i].grid(row=6 + i, column=1, columnspan=2, pady=7)
                        if self.distiller_property_inputs[i].index("end") == 0:
                            self.distiller_property_inputs[i].insert(INSERT, dist_data)
                #self.start_server()
                if self.opt_buttons[0]==None or self.opt_buttons[1]==None:
                    if self.user_type=="Retailor":
                        self.start_server()
                    else:
                        self.receiver_setting()
                else:
                    self.start_server()

            else:
                print("Enter valid Input")
                self.server_start.grid_forget()
    def check_for_receiver(self):
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        db = self.client.get_database('track_and_trace_datahub')
        records = db.user_details
        if self.receiver_name_input.index("end")!=0 and self.receiver_id_input.index("end")!=0:
            receiver_id = self.receiver_id_input.get()
            condition2 = {"uid": receiver_id}
            record=records.find_one(condition2)
            if record is not None:
                self.receiver_id=record['uid']
                print(record)
            else:
                print("both invalid input")
        elif self.receiver_id_input.index("end")==0 and self.receiver_name_input.index("end")!=0:
            receiver_name = self.receiver_name_input.get()
            condition1 = {'registered_name': receiver_name}
            record=records.find_one(condition1)
            if record is not None:
                self.receiver_id = record['uid']
                print(record)
            else:
                print("name invalid input")
        elif self.receiver_name_input.index("end")==0 and self.receiver_id_input.index("end")!=0:
            receiver_id = self.receiver_id_input.get()
            condition = {"uid": receiver_id}
            record=records.find_one(condition)
            if record is not None:
                self.receiver_id = record['uid']
                print(record)
            else:
                print("id invalid input")
        else:
            print("not valid user")
    def check_for_product_in_store(self,box_ids_list=[]):
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        db = self.client.get_database('track_and_trace_datahub')
        records = db.store_details
        if len(box_ids_list)!=0:
            for x in box_ids_list:
                query={"box_id":x}
                user = records.find_one(query)
                print(x)
                #print(user)
                if user is None:
                    print("false")
                else:
                    sender_data=[] #sender data
                    #user_id=user['uid']
                    records_usr = db.user_details
                    if not self.check_existence_of_box_in_transport_details(x):
                        user_id = user['uid']
                        sender_data.append(user_id)
                        temp_data = records_usr.find_one({'uid': user_id})
                        sender_data.append(temp_data['usertype'])
                    else:
                        user_name = self.inputs[0].get()
                        str2=records_usr.find_one({'username':user_name})['uid']
                        record_temp=db.transport_details.find_one({'box_id':x})
                        str1=record_temp["to_user"].split(',')[-1]
                        print(str1,str2)
                        if str1==str2:
                            sender_data.append(str1)
                            temp_data = records_usr.find_one({'uid': str1})
                            sender_data.append(temp_data['usertype'])
                            print(sender_data)
                        else:
                            print("invalid")

                    receiver_data=[] #receiver data
                    if self.receiver_id_input!=None and self.receiver_id_input.index("end")!=0:
                        receiver_data.append(self.receiver_id_input.get())
                        temp_data1 = records_usr.find_one({'uid': self.receiver_id_input.get()})
                        receiver_data.append(temp_data1['usertype'])
                    elif self.receiver_name_input!=None and self.receiver_name_input.index("end")!=0:
                        temp_data1 = records_usr.find_one({'registered_name': self.receiver_name_input.get()})
                        receiver_data.append(temp_data1['uid'])
                        receiver_data.append(temp_data1['usertype'])
                    self.change_the_product_status_in_transport_and_update(sender_data, receiver_data,
                                                                      box_id=x)
    def check_existence_of_box_in_transport_details(self, box_id=""):
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        db = self.client.get_database('track_and_trace_datahub')
        temp_data=db.transport_details.find_one({'box_id':box_id})
        if temp_data is not None:
            return True
        else:
            return False
    #invoice generation
    def generate_invoice(self,sender_name, receiver_name,box_id,product_count,product_quantity,total_box,total_product):
        # Generate a simple invoice
        invoice_template = """
        ================================================================
        KARNATAKA(KR) LIQUOR TRANSPORT INVOICE
        ================================================================
        Sender Name: {}
        Receiver Name: {}
        ======================================================
        Box Id: {}
        Box Quantity: {}
        Product Quantity(l/ml): {}
        ======================================================
        Total box:{}  Total Product:{}
        Thank you for ordering!
        ================================================================
        """
        invoice = invoice_template.format(sender_name, receiver_name, box_id, product_count, product_quantity,
                                          total_box, total_product)
        # Display the invoice
        with open('invoice.txt', "w+") as f:
            f.writelines(invoice)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        f = open("invoice.txt", "r")
        for x in f:
            pdf.cell(200, 10, txt=x, ln=1, align='C')
        #pdf.output("invoice.pdf")
        filename=sender_name+'_invoice'
        pdf.output(f"{filename}.pdf")

    def invoice_generation(self):
        db=self.client.get_database('track_and_trace_datahub')
        usr_details=db.user_details
        store_detail=db.store_details
        product_count=[]
        product_quantity=[]
        sender_name="john"
        receiver_name="dsdsd"
        #print(self.sender_id, self.receiver_id)
        sender_name=usr_details.find_one({'uid':self.sender_id})['registered_name']
        receiver_name=usr_details.find_one({'uid':self.receiver_id})['registered_name']
        print('sender_name',sender_name,'receiver_name',receiver_name)
        total_product=0
        for x in self.box_id_for_invoice:
            count=0
            product_quantity.append(store_detail.find_one({'box_id':x})['quantity'])
            for i in store_detail.find({'box_id':x}):
                count+=1
            total_product+=count
            product_count.append(count)
        total_box=len(self.box_id_for_invoice)
        print(self.box_id_for_invoice)
        box_id=[int(x) for x in self.box_id_for_invoice]
        #items_purchased = ["             ".join([str(x), '|', str(y), '|', str(z)]) for x, y, z in zip(self.box_id_for_invoice, product_count, product_quantity)]
        self.generate_invoice(sender_name, receiver_name,box_id, product_count,product_quantity, total_box, total_product)

    def change_the_product_status_in_transport_and_update(self,sender_data=[], receiver_data=[],box_id=""):
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        self.sender_id = sender_data[0]
        self.receiver_id = receiver_data[0]
        db = self.client.get_database('track_and_trace_datahub')

        if not self.check_existence_of_box_in_transport_details(box_id):
            self.box_id_for_invoice.append(box_id)
            if len(sender_data)>0 and len(receiver_data)>0:
                list_id = [0]
                for x1 in db.transport_details.find():
                    list_id.append(x1['id'])
                max_id = max(list_id)
                max_id = max(1, max_id + 1)
                final_data = {"id": max_id,
                              "box_id": box_id,
                              "from_user_type": sender_data[1],
                              "from_user": sender_data[0],
                              "from_user_status": "Dispatched",
                              "to_user_type": receiver_data[1],
                              "to_user": receiver_data[0],
                              "to_user_status": "Received",
                              "date": str(datetime.datetime.now().date())}
                db.transport_details.insert_one(final_data)
        else:
            for x1 in db.transport_details.find():
                query={"box_id": box_id}
                update_field = {"$set": {"from_user_type": x1['from_user_type']+','+sender_data[1],
                                         "from_user": x1["from_user"]+','+sender_data[0],
                                         "from_user_status": x1["from_user_status"]+','+"Dispatched",
                                         "to_user_type": x1["to_user_type"]+','+receiver_data[1],
                                         "to_user": x1["to_user"]+','+receiver_data[0],
                                         "to_user_status": x1["to_user_status"]+','+"Received",
                                         "date": x1["date"]+','+str(datetime.datetime.now().date())}}
                db.transport_details.update_one(query, update_field)
    def retailor_is_user_then_perform_operation(self,ids_list=[]):
        #print("hi I'm in")
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        db = self.client.get_database('track_and_trace_datahub')
        records=db.store_details
        records_trans=db.transport_details
        usr_record=db.user_details
        print("product_list:",ids_list)
        for x in ids_list:
            #data=records.find_one({"product_qrcode":x})
            data = []
            for x1 in records.find():
                if int(x1['product_qrcode']) == int(x):
                    data.append(x1)
            data = data[0]
            print('data',data)
            data_temp = records_trans.find_one({"box_id":data['box_id']})
            print('data',data,'data_temp',data_temp)
            #print('data_temp',data_temp,'data',data)
            if (data is not None and data_temp is not None):
                retailor_id=data_temp['to_user'].split(',')[-1]
                print(retailor_id)
                username1=self.inputs[0].get()
                ret_id=usr_record.find_one({'username':username1})['uid']
                print('ret_id',ret_id)
                if (retailor_id==ret_id):
                    update_field={"$set": {"product_status": "out"}}
                    if data is not None:
                        if data['product_status']=="in":
                            db.store_details.update_one({"product_qrcode":x}, update_field)
                            print("ok retailor updated")
                        else:
                            tkinter.messagebox.showinfo("error","not updated product status-out")
            else:
                tkinter.messagebox.showinfo("error", "not possible")
    def config_cancel(self):
        self.clear_previous_screen()

    def after_switch_config(self):
        self.clear_previous_screen()
        if self.master_key_label!=None:
            self.master_key_label.grid(row=2, column=0, pady=9)
        else:
            self.master_key_label = Label(self, text="Master Key", font=('Arial', '14', 'bold'))
            self.master_key_label.grid(row=2, column=0, pady=9)
        if self.master_key_input!=None:
            self.master_key_input.grid(row=2, column=1, columnspan=2, pady=7)

        else:
            self.master_key_input = Entry(self, width=31, font=('Arial', '14'))
            self.master_key_input.grid(row=2, column=1, columnspan=2, pady=7)
        if self.master_key_ok_button!=None:
            self.master_key_ok_button.grid(row=4, column=0, pady=7, columnspan=3)
        else:
            self.master_key_ok_button = Button(self, font=BUTTON_FONT, text="Ok", width=5, height=1,
                                         command=lambda: self.after_master_key_ok())
            self.master_key_ok_button.grid(row=4, column=0, pady=7,columnspan=3)
    def after_master_key_ok(self):
        #hidding  transport
        if self.transport_receiver_label!=None:
            self.transport_receiver_label.grid_forget()
        if self.receiver_name_label!=None:
            self.receiver_name_label.grid_forget()
        if self.receiver_id_label!=None:
            self.receiver_id_label.grid_forget()
        if self.transfer_date_label!=None:
            self.transfer_date_label.grid_forget()
        if self.receiver_name_input!=None:
            self.receiver_name_input.grid_forget()
        if self.receiver_id_input!=None:
            self.receiver_id_input.grid_forget()
        if self.transfer_date_input!=None:
            self.transfer_date_input.grid_forget()
        if self.transfer_button!=None:
            self.transfer_button.grid_forget()
        ##
        #hidding username and password

        if self.master_key_input.index("end") != 0:
            a=self.master_key_input.get()
            b=self.master_key
            if self.master_key_label!=None:
                self.master_key_label.grid_forget()
            if self.master_key_input!=None:
                self.master_key_input.delete(0, END)
                self.master_key_input.grid_forget()
                self.stored_info[4]=self.master_key_input.get()
            if self.master_key_ok_button!=None:
                self.master_key_ok_button.grid_forget()
            if (self.stored_info[0]!=None and self.stored_info[1]!=None):
                if (a==b):
                    if self.server_start!=None:
                        self.server_start.grid(row=2, column=0, )
                    else:
                        self.server_start = Label(self, text='Database Connect...', foreground="green",
                                                  font=('Arial', '14', 'bold'))
                        self.server_start.grid(row=2, column=0, )
                    for i in range(2):
                        self.labels[i].grid(row=3+i,column=0,pady=12)
                        self.inputs[i].grid(row=3+i,column=1, columnspan=2)

                    self.server_started()
                else:
                    self.master_key_label.grid(row=2, column=0, pady=9)
                    self.master_key_input.grid(row=2, column=1, columnspan=2, pady=7)
                    self.master_key_ok_button.grid(row=4, column=0, pady=7, columnspan=3)
                    print("Enter valid Input")
            else:
                self.master_key_label.grid(row=2, column=0, pady=9)
                self.master_key_input.grid(row=2, column=1, columnspan=2, pady=7)
                self.master_key_ok_button.grid(row=4, column=0, pady=7, columnspan=3)
                print("Enter valid Input")
            #print('actual_id',self.master_key)

            #for i in range(5):
            #    print(type(self.stored_info[i]))
        else:
            self.master_key_label.grid(row=2, column=0, pady=9)
            self.master_key_input.grid(row=2, column=1, columnspan=2, pady=7)
            self.master_key_ok_button.grid(row=4, column=0, pady=7, columnspan=3)
            print("Enter valid input")
    def status_listening(self):
        if self.status_textarea != None:
            self.status_textarea.delete("1.0", "end")
            #print('status1')
            self.status_textarea.insert(INSERT, "Listening" + "\n")
        else:
            self.status_textarea = Text(self, height=30, width=60, )
            #print('status2')
            self.status_textarea.insert(INSERT, "Listening" + "\n")
    def logs_listening(self):
        if self.logs_textarea != None:
            self.logs_textarea.delete("1.0", "end")
            #print('logs1')
            self.logs_textarea.insert(INSERT, "Listening" + "\n")
        else:
            self.logs_textarea = Text(self, height=30, width=60, )
            #print('logs2')
            # self.logs_textarea.delete("1.0","end")
            self.logs_textarea.insert(INSERT, "Listening" + "\n")
    def server_communication(self):
        print(Board.ip_address,Board.port)
        self.logs_listening()
        self.status_listening()
        #self.logs_press()
        try:
            self.server_stop = False
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #port_no = 2001
            self.server_socket.bind((Board.ip_address, Board.port))
            #self.server_socket.bind((Board.ip_address, Board.port))
            self.server_socket.listen(5)
            print('Server Started')
            print('server listening from ...', datetime.datetime.now())
            self.status_textarea.insert(INSERT,'Server Started\n')
            self.status_textarea.insert(INSERT, f'IP Address: {Board.ip_address}\n')
            self.status_textarea.insert(INSERT, f'Port: {Board.port}\n')
            self.status_textarea.insert(INSERT, f'server listening from ... {datetime.datetime.now()}\n')
            self.logs_press()
            #SET text in status box
            #self.status_textarea.insert(INSERT,'Server Started')
            while True and not self.server_stop:
                conn, addr = self.server_socket.accept()
                from_client = ''
                while True and not self.server_stop:
                    data = conn.recv(4096)

                    if (not data): break
                    from_client += data.decode('utf8')
                    text=from_client + ' Port ' + str(Board.port) + ' Time: ' + str(datetime.datetime.now())
                    print(text)
                    #here database connection for fetching ids
                    from_client=from_client.split(',')
                    #print('self.user_type',self.user_type)
                    if self.user_type!="Retailor":
                        self.check_for_product_in_store(from_client)
                        print('true')
                        #self.insert_data_in_products_data(self.database_information(from_client))
                    else:
                        self.retailor_is_user_then_perform_operation(from_client)
                        print('false')

                    #
                    # end database connection for fetching ids
                    if self.logs_textarea!=None:
                        self.logs_textarea.insert(INSERT,text+'\n')
                    else:
                        #self.logs_press()
                        self.logs_textarea.insert(INSERT, text+'\n')
                        self.logs_press()
                    time.sleep(0.1)
                    # conn.send("received".encode())
                    # handle_termination()
                conn.close()
            print('server disconnected and shutdown')
            self.status_textarea.insert(INSERT,'server disconnected and shutdown' + '\n')
        except Exception as e:
            print(f'{e}: Connection Terminated')
            tkinter.messagebox.showinfo("error",'Connection Terminated')
            self.status_textarea.insert( INSERT,'Connection Terminated'+ '\n')


    def button_close_command(self):
        # If the close button is pressed then terminate the application
        if  self.master!= None:
            self.master.destroy()

    def button_stop_command(self):
        #generate invoice
        self.invoice_generation()
        self.box_id_for_invoice.clear()
        # If the STOP button is pressed then terminate the loop
        self.server_stop = True
        # server_socket.shutdown(socket.SHUT_RDWR)
        if self.server_socket != None:
            self.server_socket.close()

    def button_starter(self):
        # t = threading.Thread(target=button_start_command)
        Board.ip_address=self.server_configuration_input[0].get()
        Board.port=int(self.server_configuration_input[1].get())
        #print(Board.ip_address,Board.port)
        t = threading.Thread(target=self.server_communication)
        t.start()








# Create the GUI
tk = Tk()
tk.title("Transport Server")

board = Board(tk)
tk.mainloop()