from CTkMessagebox import CTkMessagebox
from customtkinter import *
import customtkinter as ctk
from PIL import Image
import datetime
from pymongo import MongoClient
import certifi
import socket
import datetime
import time
import threading
from fpdf import FPDF
class Board(ctk.CTk):
    #server configuration
    ip_address = "0.0.0.0"
    port = 9004
    # Constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Transport Server')
        self.geometry("856x645")
        self.resizable(True, True)
        self.frame=CTkFrame(master=self, width=856, height=645, fg_color="#ffffff")
        #Login section
        self.side_img_data = Image.open("./all_images/side-img.png")
        self.email_icon_data = Image.open("./all_images/user.png")
        self.password_icon_data = Image.open("./all_images/password-icon.png")
        self.logo_icon_data = Image.open("./all_images/logo_old.png")
        self.side_img = CTkImage(dark_image=self.side_img_data, light_image=self.side_img_data, size=(428, 645))
        self.email_icon = CTkImage(dark_image=self.email_icon_data, light_image=self.email_icon_data, size=(35, 35))
        self.password_icon = CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data, size=(29, 29))
        self.logo_icon = CTkImage(dark_image=self.logo_icon_data, light_image=self.logo_icon_data, size=(50, 50))
        self.left_side_image=None
        self.login_label=[None]*5
        self.login_input=[None]*2
        self.login_button=None
        # End Login
        #Main Form page Start
        self.main_view = CTkFrame(master=self, fg_color="#fff",  width=680, height=650, corner_radius=0)
        #Database connection
        self.client = MongoClient(
            "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        #user frame
        self.user_header_container=None
        self.user_container=None
        self.ok_img_data = Image.open("./all_images/ok_logo.png")
        #transport frame
        self.transport_header_container=None
        self.transport_container=None
        self.transport_button_container=None
        self.receiver_frame=None
        #server frame
        self.server_header_container=None
        self.server_container=None
        #master key frame
        self.master_container=None
        #status frame
        self.status_label_container=None
        self.status_textbox_container=None
        self.status_button_container=None
        #logs frame
        self.logs_label_container=None
        self.logs_textbox_container=None
        self.logs_button_container=None
        #Main form page End
        #elements of customtkinter
        self.cancel_img_data = Image.open("./all_images/terminate_logo.png")
        self.master_key = ""
        self.master_key_input=None
        self.master_key_button = None
        #elements of user page
        self.usertype=""
        self.user_id=""
        self.username=""
        self.registered_name=""
        self.email_id=""
        self.contact_no=""
        self.address=""
        #transport elements
        #self.receiver_showframe=None
        self.transport_name=None
        self.transport_id=None
        self.transport_date=None
        self.transport_button_ok=None
        self.transport_button_cancel=None
        self.transport_server_label=None
        self.transport_name_label=None
        self.transport_id_label=None
        self.transport_date_label=None
        #server elements
        self.ip_address_input=None
        self.port_input=None
        self.server_header_label=None
        self.ip_address_label=None
        self.ip_address_input=None
        self.port_label=None
        self.port_input=None
        self.server_button_start=None
        self.server_button_stop=None
        self.server_button_terminate=None
        #status element
        self.status_textarea=None
        self.status_label=None
        self.status_button=None

        #logs element
        self.logs_textarea=None
        self.logs_label = None
        self.logs_button = None

        #other variables
        self.receiver_showlabel=None
        self.receiver_name_showlabel=None
        self.receiver_type_showlabel=None
        self.receiver_name=""
        self.receiver_type=""
        self.sender_id = None
        self.receiver_id = None
        self.box_id_for_invoice=[]
        self.option_showing_status=False
        self.function_name=""
        self.configure_called=False  #for configure method
        self.server_running_status=False
        self.server_socket = None
        self.server_stop = False  # bool
        self.product_id = 1
        self.box_id = None
        self.box_quantity = []
        self.box_quantity_temp = []
        self.hostname = socket.gethostname()
        self.login()
    def login_data(self):
        #add login verification
        username=self.login_input[0].get()
        password=self.login_input[1].get()
        if (self.login_input[0].index("end") == 0 or self.login_input[1].index("end") == 0):
            CTkMessagebox(title="Error", message="Invalid Username/Password", icon="cancel")
            print("enter valid input")

            #self.login_data()
        else:
            db = self.client.get_database('track_and_trace_datahub')
            records = db.user_details
            data = []
            condition1 = {"username": username}
            condition2 = {"password": password}
            #print(condition1, condition2)
            query = {"$and": [condition1, condition2]}
            data = records.find_one(query)
            #print(data)
            if (data != None and len(data) > 0):
                self.master_key = data['master_key']
                self.usertype = data['usertype']
                self.user_id = data['uid']
                self.username = data['username']
                self.registered_name = data['registered_name']
                self.email_id = data['email']
                self.contact_no = data['contact_no']
                self.address = data['Address']
                #for clearing current page
                self.clear_screen()
                #calling main page
                self.sidebar_showing()
                self.main_page()
            else:
                CTkMessagebox(title="Error", message="Invalid Username/Password", icon="cancel")
    def clear_screen(self):
        self.frame.pack_forget()
    def clear_main_page_content(self):
        # user frame
        if self.user_header_container != None:
            self.user_header_container.pack_forget()
        if self.user_container != None:
            self.user_container.pack_forget()
        self.ok_img_data = Image.open("./all_images/ok_logo.png")
        # transport frame
        if self.transport_header_container != None:
            self.transport_header_container.pack_forget()
        if self.transport_container != None:
            self.transport_container.pack_forget()
        if self.transport_button_container != None:
            self.transport_button_container.pack_forget()
        # server frame
        if self.server_header_container != None:
            self.server_header_container.pack_forget()
        if self.server_container != None:
            self.server_container.pack_forget()
        if self.server_header_label != None:
            self.server_header_label.pack_forget()
        if self.ip_address_label != None:
            self.ip_address_label.grid_forget()
        if self.ip_address_input != None:
            self.ip_address_input.grid_forget()
        if self.port_label != None:
            self.port_label.grid_forget()
        if self.port_input != None:
            self.port_input.grid_forget()
        if self.server_button_start != None:
            self.server_button_start.grid_forget()
        if self.server_button_stop != None:
            self.server_button_stop.grid_forget()
        if self.server_button_terminate != None:
            self.server_button_terminate.grid_forget()
        # master key frame
        if self.master_container != None:
            self.master_container.pack_forget()
        #if self.master_key != None:
        #    self.master_key.grid_forget()
        # status frame
        if self.status_label_container != None:
            self.status_label_container.pack_forget()

        if self.status_textbox_container != None:
            self.status_textbox_container.pack_forget()

        if self.status_button_container != None:
            self.status_button_container.pack_forget()
        # logs frame
        if self.logs_label_container != None:
            self.logs_label_container.pack_forget()

        if self.logs_textbox_container != None:
            self.logs_textbox_container.pack_forget()

        if self.logs_button_container != None:
            self.logs_button_container.pack_forget()
        #status textarea
        if self.status_textarea != None:
            self.status_textarea.pack_forget()
        if self.status_label != None:
            self.status_label.pack_forget()
        if self.status_button != None:
            self.status_button.pack_forget()
        #logs textarea
        if self.logs_textarea != None:
            self.logs_textarea.pack_forget()
        if self.logs_label != None:
            self.logs_label.pack_forget()
        if self.logs_button != None:
            self.logs_button.pack_forget()
        #transport info
        if self.transport_id!= None:
            self.transport_id.grid_forget()
        if self.transport_name!= None:
            self.transport_name.grid_forget()
        if self.transport_date!= None:
            self.transport_date.grid_forget()
        if self.transport_server_label != None:
            self.transport_server_label.grid_forget()
        if self.transport_name_label != None:
            self.transport_name_label.grid_forget()
        if self.transport_id_label != None:
            self.transport_id_label.grid_forget()
        if self.transport_id_label != None:
            self.transport_id_label.grid_forget()
        if self.receiver_frame != None:
            self.receiver_frame.pack_forget()
        if self.receiver_showlabel != None:
            self.receiver_showlabel.pack_forget()
        if self.receiver_name_showlabel != None:
            self.receiver_name_showlabel.pack_forget()
        if self.receiver_type_showlabel != None:
            self.receiver_type_showlabel.pack_forget()

    def login(self):
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="right")
        self.left_side_image = CTkLabel(master=self.frame, text="", image=self.side_img)
        self.left_side_image.pack(expand=True, side="left")

        self.login_label[0]=CTkLabel(master=self.frame, text="  Karnataka Brewers & Distillers Association      ", text_color="#601E88",
                 justify="right", font=("Arial Bold", 16), image=self.logo_icon, compound="left")
        self.login_label[0].pack(anchor="w",pady=(46, 0),padx=(25, 0))

        self.login_label[1]=CTkLabel(master=self.frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left",font=("Arial Bold", 26))
        self.login_label[1].pack(anchor="w", pady=(50, 5), padx=(25, 0))
        self.login_label[2]=CTkLabel(master=self.frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left",font=("Arial Bold", 16))
        self.login_label[2].pack(anchor="w", padx=(25, 0))
        self.login_label[3]=CTkLabel(master=self.frame, text="  Username:", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 19), image=self.email_icon, compound="left")
        self.login_label[3].pack(anchor="w", pady=(46, 10),padx=(25, 0))
        self.login_input[0] = CTkEntry(master=self.frame, width=250,height=35, fg_color="#EEEEEE", border_color="#601E88", border_width=1,text_color="#000000")
        self.login_input[0].pack(anchor="w", padx=(25, 0))
        self.login_label[4]=CTkLabel(master=self.frame, text="  Password:", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 19), image=self.password_icon, compound="left")
        self.login_label[4].pack(anchor="w", pady=(30, 10),padx=(25, 0))
        self.login_input[1] = CTkEntry(master=self.frame, width=250,height=35, fg_color="#EEEEEE", border_color="#601E88", border_width=1,text_color="#000000", show="*")
        self.login_input[1].pack(anchor="w", padx=(25, 0))
        self.login_button=CTkButton(master=self.frame, command=self.login_data, text="Login", fg_color="#601E88", hover_color="#2A8C55",
                  font=("Arial Bold", 20), text_color="#ffffff", width=250, height=40)
        self.login_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))
    #main page method starting
    # user details starting
    def user_details(self):
        self.clear_main_page_content()
        if not self.option_showing_status:
            self.master_key_showing("user_details")
        if self.option_showing_status:
            self.user_header_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.user_header_container.pack(fill="x", pady=(45, 0), padx=10)
            self.user_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.user_container.pack(fill="x", pady=(10, 0), padx=10)
            CTkLabel(master=self.user_header_container, text="User Details", font=("Arial Black", 18),
                     text_color="#2A8C55").pack(anchor="center", ipady=10, pady=(0, 0))
            CTkLabel(master=self.user_container, text="User Type", font=("Arial Black", 14), text_color="#2A8C55").grid(row=1,column=0,padx=(10, 0),pady=15)
            temp_usertype=CTkEntry(master=self.user_container, width=200,placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_usertype.insert(INSERT,self.usertype)
            temp_usertype.grid(row=1, column=1, padx=(10, 0), pady=15)
            CTkLabel(master=self.user_container, text="User Id", font=("Arial Black", 14), text_color="#2A8C55").grid(row=1,column=2,padx=(10, 0),pady=15)
            temp_userid=CTkEntry(master=self.user_container, width=200, placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_userid.insert(INSERT,self.user_id)
            temp_userid.grid(row=1, column=3, padx=(10, 0), pady=15)
            CTkLabel(master=self.user_container, text="User Name", font=("Arial Black", 14), text_color="#2A8C55").grid(row=2,column=0,padx=(10, 0),pady=15)
            temp_username=CTkEntry(master=self.user_container, width=200, placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_username.insert(INSERT,self.username)
            temp_username.grid(row=2, column=1, padx=(10, 0), pady=15)
            CTkLabel(master=self.user_container, text="Reg. Name", font=("Arial Black", 14), text_color="#2A8C55").grid(row=2,column=2,padx=(10, 0),pady=15)
            temp_regname=CTkEntry(master=self.user_container, width=200,placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_regname.insert(INSERT,self.registered_name)
            temp_regname.grid(row=2, column=3, padx=(10, 0), pady=15)
            CTkLabel(master=self.user_container, text="Email Id", font=("Arial Black", 14), text_color="#2A8C55").grid(row=3,column=0,padx=(10, 0), pady=15)
            temp_email=CTkEntry(master=self.user_container, width=200, placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_email.insert(INSERT,self.email_id)
            temp_email.grid(row=3, column=1, padx=(10, 0), pady=15)
            CTkLabel(master=self.user_container, text="Contact No.", font=("Arial Black", 14), text_color="#2A8C55").grid(row=3,column=2,padx=(10, 0),pady=15)
            temp_contact=CTkEntry(master=self.user_container, width=200, placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_contact.insert(INSERT,self.contact_no)
            temp_contact.grid(row=3, column=3, padx=(10, 0), pady=15)
            CTkLabel(master=self.user_container, text="Address", font=("Arial Black", 14), text_color="#2A8C55").grid(row=4,column=0,padx=(10, 0),pady=15)
            temp_address=CTkEntry(master=self.user_container, width=515, placeholder_text="", border_color="#2A8C55", border_width=2)
            temp_address.insert(INSERT,self.address)
            temp_address.grid(row=4, column=1, padx=(10, 0), columnspan=3, pady=15)
            ok_img_data = Image.open("./all_images/terminate_logo.png")
            ok_img = CTkImage(light_image=ok_img_data, dark_image=ok_img_data, size=(43, 43))
            CTkButton(master=self.user_container, width=100, image=ok_img, text="Close", fg_color="#964B00",font=("Arial Bold", 20), text_color="#fff", hover_color="#2A8C55", anchor="w", command=self.clear_main_page_content).grid(row=5, column=0,padx=(10, 0),columnspan=4,pady=15)
            self.option_showing_status=False

    # end of user details
    # Transport starting
    def transport_setting(self):
        self.clear_main_page_content()
        if not self.option_showing_status:
            self.master_key_showing("transport_setting")
        if self.option_showing_status and self.usertype != "Retailor":
            if not self.setting_call_method():
                CTkMessagebox(title="Info", message="Server running you shouldn't change the receiver, firstly stop it")
            ok_img_data = Image.open("./all_images/ok_logo.png")
            ok_img = CTkImage(light_image=ok_img_data, dark_image=ok_img_data, size=(43, 43))
            cancel_img = CTkImage(light_image=self.cancel_img_data, dark_image=self.cancel_img_data, size=(43, 43))
            if self.transport_header_container == None:
                self.transport_header_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                self.transport_header_container.pack(fill="x", pady=(45, 0), padx=10)
                if self.transport_server_label == None:
                    self.transport_server_label=CTkLabel(master=self.transport_header_container, text="Transport Server Settings",
                         font=("Arial Black", 18),text_color="#2A8C55")
                self.transport_server_label.pack(anchor="center", ipady=10, pady=(0, 0))

            else:
                self.transport_header_container.pack(fill="x", pady=(45, 0), padx=10)
                if self.transport_server_label == None:
                    self.transport_server_label=CTkLabel(master=self.transport_header_container, text="Transport Server Settings",
                            font=("Arial Black", 18),text_color="#2A8C55")
                self.transport_server_label.pack(anchor="center", ipady=10, pady=(0, 0))
            if self.transport_container == None:
                self.transport_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                self.transport_container.pack(fill="x", pady=(10, 0), padx=10)
                if self.transport_name_label == None:
                    self.transport_name_label=CTkLabel(master=self.transport_container, text="Receiver Name", font=("Arial Black", 14),
                            text_color="#2A8C55")
                self.transport_name_label.grid(row=2, column=0, padx=(10, 0), pady=15)
                if self.transport_name == None:
                    self.transport_name = CTkEntry(master=self.transport_container, width=400, height=40,
                                               font=("Black", 14),placeholder_text="Enter Distiller Name", border_color="#2A8C55",border_width=2)
                self.transport_name.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=15)
                if self.transport_id_label == None:
                    self.transport_id_label=CTkLabel(master=self.transport_container, text="Receiver Id", font=("Arial Black", 14),
                                text_color="#2A8C55")
                self.transport_id_label.grid(row=3, column=0, padx=(10, 0), pady=15)
                if self.transport_id == None:
                    self.transport_id = CTkEntry(master=self.transport_container, width=400, height=40, font=("Black", 14),
                                             placeholder_text="Enter Id", border_color="#2A8C55", border_width=2)
                self.transport_id.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=15)
                if self.transport_date_label == None:
                    self.transport_date_label=CTkLabel(master=self.transport_container, text="Transport Date", font=("Arial Black", 14),
                         text_color="#2A8C55")
                self.transport_date_label.grid(row=4, column=0, padx=(10, 0), pady=15)
                if self.transport_date == None:
                    self.transport_date = CTkEntry(master=self.transport_container, width=400, height=40,
                                               font=("Black", 14),
                                               border_color="#2A8C55", border_width=2)
                    self.transport_date.insert(INSERT, str(datetime.datetime.now().date()))
                self.transport_date.grid(row=4, column=1, columnspan=2, padx=(10, 0), pady=15)
            else:
                self.transport_container.pack(fill="x", pady=(10, 0), padx=10)
                if self.transport_name_label == None:
                    self.transport_name_label=CTkLabel(master=self.transport_container, text="Receiver Name", font=("Arial Black", 14),
                            text_color="#2A8C55")
                self.transport_name_label.grid(row=2, column=0, padx=(10, 0), pady=15)
                if self.transport_name == None:
                    self.transport_name = CTkEntry(master=self.transport_container, width=400, height=40,
                                               font=("Black", 14),placeholder_text="Enter Distiller Name", border_color="#2A8C55",border_width=2)
                self.transport_name.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=15)
                if self.transport_id_label == None:
                    self.transport_id_label=CTkLabel(master=self.transport_container, text="Receiver Id", font=("Arial Black", 14),
                                text_color="#2A8C55")
                self.transport_id_label.grid(row=3, column=0, padx=(10, 0), pady=15)
                if self.transport_id == None:
                    self.transport_id = CTkEntry(master=self.transport_container, width=400, height=40, font=("Black", 14),
                                             placeholder_text="Enter Id", border_color="#2A8C55", border_width=2)
                self.transport_id.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=15)
                if self.transport_date_label == None:
                    self.transport_date_label=CTkLabel(master=self.transport_container, text="Transport Date", font=("Arial Black", 14),
                         text_color="#2A8C55")
                self.transport_date_label.grid(row=4, column=0, padx=(10, 0), pady=15)
                if self.transport_date == None:
                    self.transport_date = CTkEntry(master=self.transport_container, width=400, height=40,
                                               font=("Black", 14),
                                               border_color="#2A8C55", border_width=2)
                    self.transport_date.insert(INSERT, str(datetime.datetime.now().date()))
                self.transport_date.grid(row=4, column=1, columnspan=2, padx=(10, 0), pady=15)

            if self.transport_button_container == None:
                self.transport_button_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                self.transport_button_container.pack(fill="x", pady=(5, 0), padx=10)
                if self.transport_button_cancel == None:
                    self.transport_button_cancel=CTkButton(master=self.transport_button_container, width=150, image=cancel_img, text="Cancel",
                        fg_color="#964B00",font=("Arial Bold", 20), text_color="#fff", hover_color="#2A8C55", anchor="CENTER",
                        command=self.clear_main_page_content)
                self.transport_button_cancel.grid(row=5, column=2, padx=(100, 0), pady=15)
                if self.transport_button_ok == None:
                    self.transport_button_ok=CTkButton(master=self.transport_button_container, width=150, image=ok_img, text="Ok",
                          fg_color="#964B00",font=("Arial Bold", 20),text_color="#fff", hover_color="#2A8C55", anchor="CENTER", command=self.server_setting)
                self.transport_button_ok.grid(row=5, column=0, padx=(100, 0), pady=15)
            else:
                self.transport_button_container.pack(fill="x", pady=(5, 0), padx=27)
                if self.transport_button_cancel == None:
                    self.transport_button_cancel = CTkButton(master=self.transport_button_container, width=150,
                                                             image=cancel_img, text="Cancel",
                                                             fg_color="#964B00", font=("Arial Bold", 20),
                                                             text_color="#fff", hover_color="#2A8C55", anchor="CENTER",
                                                             command=self.clear_main_page_content)
                self.transport_button_cancel.grid(row=5, column=2, padx=(100, 0), pady=15)
                if self.transport_button_ok == None:
                    self.transport_button_ok = CTkButton(master=self.transport_button_container, width=150,
                                                         image=ok_img, text="Ok",
                                                         fg_color="#964B00", font=("Arial Bold", 20), text_color="#fff",
                                                         hover_color="#2A8C55", anchor="CENTER",
                                                         command=self.server_setting)
                self.transport_button_ok.grid(row=5, column=0, padx=(100, 0), pady=15)

            self.option_showing_status = False

    # end transport setting
    # Server Setting starting
    def server_setting(self):
        #print(self.brand_name.get(),self.product_qty.get(),self.mfg_date.get(),self.date.get(),self.box_qty_size.get(), self.production_line_no.get())
        if (self.check_candidate_existence() or self.usertype=='Retailor'):
            self.clear_main_page_content()
            if ((not self.option_showing_status) and (not self.configure_called)):
                self.master_key_showing("server_setting")
            if self.option_showing_status or self.configure_called:
                #new added

                if self.receiver_frame == None:
                    self.receiver_frame = CTkFrame(master=self.main_view, fg_color="transparent")
                self.receiver_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
                if self.receiver_showlabel == None:
                    self.receiver_showlabel=CTkLabel(master=self.receiver_frame, text="Receiver Status", font=("Arial Black", 20),
                         text_color="#2A8C55")
                self.receiver_showlabel.pack(anchor="nw", side="left", padx=(0, 50))
                if self.receiver_name_showlabel == None:
                    self.receiver_name_showlabel=CTkLabel(master=self.receiver_frame, text=f"   {self.receiver_name}   ", font=("Arial Black", 15), text_color="#fff",fg_color="#2A8C55", )
                self.receiver_name_showlabel.pack(anchor="ne", side="right", padx=(0, 0))
                if self.receiver_type_showlabel == None:
                    self.receiver_type_showlabel=CTkLabel(master=self.receiver_frame, text=f"   {self.receiver_type}   ", font=("Arial Black", 15), text_color="#fff",fg_color="#2A8C55")
                self.receiver_type_showlabel.pack(anchor="ne", side="right", padx=(0, 30))
                #end new added
                Board.ip_address=self.getIpAddressofSystem()
                start_img_data = Image.open("./all_images/start_logo.png")
                start_img = CTkImage(light_image=start_img_data, dark_image=start_img_data, size=(43, 43))
                stop_img_data = Image.open("./all_images/stop_logo.png")
                stop_img = CTkImage(light_image=stop_img_data, dark_image=stop_img_data, size=(43, 43))
                terminate_img_data = Image.open("./all_images/terminate_logo.png")
                terminate_img = CTkImage(light_image=terminate_img_data, dark_image=terminate_img_data, size=(43, 43))
                if self.server_header_container == None:
                    self.server_header_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                    self.server_header_container.pack(fill="x", pady=(45, 0), padx=10)
                    if self.server_header_label == None:
                        self.server_header_label=CTkLabel(master=self.server_header_container, text="Internal Server Settings", font=("Arial Black", 18),
                             text_color="#2A8C55")
                    self.server_header_label.pack(anchor="center", ipady=10, pady=(0, 0))
                else:
                    self.server_header_container.pack(fill="x", pady=(45, 0), padx=10)
                    if self.server_header_label == None:
                        self.server_header_label=CTkLabel(master=self.server_header_container, text="Internal Server Settings", font=("Arial Black", 18),
                             text_color="#2A8C55")
                    self.server_header_label.pack(anchor="center", ipady=10, pady=(0, 0))
                if self.server_container == None:
                    self.server_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                    self.server_container.pack(fill="x", pady=(10, 0), padx=10)
                    if self.ip_address_label == None:
                        self.ip_address_label=CTkLabel(master=self.server_container, text="IP Address", font=("Arial Black", 14), text_color="#2A8C55")
                    self.ip_address_label.grid(row=2, column=0, padx=(10, 0), pady=15)
                    if self.ip_address_input == None:
                        self.ip_address_input = CTkEntry(master=self.server_container, width=230, height=40, font=("Black", 14),
                                                        border_color="#2A8C55", border_width=2)
                        self.ip_address_input.insert(INSERT, Board.ip_address)
                    self.ip_address_input.grid(row=2, column=1, padx=(10, 0), pady=15)
                    if self.port_label == None:
                        self.port_label=CTkLabel(master=self.server_container, text="Port No.", font=("Arial Black", 14),
                                text_color="#2A8C55")
                    self.port_label.grid(row=3, column=0, padx=(10, 0), pady=15)
                    if self.port_input == None:
                        self.port_input = CTkEntry(master=self.server_container, width=230, height=40, font=("Black", 14),
                                               border_color="#2A8C55", border_width=2)
                        self.port_input.insert(INSERT, "9004")
                    self.port_input.grid(row=3, column=1, padx=(10, 0), pady=15)
                    if self.server_button_start == None:
                        self.server_button_start=CTkButton(master=self.server_container, width=202, image=start_img, bg_color="#fff", text="Start",
                                fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                                anchor="w", command=self.button_starter)
                    self.server_button_start.grid(row=4, column=0, padx=(5, 0), pady=15)
                    if self.server_button_stop == None:
                        self.server_button_stop=CTkButton(master=self.server_container, width=202, image=stop_img, bg_color="#fff", text="Stop",
                                fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                                anchor="w", command=self.button_stop_command)
                    self.server_button_stop.grid(row=4, column=1, padx=(5, 0), pady=15)
                    if self.server_button_terminate == None:
                        self.server_button_terminate=CTkButton(master=self.server_container, width=202, image=terminate_img, bg_color="#fff",
                              text="Terminate",fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                              anchor="w", command=self.button_close_command)
                    self.server_button_terminate.grid(row=4, column=2, padx=(5, 0), pady=15)

                else:
                    self.server_container.pack(fill="x", pady=(10, 0), padx=10)
                    if self.ip_address_label == None:
                        self.ip_address_label=CTkLabel(master=self.server_container, text="IP Address", font=("Arial Black", 14), text_color="#2A8C55")
                    self.ip_address_label.grid(row=2, column=0, padx=(10, 0), pady=15)
                    if self.ip_address_input == None:
                        self.ip_address_input = CTkEntry(master=self.server_container, width=230, height=40, font=("Black", 14),
                                                        border_color="#2A8C55", border_width=2)
                        self.ip_address_input.insert(INSERT, Board.ip_address)
                    self.ip_address_input.grid(row=2, column=1, padx=(10, 0), pady=15)
                    if self.port_label == None:
                        self.port_label=CTkLabel(master=self.server_container, text="Port No.", font=("Arial Black", 14),
                                text_color="#2A8C55")
                    self.port_label.grid(row=3, column=0, padx=(10, 0), pady=15)
                    if self.port_input == None:
                        self.port_input = CTkEntry(master=self.server_container, width=230, height=40, font=("Black", 14),
                                               border_color="#2A8C55", border_width=2)
                        self.port_input.insert(INSERT, "9004")
                    self.port_input.grid(row=3, column=1, padx=(10, 0), pady=15)
                    if self.server_button_start == None:
                        self.server_button_start=CTkButton(master=self.server_container, width=202, image=start_img, bg_color="#fff", text="Start",
                                fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                                anchor="w", command=self.button_starter)
                    self.server_button_start.grid(row=4, column=0, padx=(5, 0), pady=15)
                    if self.server_button_stop == None:
                        self.server_button_stop=CTkButton(master=self.server_container, width=202, image=stop_img, bg_color="#fff", text="Stop",
                                fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                                anchor="w", command=self.button_stop_command)
                    self.server_button_stop.grid(row=4, column=1, padx=(5, 0), pady=15)
                    if self.server_button_terminate == None:
                        self.server_button_terminate=CTkButton(master=self.server_container, width=202, image=terminate_img, bg_color="#fff",
                              text="Terminate",fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                              anchor="w", command=self.button_close_command)
                    self.server_button_terminate.grid(row=4, column=2, padx=(5, 0), pady=15)
                self.option_showing_status = False
                self.configure_called = False
        else:
            CTkMessagebox(message="please enter correct receiver name/receiver id", icon="check", option_1="OK")
    #end server setting
    def master_key_handling(self):
        username = self.login_input[0].get()
        db = self.client.get_database('track_and_trace_datahub')
        collection_temp = db.user_details
        if(self.master_key_input.index("end") != 0):
            if self.master_key_input.get() != "":
                usr_name = collection_temp.find_one({'master_key': self.master_key_input.get()})
                self.master_key_input.delete(0, END)
                if usr_name != None:
                    if usr_name['username'] == username:
                        self.option_showing_status=True
                        if self.function_name=='user_details':
                            self.user_details()
                        elif self.function_name=='transport_setting':
                            self.transport_setting()
                        elif self.function_name=='server_setting':
                            self.server_setting()
                    else:
                        CTkMessagebox(title="Error", message="Invalid Master Key", icon="cancel")
                        print("invalid")
                        self.master_key_showing()
                        self.option_showing_status = False
                else:
                    CTkMessagebox(title="Error", message="Invalid Master Key", icon="cancel")
                    print("invalid master key")
            else:
                CTkMessagebox(title="Error", message="Invalid Master Key", icon="cancel")
                self.option_showing_status = False
        else:
            CTkMessagebox(title="Error", message="Invalid Master Key", icon="cancel")
            print("invalid master key")
    # master key start
    def master_key_showing(self, fun_name=""):
        self.clear_main_page_content()
        self.function_name=fun_name
        if self.master_container == None:
            self.master_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
        self.master_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkLabel(master=self.master_container, text="Master Key", font=("Arial Black", 14), text_color="#2A8C55").grid(row=1,column=0,padx=(10,0),pady=15)
        if self.master_key_input == None:
            self.master_key_input=CTkEntry(master=self.master_container, width=400, placeholder_text="", border_color="#2A8C55", border_width=2,show="*")
        self.master_key_input.grid(row=1, column=1, columnspan=2, padx=(10, 0), pady=15)

        ok_img_data = Image.open("./all_images/ok_logo.png")
        ok_img = CTkImage(light_image=ok_img_data, dark_image=ok_img_data, size=(43, 43))
        if self.master_key_button == None:
            self.master_key_button=CTkButton(master=self.master_container, width=100, image=ok_img, text="Ok", fg_color="#964B00",
                    font=("Arial Bold", 20), text_color="#fff", hover_color="#2A8C55", anchor="w", command=self.master_key_handling)
        self.master_key_button.grid(row=1, column=3,padx=(5, 0),columnspan=4,pady=15)


    # end master key
    #start testing configure called
    def configure_method(self):
        self.clear_main_page_content()
        self.configure_called=True
        self.transport_setting()
    #end testing configure called
    # status starting
    def status_showing(self, fact=""):
        self.clear_main_page_content()
        if self.status_label_container==None:
            self.status_label_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.status_label_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.status_label==None:
                self.status_label=CTkLabel(master=self.status_label_container, text="Status", font=("Arial Black", 20), text_color="#2A8C55")
            self.status_label.pack(pady=(0, 0))
        else:
            self.status_label_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.status_label==None:
                self.status_label=CTkLabel(master=self.status_label_container, text="Status", font=("Arial Black", 20),
                        text_color="#2A8C55")
            self.status_label.pack(pady=(0, 0))
        if self.status_textbox_container==None:
            self.status_textbox_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.status_textbox_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.status_textarea == None:
                self.status_textarea = CTkTextbox(master=self.status_textbox_container, width=650, height=350,
                                                border_width=2, border_color="#2A8C55")
                self.status_textarea.insert(INSERT, "Listening\n")
                self.status_textarea.see("end")
                self.status_textarea.pack(pady=(0, 0))
            else:
                # self.logs_textarea.insert(INSERT, self.logs_textarea.get("1.0", 'end'))
                self.status_textarea.insert("end", fact)
                self.status_textarea.see("end")
                self.status_textarea.pack(pady=(0, 0))
        else:
            self.status_textbox_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.status_textarea == None:
                self.status_textarea = CTkTextbox(master=self.status_textbox_container, width=650, height=350,
                                                border_width=2, border_color="#2A8C55")
                self.status_textarea.insert(INSERT, "Listening\n")
                self.status_textarea.see("end")
                self.status_textarea.pack(pady=(0, 0))
            else:
                # self.logs_textarea.insert(INSERT, self.logs_textarea.get("1.0", 'end'))
                self.status_textarea.insert("end", fact)
                self.status_textarea.see("end")
                self.status_textarea.pack(pady=(0, 0))
        hide_img_data = Image.open("./all_images/hide_logo.png")
        hide_img = CTkImage(light_image=hide_img_data, dark_image=hide_img_data, size=(43, 43))
        if self.status_button_container == None:
            self.status_button_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.status_button_container.pack(fill="x", pady=(5, 0), padx=27)
            if self.status_button==None:
                self.status_button=CTkButton(master=self.status_button_container, width=100, image=hide_img, text="Hide", fg_color="#964B00",
                        font=("Arial Bold", 14), text_color="#fff", hover_color="#2A8C55", anchor="w",command=self.clear_main_page_content)
            self.status_button.pack(pady=(0, 0))
        else:
            self.status_button_container.pack(fill="x", pady=(5, 0), padx=27)
            if self.status_button == None:
                self.status_button.CTkButton(master=self.status_button_container, width=100, image=hide_img, text="Hide", fg_color="#964B00",
                      font=("Arial Bold", 14), text_color="#fff", hover_color="#2A8C55", anchor="w",
                      command=self.clear_main_page_content)
            self.status_button.pack(pady=(0, 0))
    # status ending
    # for logs level setting
    def logs_showing(self, fact=""):
        self.clear_main_page_content()
        if self.logs_label_container==None:
            self.logs_label_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.logs_label_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.logs_label == None:
                self.logs_label=CTkLabel(master=self.logs_label_container, text="Logs", font=("Arial Black", 20),
                     text_color="#2A8C55")
            self.logs_label.pack(pady=(0, 0))
        else:
            self.logs_label_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.logs_label != None:
                self.logs_label=CTkLabel(master=self.logs_label_container, text="Logs", font=("Arial Black", 20),
                        text_color="#2A8C55")
            self.logs_label.pack(pady=(0, 0))
        if self.logs_textbox_container==None:
            self.logs_textbox_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.logs_textbox_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.logs_textarea == None:
                self.logs_textarea = CTkTextbox(master=self.logs_textbox_container, width=650, height=350,
                                                border_width=2, border_color="#2A8C55")
                self.logs_textarea.insert(INSERT, "Listening\n")
                self.logs_textarea.see("end")
                self.logs_textarea.pack(pady=(0, 0))
            else:
                # self.logs_textarea.insert(INSERT, self.logs_textarea.get("1.0", 'end'))
                self.logs_textarea.insert("end", fact)
                self.logs_textarea.see("end")
                self.logs_textarea.pack(pady=(0, 0))
        else:
            self.logs_textbox_container.pack(fill="x", pady=(10, 0), padx=27)
            if self.logs_textarea == None:
                self.logs_textarea = CTkTextbox(master=self.logs_textbox_container, width=650, height=350,
                                                border_width=2, border_color="#2A8C55")
                self.logs_textarea.insert(INSERT, "Listening\n")
                self.logs_textarea.see("end")
                self.logs_textarea.pack(pady=(0, 0))
            else:
                # self.logs_textarea.insert(INSERT, self.logs_textarea.get("1.0", 'end'))
                self.logs_textarea.insert("end", fact)
                self.logs_textarea.see("end")
                self.logs_textarea.pack(pady=(0, 0))
        hide_img_data = Image.open("./all_images/hide_logo.png")
        hide_img = CTkImage(light_image=hide_img_data, dark_image=hide_img_data, size=(43, 43))
        if self.logs_button_container==None:
            self.logs_button_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            self.logs_button_container.pack(fill="x", pady=(5, 0), padx=27)
            if self.logs_button == None:
                self.logs_button=CTkButton(master=self.logs_button_container, width=100, image=hide_img, text="Hide", fg_color="#964B00",
                        font=("Arial Bold", 14), text_color="#fff", hover_color="#2A8C55", anchor="w", command=self.clear_main_page_content)
            self.logs_button.pack(pady=(0, 0))
        else:
            self.logs_button_container.pack(fill="x", pady=(5, 0), padx=27)
            if self.logs_button == None:
                self.logs_button=CTkButton(master=self.logs_button_container, width=100, image=hide_img, text="Hide", fg_color="#964B00",
                        font=("Arial Bold", 14), text_color="#fff", hover_color="#2A8C55", anchor="w",
                        command=self.clear_main_page_content)
            self.logs_button.pack(pady=(0, 0))
    # logs level setting end
    #sidebar starting
    def sidebar_showing(self):
        sidebar_frame = CTkFrame(master=self, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")
        logo_img_data = Image.open("./all_images/logo_old.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")
        package_img_data = Image.open("./all_images/user.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
        CTkButton(master=sidebar_frame, image=package_img, text="User", fg_color="#fff", font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=self.user_details).pack(anchor="center",ipady=10,pady=(36, 0))
        returns_img_data = Image.open("./all_images/transport_logo.png")
        returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
        CTkButton(master=sidebar_frame, image=returns_img, text="Transport", fg_color="#fff", font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=self.transport_setting).pack(anchor="center", ipady=10, pady=(36, 0))
        settings_img_data = Image.open("./all_images/server_logo.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        CTkButton(master=sidebar_frame, image=settings_img, text="Server", fg_color="#fff", font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=self.server_setting).pack(anchor="center",ipady=10,pady=(36, 0))
        CTkLabel(master=sidebar_frame, text="Copyright©2023", text_color="#fff", font=("Arial Black", 10)).pack(anchor="center", pady=(230, 0))
    #end of sidebar

    # main page content starting
    def main_page(self):
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Logged In As", font=("Arial Black", 20), text_color="#2A8C55").pack(
            anchor="nw", side="left")
        CTkButton(master=title_frame, text=str(self.registered_name), font=("Arial Black", 15), text_color="#fff",
                  fg_color="#2A8C55", hover_color="#207244", command=self.user_details).pack(anchor="ne", side="right")
        CTkButton(master=title_frame, text=str(self.usertype), font=("Arial Black", 15), text_color="#fff",
                  fg_color="#2A8C55", hover_color="#207244", command=self.user_details).pack(anchor="ne", side="right", padx=(0,27))
        metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))
        orders_metric = CTkFrame(master=metrics_frame, width=200, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")
        logitics_img_data = Image.open("./all_images/status_logo.png")
        logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))
        CTkButton(master=orders_metric, width=200, image=logistics_img, bg_color="#fff", text="Status",
                  fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00", anchor="w",
                  command=self.status_showing).pack(anchor="center", ipady=10, pady=(0, 0))
        shipped_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        shipped_metric.grid_propagate(0)
        shipped_metric.pack(side="left", expand=True, anchor="center")
        shipping_img_data = Image.open("./all_images/setting_logo.png")
        shipping_img = CTkImage(light_image=shipping_img_data, dark_image=shipping_img_data, size=(43, 43))
        CTkButton(master=shipped_metric, width=200, image=shipping_img, bg_color="#fff", text="Configure",
                  fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00",
                  anchor="w", command=self.configure_method).pack(anchor="center", ipady=10, pady=(0, 0))
        delivered_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        delivered_metric.grid_propagate(0)
        delivered_metric.pack(side="right", )
        delivered_img_data = Image.open("./all_images/logs_logo.png")
        delivered_img = CTkImage(light_image=delivered_img_data, dark_image=delivered_img_data, size=(43, 43))
        CTkButton(master=delivered_metric, width=200, image=delivered_img, bg_color="#fff", text="Logs",
                  fg_color="#2A8C55", font=("Arial Bold", 14), text_color="#fff", hover_color="#964B00", anchor="w",
                  command=self.logs_showing).pack(anchor="center", ipady=10, pady=(0, 0))
    #end of main page content
    def getIpAddressofSystem(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
        s.close()
        return ip
    def logs_listening(self):
        #self.clear_main_page_content()
        if self.logs_textbox_container==None:
            self.logs_textbox_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            if self.logs_textarea==None:
                self.logs_textarea = CTkTextbox(master=self.logs_textbox_container, width=650, height=350, border_width=2,
                                            border_color="#2A8C55")
                self.logs_textarea.insert(INSERT, "Listening\n")
            else:
                self.logs_textarea.delete("1.0", "end")
                self.logs_textarea.insert(INSERT, "Listening\n")
        else:
            if self.logs_textarea==None:
                self.logs_textarea = CTkTextbox(master=self.logs_textbox_container, width=650, height=350, border_width=2,
                                            border_color="#2A8C55")
                self.logs_textarea.insert(INSERT, "Listening\n")
            else:
                self.logs_textarea.delete("1.0", "end")
                self.logs_textarea.insert(INSERT, "Listening\n")

    def status_listening(self):
        #self.clear_main_page_content()
        if self.status_textbox_container==None:
            self.status_textbox_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
            if self.status_textarea==None:
                self.status_textarea = CTkTextbox(master=self.status_textbox_container, width=650, height=350, border_width=2,
                                              border_color="#2A8C55")
                self.status_textarea.insert(INSERT, 'Listening\n')
            else:
                self.status_textarea.delete("1.0", "end")
                self.status_textarea.insert(INSERT, 'Listening\n')
        else:
            if self.status_textarea==None:
                self.status_textarea = CTkTextbox(master=self.status_textbox_container, width=650, height=350, border_width=2,
                                              border_color="#2A8C55")
                self.status_textarea.insert(INSERT, 'Listening\n')
            else:
                self.status_textarea.delete("1.0", "end")
                self.status_textarea.insert(INSERT, 'Listening\n')
        #self.status_textarea.pack(pady=(0, 0))
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
        with open('../invoice.txt', "w+") as f:
            f.writelines(invoice)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        f = open("../invoice.txt", "r")
        for x in f:
            pdf.cell(200, 10, txt=x, ln=1, align='C')
        #pdf.output("invoice.pdf")
        filename=sender_name+'_invoice'
        pdf.output(f"{filename}.pdf")

    def invoice_generation(self):
        db=self.client.get_database('track_and_trace_datahub')
        usr_details=db.user_details
        store_detail=db.store_details
        transport_details=db.transport_details
        product_count=[]
        product_quantity=[]
        sender_data=usr_details.find_one({'uid':self.sender_id})
        receiver_data = usr_details.find_one({'uid': self.receiver_id})
        if sender_data['usertype']=='Distiller' and receiver_data['usertype']=='Distributor':
            print('distiller')
            sender_name=sender_data['registered_name']
            receiver_name=receiver_data['registered_name']
            #print('sender_name',sender_name,'receiver_name',receiver_name)
            total_product=0
            for x in self.box_id_for_invoice:
                print('distiller inside')
                product_temp=store_detail.find_one({'box_id': x})
                product_quantity.append(product_temp['quantity'])
                product_temp_count=len(product_temp['product_qrcode'].split(','))
                product_count.append(product_temp_count)
                total_product+=product_temp_count
            total_box=len(self.box_id_for_invoice)
            #print(self.box_id_for_invoice)
            box_id=[int(x) for x in self.box_id_for_invoice]
            self.generate_invoice(sender_name, receiver_name,box_id, product_count,product_quantity, total_box, total_product)
        elif sender_data['usertype']=='Distributor' and receiver_data['usertype']=='Retailor':
            print('distributor')
            sender_name = sender_data['registered_name']
            receiver_name = receiver_data['registered_name']
            total_product = 0
            print('self.box_id_for_invoice',self.box_id_for_invoice)
            for x in self.box_id_for_invoice:
                print('distributor inside')
                product_temp = transport_details.find_one({'box_id': x})
                if product_temp is not None:
                    print('not none')
                    print("product_temp['to_user'].split(',')[-1]",product_temp['to_user'].split(',')[-1],'self.sender_id',self.receiver_id)
                    if product_temp['to_user'].split(',')[0]==self.sender_id and product_temp['to_user'].split(',')[-1]==self.receiver_id:
                        product_temp_t = store_detail.find_one({'box_id': x})
                        product_quantity.append(product_temp_t['quantity'])
                        product_temp_count = len(product_temp_t['product_qrcode'].split(','))
                        product_count.append(product_temp_count)
                        total_product += product_temp_count
                        total_box = len(self.box_id_for_invoice)
                        print(self.box_id_for_invoice)
                        print(sender_name, receiver_name, product_count, product_quantity, total_box,total_product)
                        box_id = [int(x) for x in self.box_id_for_invoice]
                        self.generate_invoice(sender_name, receiver_name, box_id, product_count, product_quantity, total_box,
                                          total_product)
                    else:
                        CTkMessagebox(title="Error", message="Not Exists", icon="cancel")
                else:
                    CTkMessagebox(title="Error", message="Not Exists", icon="cancel")
    #from here we need to remove the code
    def setting_call_method(self):
        if self.server_running_status:
            return False
        else:
            return True

    # new added method
    def check_for_receiver(self):
        db = self.client.get_database('track_and_trace_datahub')
        records = db.user_details
        if self.transport_name.index("end")!=0 and self.transport_id.index("end")!=0:
            receiver_id = self.transport_id.get()
            condition2 = {"uid": receiver_id}
            record=records.find_one(condition2)
            if record is not None:
                self.receiver_id=record['uid']
                print(record)
            else:
                print("both invalid input")
        elif self.transport_id.index("end")==0 and self.transport_name.index("end")!=0:
            receiver_name = self.transport_name.get()
            condition1 = {'registered_name': receiver_name}
            record=records.find_one(condition1)
            if record is not None:
                self.receiver_id = record['uid']
                print(record)
            else:
                print("name invalid input")
        elif self.transport_name.index("end")==0 and self.transport_id.index("end")!=0:
            receiver_id = self.transport_id.get()
            condition = {"uid": receiver_id}
            record=records.find_one(condition)
            if record is not None:
                self.receiver_id = record['uid']
                print(record)
            else:
                print("id invalid input")
        else:
            print("not valid user")
    def check_existence_of_box_in_transport_details(self, box_id=""):
        db = self.client.get_database('track_and_trace_datahub')
        temp_data=db.transport_details.find_one({'box_id':box_id})
        if temp_data is not None:
            print('exist')
            return True
        else:
            print('not exist')
            return False
    def retailor_is_user_then_perform_operation(self,ids_list=[]):
        db = self.client.get_database('track_and_trace_datahub')
        records=db.store_details
        records_trans=db.transport_details
        usr_record=db.user_details
        retailor_store_records=db.retailor_store_details
        print("product_list:",ids_list)
        for x in ids_list:
            # data=records.find_one({"product_qrcode":x})
            product_data = []
            box_data = []
            for x1 in retailor_store_records.find():
                if (x1['product_qrcode'].strip('\r') == x.strip('\r')):
                    product_data.append(x1['product_qrcode'].strip('\r'))
                    box_data.append(x1['box_id'].strip('\r'))
            product_data = list(set(product_data))
            box_data = list(set(box_data))
            print('product_data', product_data)
            print('box_data', box_data)
            for x in box_data:
                data_temp = records_trans.find_one({"box_id": x.strip('\r')})
                retailor_id = data_temp['to_user'].split(',')[-1]
                print(retailor_id)
                username1 = self.login_input[0].get()
                print(username1)
                print('ok0')
                ret_id = usr_record.find_one({'username': username1})['uid']
                print('ret_id', ret_id)
                print('ok1')
                if (retailor_id == ret_id):
                    update_field = {"$set": {"product_status": "OUT"}}
                    for x1 in product_data:
                        print('here x1 is:',x1)
                        find_product = retailor_store_records.find_one({'product_qrcode': x1})
                        if find_product is not None:
                            if find_product['product_status'] == "IN":
                                print('aj0k1')
                                #print([x for x in retailor_store_records.find()])
                                result=retailor_store_records.update_one({"product_qrcode": str(x1)}, update_field)
                                if result.matched_count>0:
                                    print('updated yes')
                                else:
                                    print('updated no')
                                print("ok retailor updated")
                            else:
                                CTkMessagebox(title="Error", message="already out of stock", icon="cancel")
                    print('ok2')
                else:
                    CTkMessagebox(title="Error", message="not possible", icon="cancel")

    def database_information(self, ids_data=""):
        ids_data=ids_data.split(',')
        list2 = []
        for x in ids_data:
            list1 = []
            list1.append(x)
            if self.transport_name!=None:
                list1.append(self.transport_name.get())
            if self.transport_id!=None:
                list1.append(self.transport_id.get())
            if self.transport_date!=None:
                list1.append(self.transport_date.get())
            if self.registered_name!=None:
                list1.append(self.registered_name.get())
            list2.append(list1)
        return list2
    def change_the_product_status_in_transport_and_update(self,sender_data=[], receiver_data=[],box_id=""):
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
            self.box_id_for_invoice.append(box_id)
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
        # here is the logic for retailor table
        user_records = db.user_details
        user_type = user_records.find_one({'uid': self.receiver_id})['usertype']
        if user_type == 'Retailor':
            retailor_records = db.retailor_store_details
            store_records = db.store_details
            transport_records = db.transport_details
            query = {"box_id": box_id}
            transport_status = transport_records.find_one(query)
            store_status = store_records.find_one(query)
            if transport_status is not None and store_status is not None:
                list_of_all_product_qrcode = store_status['product_qrcode'].split(',')
                for x in list_of_all_product_qrcode:
                    data = {'box_id': box_id, 'product_qrcode': x, 'product_status': 'IN'}
                    retailor_records.insert_one(data)
            else:
                CTkMessagebox(title="Error", message="invalid box number", icon="cancel")
                print('invalid box number')
    def check_for_product_in_store(self,box_ids_list=[]):
        db = self.client.get_database('track_and_trace_datahub')
        user_details=db.user_details
        records = db.store_details
        if len(box_ids_list)!=0:
            for x in box_ids_list:
                query={"box_id":x}
                user = records.find_one(query)
                print(x)
                if user is None:
                    print("false")
                else:
                    print('ok1')
                    sender_data=[] #sender data
                    #user_id=user['uid']
                    records_usr = db.user_details
                    if not self.check_existence_of_box_in_transport_details(x):
                        user_id = user['uid']
                        sender_data.append(user_id)
                        temp_data = records_usr.find_one({'uid': user_id})
                        sender_data.append(temp_data['usertype'])
                        print('ok2')
                    else:
                        user_name = self.login_input[0].get()
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
                        print('else ok')
                    receiver_data=[] #receiver data
                    if self.transport_id!=None and self.transport_id.index("end")!=0:
                        receiver_data.append(self.transport_id.get())
                        temp_data1 = records_usr.find_one({'uid': self.transport_id.get()})
                        receiver_data.append(temp_data1['usertype'])
                        print('ok3')
                    elif self.transport_name!=None and self.transport_name.index("end")!=0:
                        temp_data1 = records_usr.find_one({'registered_name': self.transport_name.get()})
                        receiver_data.append(temp_data1['uid'])
                        receiver_data.append(temp_data1['usertype'])
                        print('ok4')
                    self.change_the_product_status_in_transport_and_update(sender_data, receiver_data,
                                                                      box_id=x)

    #server method
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
            self.logs_showing()
            #SET text in status box
            #self.status_textarea.insert(INSERT,'Server Started')
            while True and not self.server_stop:
                conn, addr = self.server_socket.accept()
                from_client = ''
                while True and not self.server_stop:
                    data = conn.recv(4096)

                    if (not data): break
                    from_client = data.decode('utf8')
                    text=from_client + ' Port ' + str(Board.port) + ' Time: ' + str(datetime.datetime.now())
                    print(text)
                    #here database connection for fetching ids
                    #from_client=from_client.split(',')
                    from_client = from_client.split(' ')
                    test_text=from_client
                    from_client=[x.strip('\r') for x in from_client]
                    from_client = [x.strip('\n') for x in from_client]
                    if ':' in test_text:
                        from_client=list(from_client[2])
                    #print('self.user_type',self.user_type)
                    if self.usertype!="Retailor":
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
                        #self.logs_press()
                        self.logs_showing()
                    time.sleep(0.1)
                    # conn.send("received".encode())
                    # handle_termination()
                conn.close()
            print('server disconnected and shutdown')
            self.status_textarea.insert(INSERT,'server disconnected and shutdown' + '\n')
        except Exception as e:
            print(f'{e}: Connection Terminated')
            #tkinter.messagebox.showinfo("error",'Connection Terminated')
            self.status_textarea.insert( INSERT,'Connection Terminated'+ '\n')
            CTkMessagebox(title="Info", message="Connection Terminated!")
    #to terminate the application
    def button_close_command(self):
        self.server_running_status=False
        self.server_stop = True
        if self.server_socket != None:
            self.server_socket.close()
        self.destroy()
    #to stop the connection
    def button_stop_command(self):
        # generate invoice
        if (len(self.box_quantity)>0 and self.usertype != "Retailor"):
            self.invoice_generation()
        self.box_id_for_invoice.clear()
        # If the STOP button is pressed then terminate the loop
        self.server_running_status=False
        self.server_stop = True
        if self.server_socket != None:
            self.server_socket.close()
    def check_candidate_existence(self):
        flag_to_execute=False
        db = self.client.get_database('track_and_trace_datahub')
        usr_details = db.user_details
        if self.transport_id != None:
            receiver_data = usr_details.find_one({'uid': self.transport_id.get()})
            if receiver_data is not None:
                self.receiver_name=receiver_data['registered_name']
                self.receiver_type=receiver_data['usertype']
                flag_to_execute=True
                return flag_to_execute
        elif self.transport_name != None:
            receiver_data = usr_details.find_one({'registered_name': self.transport_name.get()})
            if receiver_data is not None:
                self.receiver_name = receiver_data['registered_name']
                self.receiver_type = receiver_data['usertype']
                flag_to_execute=True
                return flag_to_execute
        else:
            return flag_to_execute

    def button_starter(self):
        if self.setting_call_method():
            CTkMessagebox(message="Transport Server Started!", icon="check", option_1="OK")
            print("inside if")
            self.server_running_status = True
            Board.ip_address = self.ip_address_input.get()
            Board.port = int(self.port_input.get())
            t = threading.Thread(target=self.server_communication)
            t.start()
        else:
            CTkMessagebox(title="Error", message="Server running firstly stop it", icon="cancel")
            print("server running firstly stop it")
            print("inside else")


if __name__=="__main__":
    board = Board()
    board.mainloop()

