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
        self.production_line_label = None
        self.brand_name_label = None
        self.brand_quantity_label = None
        self.production_date_label = None
        self.brand_name_input = None
        self.brand_quantity_input = None
        self.production_date_input = None
        self.production_button = None
        self.box_quantity_size_label = None
        self.box_quantity_size_input = None
        self.production_line_name_label = None
        self.production_line_name_input = None
        self.box_id=None
        self.hostname = socket.gethostname()
        #production line settings end
        #global products id
        self.product_id=1
        #end products id
        #database connection
        self.client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        #database connection ended
        #setting for server
        self.setting=None
        #end setting
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
        if self.production_line_label!=None:
            self.production_line_label.grid_forget()
        if self.brand_name_label!=None:
            self.brand_name_label.grid_forget()
        if self.brand_quantity_label!=None:
            self.brand_quantity_label.grid_forget()
        if self.production_date_label!=None:
            self.production_date_label.grid_forget()
        if self.brand_name_input!=None:
            self.brand_name_input.grid_forget()
        if self.brand_quantity_input!=None:
            self.brand_quantity_input.grid_forget()
        if self.production_date_input!=None:
            self.production_date_input.grid_forget()
        if self.production_button!=None:
            self.production_button.grid_forget()
        if self.box_quantity_size_label!=None:
            self.box_quantity_size_label.grid_forget()
        if self.box_quantity_size_input!=None:
            self.box_quantity_size_input.grid_forget()
        if self.production_line_name_label!=None:
            self.production_line_name_label.grid_forget()
        if self.production_line_name_input!=None:
            self.production_line_name_input.grid_forget()
        if self.setting!=None:
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

    def production_line_setting(self):
        self.production_line_label=Label(self, text='Prod. line Settings...', foreground="green",
                                                  font=('Arial', '14', 'bold'))
        self.brand_name_label=Label(self, text = "Brand Name",width=10,font=('Arial', '14', 'bold'))
        self.brand_quantity_label = Label(self, text = "Quantity(ml)",width=10,font=('Arial', '14', 'bold'))
        self.production_date_label = Label(self, text = "Mfg. Date",width=10,font=('Arial', '14', 'bold'))
        self.brand_name_input= Entry(self,width=31,font=('Arial', '14'))
        self.brand_quantity_input=Entry(self,width=31,font=('Arial', '14'))
        self.production_date_input=Entry(self,width=31,font=('Arial', '14'))
        self.box_quantity_size_label = Label(self, text = "Box Quantity",width=10,font=('Arial', '14', 'bold'))
        self.box_quantity_size_input = Entry(self,width=31,font=('Arial', '14'))
        self.production_line_name_label = Label(self, text="Box Quantity", width=10, font=('Arial', '14', 'bold'))
        self.production_line_name_input = Entry(self, width=31, font=('Arial', '14'))
        self.production_button = Button(self, font=BUTTON_FONT, text="Ok", width=5, height=1, pady=5,
                                        command=lambda: self.start_server())
        self.production_date_input.insert(INSERT,datetime.datetime.now().date())
        self.brand_name_input.insert(INSERT,'Signature')
        self.brand_quantity_input.insert(INSERT,'90')
        self.box_quantity_size_input.insert(INSERT, '2')
        self.production_line_name_input.insert(INSERT, 'line-1')
        self.production_line_label.grid(row=8, column=0, pady=3)
        self.brand_name_label.grid(row=9, column=0, pady=3)
        self.brand_quantity_label.grid(row=10, column=0, pady=3)
        self.production_date_label.grid(row=11, column=0, pady=3)
        self.box_quantity_size_label.grid(row=12, column=0, pady=3)
        self.production_line_name_label.grid(row=13, column=0, pady=3)
        self.production_button.grid(row=14, column=1, pady=3)
        self.brand_name_input.grid(row=9, column=1, pady=3,columnspan=2)
        self.brand_quantity_input.grid(row=10, column=1, pady=3,columnspan=2)
        self.production_date_input.grid(row=11, column=1, pady=3,columnspan=2)
        self.box_quantity_size_input.grid(row=12, column=1, pady=3, columnspan=2)
        self.production_line_name_input.grid(row=13, column=1, pady=3, columnspan=2)
    def check_for_product_existed(self,product_id,box_id=""):
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        db = self.client.get_database('track_and_trace_datahub')
        collection = db.store_details
        data=collection.find_one({"product_qrcode":product_id})
        if data is None:
            return True
        else:
            return False
    def insert_data_in_products_data(self, data_set=[]):
        #db = self.client.Track_and_Trace_data
        #collection = db.products_data
        """client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())"""
        db = self.client.get_database('track_and_trace_datahub')
        collection=db.store_details
        collection_temp=db.user_details
        uid=collection_temp.find_one({'username':self.inputs[0].get()})['uid']
        id_list=[0]
        #only for data generation
        if self.box_id!=None:
            box_id=self.box_id
        else:
            if len(list(collection.find()))==0:
                box_id=1
            else:
                box_id=max([int(x['box_id']) for x in collection.find()])+1
        for x in collection.find():
            id_list.append(x['id'])
        counter=0
        for data in data_set:
            #data={"Distiller's Name":data[4],"Product Id":data[0],"Product Brand":data[1],"Product_quantity":data[2],
            #      "Manufacturing Date":data[3]}
            if self.check_for_product_existed(data[0]):
                date_data=datetime.datetime.now()
                data={"id":max(id_list)+1+counter,"uid":uid,"box_id":str(box_id),"product_qrcode":data[0],"product_status":"in","brand":data[1],"quantity":int(data[2]),
                      "mfg_date":str(data[3]),"time_stemp":str(date_data.time()),"date":str(date_data.date()),"production_line":data[4],"system_id":self.hostname}
                counter+=1
                collection.insert_one(data)
                #print(data)
            else:
                tkinter.messagebox.showinfo("Error","Invalid product id/already used")
                print("invalid")
    def database_information(self, ids_data=""):
        ids_data=ids_data.split(',')
        list2 = []
        for x in ids_data:
            list1 = []
            list1.append(x)
            if self.brand_name_input!=None:
                list1.append(self.brand_name_input.get())
            if self.brand_quantity_input!=None:
                list1.append(self.brand_quantity_input.get())
            if self.production_date_input!=None:
                list1.append(self.production_date_input.get())
            if self.production_line_name_input!=None:
                list1.append(self.production_line_name_input.get())
            list2.append(list1)
        #print(list2)
        return list2
    def getIpAddressofSystem(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
        s.close()
        return ip
    def setting_call_method(self):
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
            self.production_line_setting()
        else:
            print("server running firstly stop it")

    def start_server(self):
        #self.database_information() #testing for database information
        self.insert_data_in_products_data()
        Board.ip_address = self.getIpAddressofSystem()
        print('new ip address: ', Board.ip_address)
        ### production line element removes
        if self.production_line_label!=None:
            self.production_line_label.grid_forget()
        if self.brand_name_label!=None:
            self.brand_name_label.grid_forget()
        if self.brand_quantity_label!=None:
            self.brand_quantity_label.grid_forget()
        if self.production_date_label!=None:
            self.production_date_label.grid_forget()
        if self.brand_name_input!=None:
            self.brand_name_input.grid_forget()
        if self.brand_quantity_input!=None:
            self.brand_quantity_input.grid_forget()
        if self.production_date_input!=None:
            self.production_date_input.grid_forget()
        if self.production_button!=None:
            self.production_button.grid_forget()
        if self.box_quantity_size_label!=None:
            self.box_quantity_size_label.grid_forget()
        if self.box_quantity_size_input!=None:
            self.box_quantity_size_input.grid_forget()
        if self.production_line_name_label!=None:
            self.production_line_name_label.grid_forget()
        if self.production_line_name_input!=None:
            self.production_line_name_input.grid_forget()
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
                        self.server_configuration_input[i].insert(INSERT, 9004)
            else:
                self.server_configuration_input[i] = Entry(self, width=31, font=('Arial', '14'))
                self.server_configuration_input[i].grid(row=9 + i, column=1, columnspan=2, pady=7)
                if i==0 and self.server_configuration_input[i].index("end")==0:
                    self.server_configuration_input[i].insert(INSERT, Board.ip_address)
                else:
                    if self.server_configuration_input[i].index("end")==0:
                        self.server_configuration_input[i].insert(INSERT, 9004)

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
            self.setting.grid(row=12, column=0,columnspan=3,pady=9)
        else:
            self.setting = Button(self, font=BUTTON_FONT, text="Setting", width=5, height=1,
                                             command=lambda: self.setting_call_method())
            self.setting.grid(row=12, column=0,columnspan=3,pady=9)

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
        """
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client.Track_and_Trace_data
        collection = db.distiller_details
        data=[]
        if (self.inputs[0].index("end") == 0 or self.inputs[1].index("end") == 0):
            print("enter valid input")
            self.server_start.grid_forget()
        else:
            condition1={"email_id":self.inputs[0].get()}
            if (self.inputs[1].get().isdigit()):
                condition2 = {"password": int(self.inputs[1].get())}
            else:
                condition2 = {"password": self.inputs[1].get()}
            query = {"$and": [condition1, condition2]}
            data=[ x for x in collection.find(query,{'photograph':0,'manufacturer_place':0,
                                                                   'manufacturer_id':0,'registration_date':0,'email_id':0,
                                                                'phone_no':0,'password':0})]
            """
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
            #print(data)
            if (data!=None and len(data)>0):
                self.master_key=data['master_key']
                for i in range(2):
                    text = ""
                    if i == 0:
                        text = "Distiller's Name:"
                        dist_data = data["registered_name"]
                    else:
                        text = "User Type:"
                        dist_data = data["usertype"]
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
                    self.production_line_setting()
                else:
                    self.start_server()
            else:
                print("Enter valid Input")
                self.server_start.grid_forget()
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
        #hidding production line
        if self.production_line_label!=None:
            self.production_line_label.grid_forget()
        if self.brand_name_label!=None:
            self.brand_name_label.grid_forget()
        if self.brand_quantity_label!=None:
            self.brand_quantity_label.grid_forget()
        if self.production_date_label!=None:
            self.production_date_label.grid_forget()
        if self.brand_name_input!=None:
            self.brand_name_input.grid_forget()
        if self.brand_quantity_input!=None:
            self.brand_quantity_input.grid_forget()
        if self.production_date_input!=None:
            self.production_date_input.grid_forget()
        if self.box_quantity_size_label!=None:
            self.box_quantity_size_label.grid_forget()
        if self.box_quantity_size_input!=None:
            self.box_quantity_size_input.grid_forget()
        if self.production_line_name_label!=None:
            self.production_line_name_label.grid_forget()
        if self.production_line_name_input!=None:
            self.production_line_name_input.grid_forget()
        ##
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
            counter = 0
            product_stock = []
            while True and not self.server_stop:
                conn, addr = self.server_socket.accept()
                from_client = ''
                while True and not self.server_stop:
                    data = conn.recv(4096)

                    if (not data): break
                    from_client = data.decode('utf8')
                    if '/' in from_client:
                        self.box_id=from_client.split('/')[0]
                        counter=0
                    else:
                        if 'ERROR' not in from_client:
                            product_stock+=list(from_client.split(','))
                            product_stock=list(set(product_stock))
                            counter=len(product_stock)
                    #text=from_client + ' Port ' + str(Board.port) + ' Time: ' + str(datetime.datetime.now())
                    print(from_client)
                    if self.logs_textarea!=None:
                        self.logs_textarea.insert(INSERT,from_client+'\n')
                    else:
                        #self.logs_press()
                        self.logs_textarea.insert(INSERT, from_client+'\n')
                        self.logs_press()
                    #print('counter',counter,'product',product_stock)
                    #here database connection for fetching ids
                    if self.box_quantity_size_input!=None:
                        if counter==int(self.box_quantity_size_input.get()):
                            product_stock=product_stock[::-1]
                            self.insert_data_in_products_data(self.database_information(','.join(product_stock)))
                            print("completed")
                            counter=0
                            self.box_id=None
                            product_stock=[]

                    # end database connection for fetching ids
                    time.sleep(0.1)
                    # conn.send("received".encode())
                    # handle_termination()
                conn.close()
            print('server disconnected and shutdown')
            self.status_textarea.insert(INSERT,'server disconnected and shutdown' + '\n')
        except Exception as e:
            print(e)
            print(f'{e}: Connection Terminated')
            self.status_textarea.insert( INSERT,'Connection Terminated'+ '\n')


    def button_close_command(self):
        # If the close button is pressed then terminate the application
        if  self.master!= None:
            self.master.destroy()

    def button_stop_command(self):
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
tk.title("Server")

board = Board(tk)
tk.mainloop()