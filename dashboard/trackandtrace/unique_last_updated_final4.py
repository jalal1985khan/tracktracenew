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
import qrcode
import re
class Board(ctk.CTk):
    #server configuration
    ip_address = "0.0.0.0"
    port = 9004
    # Constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Production Server')
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
        #production frame
        self.production_header_container=None
        self.production_container=None
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
        # server elements
        self.ip_address_input = None
        self.port_input = None
        self.server_header_label = None
        self.ip_address_label = None
        self.ip_address_input = None
        self.port_label = None
        self.port_input = None
        self.server_button_start = None
        self.server_button_stop = None
        self.server_button_terminate = None
        #elements of user page
        self.usertype=""
        self.user_id=""
        self.username=""
        self.registered_name=""
        self.email_id=""
        self.contact_no=""
        self.address=""
        #production line elements
        self.brand_name=None
        self.product_qty=None
        self.mfg_date=None
        self.date=None
        self.box_qty_size=None
        self.production_line_no=None
        ########
        self.production_header_container=None
        self.production_header_label=None
        self.brand_name_label=None
        self.production_qty_label=None
        self.production_mfg_date_label=None
        self.date_label=None
        self.production_box_qty_size=None
        self.production_line_no_label=None
        self.production_button_cancel=None
        self.production_button_ok=None
        #server elements
        self.ip_address_input=None
        self.port_input=None
        #status element
        self.status_textarea=None
        self.status_label=None
        self.status_button=None

        #logs element
        self.logs_textarea=None
        self.logs_label = None
        self.logs_button = None

        #other variables
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
        # production frame
        if self.production_header_container != None:
            self.production_header_container.pack_forget()
        if self.production_container != None:
            self.production_container.pack_forget()
        if self.brand_name != None:
            self.brand_name.grid_forget()
        if self.product_qty != None:
            self.product_qty.grid_forget()
        if self.mfg_date != None:
            self.mfg_date.grid_forget()
        if self.date != None:
            self.date.grid_forget()
        if self.box_qty_size != None:
            self.box_qty_size.grid_forget()
        if self.production_line_no != None:
            self.production_line_no.grid_forget()
        if self.production_header_container != None:
            self.production_header_container.grid_forget()
        if self.production_header_label != None:
            self.production_header_label.grid_forget()
        if self.brand_name_label != None:
            self.brand_name_label.grid_forget()
        if self.production_qty_label != None:
            self.production_qty_label.grid_forget()
        if self.production_mfg_date_label != None:
            self.production_mfg_date_label.grid_forget()
        if self.date_label != None:
            self.date_label.grid_forget()
        if self.production_box_qty_size != None:
            self.production_box_qty_size.grid_forget()
        if self.production_line_no_label != None:
            self.production_line_no_label.grid_forget()
        if self.production_button_cancel != None:
            self.production_button_cancel.grid_forget()
        if self.production_button_ok != None:
            self.production_button_ok.grid_forget()
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
    # Production Line starting
    def production_setting(self):
        self.clear_main_page_content()
        if not self.option_showing_status:
            self.master_key_showing("production_setting")
        if self.option_showing_status:
            ok_img_data = Image.open("./all_images/ok_logo.png")
            ok_img = CTkImage(light_image=ok_img_data, dark_image=ok_img_data, size=(43, 43))
            cancel_img = CTkImage(light_image=self.cancel_img_data, dark_image=self.cancel_img_data, size=(43, 43))
            if self.production_header_container == None:
                self.production_header_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                self.production_header_container.pack(fill="x", pady=(45, 0), padx=10)
                if self.production_header_label == None:
                    self.production_header_label=CTkLabel(master=self.production_header_container, text="Production Line Settings",
                                font=("Arial Black", 18), text_color="#2A8C55")
                self.production_header_label.pack(anchor="center", ipady=10, pady=(0, 0))
            else:
                self.production_header_container.pack(fill="x", pady=(45, 0), padx=10)
                if self.production_header_label == None:
                    self.production_header_label=CTkLabel(master=self.production_header_container, text="Production Line Settings",
                                font=("Arial Black", 18), text_color="#2A8C55")
                self.production_header_label.pack(anchor="center", ipady=10, pady=(0, 0))
            if self.production_container == None:
                self.production_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
                self.production_container.pack(fill="x", pady=(10, 0), padx=10)
                if self.brand_name_label == None:
                    self.brand_name_label=CTkLabel(master=self.production_container, text="Brand Name", font=("Arial Black", 14),text_color="#2A8C55")
                self.brand_name_label.grid(row=1, column=0, padx=(5, 0), pady=15)
                if self.brand_name== None:
                    self.brand_name = CTkComboBox(master=self.production_container, width=200,
                                                  values=["Signature", "Bagpiper"], button_color="#2A8C55",
                                                  border_color="#2A8C55", border_width=2, button_hover_color="#207244",
                                                  dropdown_hover_color="#207244", dropdown_fg_color="#2A8C55",
                                                  dropdown_text_color="#fff")
                self.brand_name.grid(row=1, column=1, padx=(10, 0), pady=15)
                if self.production_qty_label == None:
                    self.production_qty_label=CTkLabel(master=self.production_container, text="Prod. Quantity(ml/l)", font=("Arial Black", 14),
                             text_color="#2A8C55")
                self.production_qty_label.grid(row=1, column=2, padx=(5, 0), pady=15)
                if self.product_qty == None:
                    self.product_qty = CTkEntry(master=self.production_container, width=175, font=("Black", 14),
                                            border_color="#2A8C55", border_width=2)
                    self.product_qty.insert(INSERT, "90")
                self.product_qty.grid(row=1, column=3, padx=(5, 0), pady=15)
                if self.production_mfg_date_label == None:
                    self.production_mfg_date_label=CTkLabel(master=self.production_container, text="Mfg. Date", font=("Arial Black", 14),text_color="#2A8C55")
                self.production_mfg_date_label.grid(row=2, column=0, padx=(5, 0), pady=15)
                if self.mfg_date == None:
                    self.mfg_date = CTkEntry(master=self.production_container, width=200, font=("Black", 14),
                                             border_color="#2A8C55", border_width=2)
                    self.mfg_date.insert(INSERT, str(datetime.datetime.now().date()))
                self.mfg_date.grid(row=2, column=1, padx=(5, 0), pady=15)
                if self.date_label == None:
                    self.date_label=CTkLabel(master=self.production_container, text="Date", font=("Arial Black", 14),text_color="#2A8C55")
                self.date_label.grid(row=2, column=2, padx=(5, 0), pady=15)
                if self.date == None:
                    self.date = CTkEntry(master=self.production_container, width=175, font=("Black", 14),
                                         border_color="#2A8C55", border_width=2)
                    self.date.insert(INSERT, str(datetime.datetime.now().date()))
                self.date.grid(row=2, column=3, padx=(5, 0), pady=15)
                if self.production_box_qty_size == None:
                    self.production_box_qty_size=CTkLabel(master=self.production_container, text="Box Qty Size", font=("Arial Black", 14),
                                    text_color="#2A8C55")
                self.production_box_qty_size.grid(row=3, column=0, padx=(5, 0), pady=15)
                if self.box_qty_size == None:
                    self.box_qty_size = CTkEntry(master=self.production_container, width=200, font=("Black", 14),
                                                 border_color="#2A8C55", border_width=2)
                    self.box_qty_size.insert(INSERT, "96")
                self.box_qty_size.grid(row=3, column=1, padx=(5, 0), pady=15)
                if self.production_line_no_label == None:
                    self.production_line_no_label=CTkLabel(master=self.production_container, text="Prod. Line No.", font=("Arial Black", 14),
                                        text_color="#2A8C55")
                self.production_line_no_label.grid(row=3, column=2, padx=(5, 0), pady=15)
                if self.production_line_no == None:
                    self.production_line_no = CTkEntry(master=self.production_container, width=175, font=("Black", 14),
                                                       border_color="#2A8C55", border_width=2)
                    self.production_line_no.insert(INSERT, "1")
                self.production_line_no.grid(row=3, column=3, padx=(5, 0), pady=15)
                if self.production_button_cancel == None:
                    self.production_button_cancel=CTkButton(master=self.production_container, width=150, image=cancel_img, text="Cancel",
                            fg_color="#964B00",font=("Arial Bold", 20), text_color="#fff", hover_color="#2A8C55", anchor="CENTER",
                            command=self.clear_main_page_content)
                self.production_button_cancel.grid(row=5, column=2, columnspan=2, pady=15)
                if self.production_button_ok == None:
                    self.production_button_ok=CTkButton(master=self.production_container, width=150, image=ok_img, text="Ok", fg_color="#964B00",
                                    font=("Arial Bold", 20),text_color="#fff", hover_color="#2A8C55", anchor="CENTER", command=self.server_setting)
                self.production_button_ok.grid(row=5, column=0, columnspan=2, pady=15)

            else:
                self.production_container.pack(fill="x", pady=(10, 0), padx=10)
                if self.brand_name_label == None:
                    self.brand_name_label=CTkLabel(master=self.production_container, text="Brand Name", font=("Arial Black", 14),text_color="#2A8C55")
                self.brand_name_label.grid(row=1, column=0, padx=(5, 0), pady=15)
                if self.brand_name== None:
                    self.brand_name = CTkComboBox(master=self.production_container, width=200,
                                                  values=["Signature", "Bagpiper"], button_color="#2A8C55",
                                                  border_color="#2A8C55", border_width=2, button_hover_color="#207244",
                                                  dropdown_hover_color="#207244", dropdown_fg_color="#2A8C55",
                                                  dropdown_text_color="#fff")
                self.brand_name.grid(row=1, column=1, padx=(10, 0), pady=15)
                if self.production_qty_label == None:
                    self.production_qty_label=CTkLabel(master=self.production_container, text="Prod. Quantity(ml/l)", font=("Arial Black", 14),
                             text_color="#2A8C55")
                self.production_qty_label.grid(row=1, column=2, padx=(5, 0), pady=15)
                if self.product_qty == None:
                    self.product_qty = CTkEntry(master=self.production_container, width=175, font=("Black", 14),
                                            border_color="#2A8C55", border_width=2)
                    self.product_qty.insert(INSERT, "90")
                self.product_qty.grid(row=1, column=3, padx=(5, 0), pady=15)
                if self.production_mfg_date_label == None:
                    self.production_mfg_date_label=CTkLabel(master=self.production_container, text="Mfg. Date", font=("Arial Black", 14),text_color="#2A8C55")
                self.production_mfg_date_label.grid(row=2, column=0, padx=(5, 0), pady=15)
                if self.mfg_date == None:
                    self.mfg_date = CTkEntry(master=self.production_container, width=200, font=("Black", 14),
                                             border_color="#2A8C55", border_width=2)
                    self.mfg_date.insert(INSERT, str(datetime.datetime.now().date()))
                self.mfg_date.grid(row=2, column=1, padx=(5, 0), pady=15)
                if self.date_label == None:
                    self.date_label=CTkLabel(master=self.production_container, text="Date", font=("Arial Black", 14),text_color="#2A8C55")
                self.date_label.grid(row=2, column=2, padx=(5, 0), pady=15)
                if self.date == None:
                    self.date = CTkEntry(master=self.production_container, width=175, font=("Black", 14),
                                         border_color="#2A8C55", border_width=2)
                    self.date.insert(INSERT, str(datetime.datetime.now().date()))
                self.date.grid(row=2, column=3, padx=(5, 0), pady=15)
                if self.production_box_qty_size == None:
                    self.production_box_qty_size=CTkLabel(master=self.production_container, text="Box Qty Size", font=("Arial Black", 14),
                                    text_color="#2A8C55")
                self.production_box_qty_size.grid(row=3, column=0, padx=(5, 0), pady=15)
                if self.box_qty_size == None:
                    self.box_qty_size = CTkEntry(master=self.production_container, width=200, font=("Black", 14),
                                                 border_color="#2A8C55", border_width=2)
                    self.box_qty_size.insert(INSERT, "96")
                self.box_qty_size.grid(row=3, column=1, padx=(5, 0), pady=15)
                if self.production_line_no == None:
                    self.production_line_no=CTkLabel(master=self.production_container, text="Prod. Line No.", font=("Arial Black", 14),
                                        text_color="#2A8C55")
                self.production_line_no.grid(row=3, column=2, padx=(5, 0), pady=15)
                if self.production_line_no == None:
                    self.production_line_no = CTkEntry(master=self.production_container, width=175, font=("Black", 14),
                                                       border_color="#2A8C55", border_width=2)
                    self.production_line_no.insert(INSERT, "1")
                self.production_line_no.grid(row=3, column=3, padx=(5, 0), pady=15)
                if self.production_button_cancel == None:
                    self.production_button_cancel=CTkButton(master=self.production_container, width=150, image=cancel_img, text="Cancel",
                            fg_color="#964B00",font=("Arial Bold", 20), text_color="#fff", hover_color="#2A8C55", anchor="CENTER",
                            command=self.clear_main_page_content)
                self.production_button_cancel.grid(row=5, column=2, columnspan=2, pady=15)
                if self.production_button_ok == None:
                    self.production_button_ok=CTkButton(master=self.production_container, width=150, image=ok_img, text="Ok", fg_color="#964B00",
                                    font=("Arial Bold", 20),text_color="#fff", hover_color="#2A8C55", anchor="CENTER", command=self.server_setting)
                self.production_button_ok.grid(row=5, column=0, columnspan=2, pady=15)
            self.option_showing_status = False

    # end production line setting
    # Server Setting starting
    def server_setting(self):
        #print(self.brand_name.get(),self.product_qty.get(),self.mfg_date.get(),self.date.get(),self.box_qty_size.get(), self.production_line_no.get())
        self.clear_main_page_content()
        if ((not self.option_showing_status) and (not self.configure_called)):
            self.master_key_showing("server_setting")
        if self.option_showing_status or self.configure_called:
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
                        elif self.function_name=='production_setting':
                            self.production_setting()
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
        self.production_setting()
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
        returns_img_data = Image.open("./all_images/production_logo.png")
        returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
        CTkButton(master=sidebar_frame, image=returns_img, text="Production", fg_color="#fff", font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=self.production_setting).pack(anchor="center", ipady=10, pady=(36, 0))
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
    def qrcode_generation(self, box_id=""):
        db = self.client.get_database('track_and_trace_datahub')
        collection_temp = db.user_details
        u_uid = collection_temp.find_one({'username': self.login_input[0].get()})['uid']
        uid='QML'+'0'*(4-len(str(self.product_qty.get())))+str(self.product_qty.get())+'KRNDST'+u_uid
        qr = qrcode.QRCode(version=1,
                           box_size=10,
                           border=5)
        qr.add_data(f"Box Id: {box_id} ")
        qr.add_data(f"UID: {uid}")
        qr.make(fit=True)
        img = qr.make_image(fill_color='black',
                            back_color='white')
        img = img.resize((100, 100))
        img.save("./all_images/temp.jpg")
    def setting_call_method(self):
        if self.server_running_status:
            return False
        else:
            return True

    # new added method
    def printingbyprinter(self):
        os.startfile("temp.jpg", "print")
    def check_for_product_existed(self,product_id=""):
        db = self.client.get_database('track_and_trace_datahub')
        collection = db.store_details
        data = collection.find({}, {'product_qrcode': 1, '_id': 0})
        for x in data:
            if product_id in x['product_qrcode'].split(','):
                return False
        return True
    def insert_data_in_products_data(self, data_set=[]):
        print('data_set',data_set)
        print("in insert data")
        db = self.client.get_database('track_and_trace_datahub')
        collection=db.store_details
        collection_temp=db.user_details
        uid=collection_temp.find_one({'username':self.login_input[0].get()})['uid']
        id_list=[0]
        #only for data generation
        if self.box_id!=None:
            box_id=self.box_id
            print('ok0')
        else:
            if len(list(collection.find()))==0:
                box_id=1
            else:
                box_id=max([int(x['box_id']) for x in collection.find()])+1
        for x in collection.find():
            id_list.append(x['id'])
        #counter=0
        flag_for_check_status_of_proper_box=True
        if len(data_set)>0:
            for data in data_set[0].split(','):
                if not self.check_for_product_existed(data):
                    flag_for_check_status_of_proper_box=False
                    CTkMessagebox(title="Error", message=f"{data} : Invalid product id/already used", icon="cancel")
                    print("invalid")
            if ((flag_for_check_status_of_proper_box) and (len(data_set)))>0:
                date_data = datetime.datetime.now()
                print('in second time insert')
                data={"id":max(id_list)+1,"uid":uid,"box_id":str(box_id),"product_qrcode":data_set[0],"product_status":"in","brand":data_set[1],"quantity":int(data_set[2]),
                      "mfg_date":str(data_set[3]),"time_stemp":str(date_data.time()),"date":str(date_data.date()),"production_line":data_set[4],"system_id":self.hostname}
                print('data:',data)
                collection.insert_one(data)
                self.qrcode_generation(str(box_id))
                #self.printingbyprinter()
        print('ok3  completed')
    def database_information(self, ids_data=""):
        print("in database information")
        ids_data=ids_data.split(',')
        ids_data=[str(x).strip('\r') for x in ids_data]

        list1 = []
        db = self.client.get_database('track_and_trace_datahub')
        collection = db.store_details
        box_temp_id=[]
        product_temp_id=[]
        for x in collection.find():
            box_temp_id.append(x['box_id'])
            product_temp_id+=x['product_qrcode'].split(',')

        final_ids_data=[]

        for x in ids_data:
            if x not in product_temp_id:
                final_ids_data.append(x)
            else:
                print(x,'already exist')
                CTkMessagebox(title="Error", message=f"{x}:Invalid product id/already used", icon="cancel")
                print("invalid")
        if self.box_id!=None:
            if self.box_id in box_temp_id:
                CTkMessagebox(title="Error", message="Invalid Box id/already used", icon="cancel")
                self.box_id=None
                print("invalid")

        final_ids_data = list(set(self.box_quantity_temp + final_ids_data))
        if (len(self.box_quantity_temp)>0 and len(final_ids_data)>int(self.box_qty_size.get())) or (len(self.box_quantity_temp)==0 and len(final_ids_data)>int(self.box_qty_size.get())):
            self.box_quantity_temp=final_ids_data[int(self.box_qty_size.get()):]
            self.box_quantity=final_ids_data[:int(self.box_qty_size.get())]
            final_ids_data.clear()
        elif len(final_ids_data) == int(self.box_qty_size.get()):
            self.box_quantity = final_ids_data
        else:
            self.box_quantity_temp = final_ids_data
        if (len(ids_data)==int(self.box_qty_size.get()) and len(ids_data)>0):
            list1.append(','.join(self.box_quantity))
            if self.brand_name!=None:
                list1.append(self.brand_name.get())
            if self.product_qty!=None:
                list1.append(self.product_qty.get())
            if self.mfg_date!=None:
                list1.append(self.mfg_date.get())
            if self.production_line_no!=None:
                list1.append(self.production_line_no.get())
        return list1
    #server method
    def server_communication(self):
        print(Board.ip_address,Board.port)
        self.logs_listening()
        self.status_listening()
        try:
            self.server_stop = False
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((Board.ip_address, Board.port))
            self.server_socket.listen(5)
            print('Server Started')
            print('server listening from ...', datetime.datetime.now())
            self.status_textarea.insert(INSERT,'Server Started\n')
            self.status_textarea.insert(INSERT, f'IP Address: {Board.ip_address}\n')
            self.status_textarea.insert(INSERT, f'Port: {Board.port}\n')
            self.status_textarea.insert(INSERT, f'server listening from ... {datetime.datetime.now()}\n')
            self.logs_showing()

            counter = 0
            product_stock = []
            while True and not self.server_stop:
                conn, addr = self.server_socket.accept()
                from_client = ''
                while True and not self.server_stop:
                    data = conn.recv(4096)
                    #self.server_running_status=True
                    if (not data): break
                    from_client = data.decode('utf8')
                    from_client=from_client.strip('\r')
                    if (len(from_client) == 8 and self.box_id==None and (len(self.box_quantity)==int(self.box_qty_size.get()) or len(self.box_quantity)==0)):
                        self.box_id=from_client.strip('\r')
                        counter=0
                    elif '/' in from_client:
                        self.box_id = from_client.split('/')[-2]
                        counter = 0
                    elif '|' in from_client:
                        self.box_id = from_client.split('|')[-2]
                        counter = 0

                    else:
                        if (('ERROR' not in from_client) and (len(from_client) != 8) and self.box_id!=from_client):
                            product_stock+=[x.strip('\r') for x in list(from_client.split('\r')) if len(x)>0]
                            product_stock=list(set(product_stock+self.box_quantity))
                    print("product_initial_list",product_stock)
                    print("box_quantity", self.box_quantity)
                    print("in server")
                    #text=from_client + ' Port ' + str(Board.port) + ' Time: ' + str(datetime.datetime.now())
                    print(from_client)

                    #text box handling
                    if self.logs_textarea.get("1.0", END).count('\n') > 50:
                        self.logs_textarea.delete("1.0", "end")
                        self.logs_textarea.insert(INSERT, 'Listening\n')
                    if self.logs_textarea!=None:
                        self.logs_textarea.insert(INSERT,from_client+'\n')
                    else:
                        #self.logs_press()
                        self.logs_textarea.insert(INSERT, from_client+'\n')
                        self.logs_showing()
                    final_product_stock=[]
                    for x in product_stock:
                        if self.check_for_product_existed(x):
                            final_product_stock.append(x)
                        #else:
                        #    tkinter.messagebox.showerror('Error', 'Product/Box already existed!')
                    product_stock=final_product_stock
                    counter = len(product_stock)
                    print('counter', counter, 'product_stock', product_stock)
                    if self.box_qty_size!=None:
                        print('server ok1')
                        if counter==int(self.box_qty_size.get()):
                            product_stock=product_stock[::-1]
                            print('server ok2')
                            self.insert_data_in_products_data(self.database_information(','.join(product_stock)))
                            print('server ok3')
                            if (len(self.box_quantity)==int(self.box_qty_size.get())):
                                print("completed")
                                counter=0
                                self.box_id=None
                                self.box_quantity.clear()
                                product_stock=[]
                                print('server ok4')
                        elif counter>int(self.box_qty_size.get()):
                            counter_temp=counter
                            while(counter_temp>int(self.box_qty_size.get())):
                                print('server ok2')
                                self.insert_data_in_products_data(self.database_information(','.join(product_stock[0:int(self.box_quantity_size_input.get())])))
                                product_stock = product_stock[int(self.box_qty_size.get()):]
                                print('server ok3')
                                counter_temp=len(product_stock)
                                print('ajay box size is now:',len(self.box_quantity))

                                if (len(self.box_quantity) == int(self.box_qty_size.get())):
                                    print("completed")
                                    counter = 0
                                    self.box_id = None
                                    self.box_quantity.clear()
                                    #product_stock = []
                                    print('server ok4')
                    # end database connection for fetching ids
                    time.sleep(0.1)
                conn.close()
            print('server disconnected and shutdown')
            self.status_textarea.insert(INSERT,'server disconnected and shutdown' + '\n')
        except Exception as e:
            self.server_running_status=False
            print(e)
            error_text=str(e)
            if 'Only one usage of each socket address (protocol/network address/port) is normally permitted' in error_text:
                CTkMessagebox(title="Error", message="Another server running on same ip/port", icon="cancel")
            else:
                CTkMessagebox(title="Info", message="Connection Terminated!")
            print(f'{e}: Connection Terminated')
            self.status_textarea.insert( INSERT,'Connection Terminated'+ '\n')
    #to terminate the application
    def button_close_command(self):
        self.server_running_status=False
        self.destroy()
    #to stop the connection
    def button_stop_command(self):
        # If the STOP button is pressed then terminate the loop
        self.server_running_status=False
        self.server_stop = True
        if self.server_socket != None:
            self.server_socket.close()
        CTkMessagebox(title="Info", message="Server Terminated Successfully")
    def button_starter(self):
        if self.setting_call_method():
            CTkMessagebox(message="Production Server Started!",icon="check", option_1="OK")
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

