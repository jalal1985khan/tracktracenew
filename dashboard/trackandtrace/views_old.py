from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from trackandtrace.models import *
from trackandtrace.forms import *
import pymongo
import subprocess

# Create your views here.

def loginPage(request):        
            if request.method =='POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username,password=password)
                if user is not None:
                        login(request,user)
                        return redirect('/dashboard/')
                else:
                    messages.info(request,'username or password incorrect')
            context = {}
            return render(request,"login.html", context)

def dashboard(request):
       username = request.user
       groups = username.groups.all()  # Get the groups associated with the user
       context ={
              'username':username,
              'groups':groups
       }
       return render(request,"dashboard.html", context) 

def run_server(request):
    subprocess.Popen(['python', 'trackandtrace/unique_last_updated_final4.py'])
    return redirect('/production/')

def run_transportation(request):
    subprocess.Popen(['python', 'trackandtrace/unique_last_updated_for_database_with_retailor4.py'])
    return redirect('/production/')


def viewRegistration(request):
       username = request.user
       groups = username.groups.all()  # Get the groups associated with the user
       all_users = User.objects.all()  # Get the groups associated with the user
       context ={
              'username':username,
              'groups':groups,
              'all_users':all_users
       }
       return render(request,"view_registration.html", context) 


def newRegistration(request):
       userform = CreateUserForm()
       username = request.user
       form = CreateProfileForm()
       groups = username.groups.all()  # Get the groups associated with the user
       if request.method =='POST':      
            form = CreateUserForm(request.POST)
            #Profile = CreateProfileForm( instance = user )
            if form.is_valid():
                user = form.save()
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                phone = request.POST['phone']
                email = request.POST['email']
                address = request.POST['address']
                registration_number = request.POST['registration_number']
                registered_name = request.POST['registered_name']
                username = form.cleaned_data.get('username')
                password = request.POST['password']
                status = request.POST['status']
                usertype = request.POST['usertype']
                master_key = request.POST['master_key']
                group_t = Group.objects.get(name=usertype)
                user.groups.add(group_t)
                Profile.objects.create(user=user,first_name=first_name,last_name=last_name,phone=phone,email=email,address=address,registration_number=registration_number,registered_name=registered_name,usertype=usertype,username=username,password=password,status=status,master_key=master_key)
                messages.success(request,'User created successfully ' + username) 
       group_type = Group.objects.all()
       context ={
              'username':username,
              'form':form,
              'userform':userform,
              'groups':groups,
              'group_type':group_type
       }
       return render(request,"new_registration.html", context) 

def Production(request):
       username = request.user
       groups = username.groups.all()  # Get the groups associated with the user

       # mango connection starts from here  
       #username='dewars'
       #password='123'
       profile = Profile.objects.get(user=username)
       uid = str(profile.uuid)
       profile = Profile.objects.get(user=username)
       password = str(profile.password)
       client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
       db=client.get_database('track_and_trace_datahub')
       records=db.store_details
       str_uid=uid
       line_1=[]
       for x in records.find({'uid':uid}):
           if x['production_line']=='line-1':
               line_1.append(x)
       context ={
              'username':username,
              'groups':groups,
              'lin_1':line_1,
       }
       
       return render(request,'production.html', context)

def InStock(request):
       username = request.user

       #usertype=request.usertype
       profile = Profile.objects.get(user=username)
       uid = str(profile.uuid)
       usertype = str(profile.usertype)
       groups = username.groups.all()  # Get the groups associated with the user
       print('uid',uid)
       # mango connection starts from here 
       client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
       db=client.get_database('track_and_trace_datahub')
       user_records=db.user_details
       transport_records=db.transport_details
       store_records=db.store_details
       db=client.get_database('track_and_trace_datahub')
       if usertype=='Distiller':
           box_id_in=[]
           box_id_out=[]
           box_in_data=[]
           box_out_data=[]
           box_id=[]
           product_id=[]
           dstr_id= uid
           #mango connection end here
           print('username',username)
           for  x in transport_records.find():
                datas=x['from_user'].split(',')[0]
                if datas==dstr_id:
                    box_id_out.append(x['box_id'])
           #receiver_id=x['to_user'].split(',')[0]
           for  x in store_records.find({'uid':dstr_id}):
                if (x['box_id'] not in box_id_out and x['box_id'] not in box_id_in):
                    box_id_in.append(x['box_id'])
           print(box_id_out,box_id_in)
           #receiver_name=user_records.find_one({'uid':receiver_id})['registered_name']

           for x in box_id_in:
                for x1 in store_records.find({'box_id':x}):
                    box_in_data.append(x1)
           for x in box_id_out:
                for x1 in store_records.find({'box_id':x}):
                    box_out_data.append(x1)

           for  x in store_records.find({'uid':dstr_id}):
                    box_id.append(x['box_id'])
           box_id=list(set(box_id))
           for x in box_id:
                for x1 in store_records.find({'box_id':x}):
                    product_id.append(x1['product_qrcode'])
           product_id=list(set(product_id))
           print('box_id',box_id,'product_id',product_id)
           #print('receiver_name',receiver_name)
           context ={
                  'username':username,
                  'groups':groups,
                  'data_in' : box_in_data,
                  'data_out':box_out_data,
                  #'total_product':len(set(product_id)),
                  #'total_box':len(set(box_id)),
                  'status':'In',
                  'uid':uid
           }
       elif usertype=='Distributor':
           box_id_in = []
           box_id_out = []
           box_in_data = []
           box_out_data = []
           # product_id=[]
           dstr_id = 'dist002'
           for x in transport_records.find():
               data = x['from_user'].split(',')[-1]
               if data == dstr_id:
                   box_id_out.append(x['box_id'])
           box_id_out = list(set(box_id_out))
           for x in transport_records.find():
               data = x['to_user'].split(',')[0]
               if (data == dstr_id and x['box_id'] not in box_id_out):
                   box_id_in.append(x['box_id'])
           #receiver_id=x['to_user'].split(',')[-1]
           #receiver_name = user_records.find_one({'uid': receiver_id})['registered_name']
           #print('receiver_id',receiver_id,'receiver_name',receiver_name)
           box_id_in = list(set(box_id_in))
           print(box_id_in, box_id_out)
           for x in box_id_in:
               for x1 in store_records.find({'box_id': x}):
                   box_in_data.append(x1)
           print('box_in_data:', box_in_data)
           for x in box_id_out:
               for x1 in store_records.find({'box_id': x}):
                   box_out_data.append(x1)
           print('box_out_data', box_out_data)
           #instock box
           #total_box=len(set(box_id_in))
           #total_product=len(set(box_in_data))
           context = {
               'username': username,
               'groups': groups,
               'data_in': box_in_data,
               'data_out': box_out_data,
               #'total_product':total_product ,
               #'total_box': total_box,
               'status': 'In',
               'uid': uid
           }
       elif usertype=='Retailor':
           retailor_id = uid
           box_id_in = []
           product_in = []
           product_out = []
           product_in_item = []
           product_out_item = []
           for x in transport_records.find():
               if x['to_user'].split(',')[-1] == retailor_id:
                   box_id_in.append(x['box_id'])
           print(box_id_in)
           total_product=0
           for x in box_id_in:
               for x1 in store_records.find({'box_id': x}):
                   total_product+=1
                   if x1['product_status'] == 'out':
                       product_out.append(x1['product_qrcode'])
                       product_out_item.append(x1)
                   else:
                       product_in.append(x1['product_qrcode'])
                       product_in_item.append(x1)
           print('product_out', len(set(product_out)), 'product_in', len(set(product_in)))
           print(product_in_item)
           total_box=len(box_id_in)

           context = {
               'username': username,
               'groups': groups,
               'data_in': product_in_item,
               'data_out': product_out_item,
               #'total_product': total_product,
               #'total_box': total_box,
               'status': 'In',
               'uid': uid
           }
       return render(request,'in_stock.html',context)

def OutStock(request):
    username = request.user

    # usertype=request.usertype
    profile = Profile.objects.get(user=username)
    uid = str(profile.uuid)
    usertype = str(profile.usertype)
    groups = username.groups.all()  # Get the groups associated with the user
    print('uid', uid)
    # mango connection starts from here
    client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
    db = client.get_database('track_and_trace_datahub')
    user_records = db.user_details
    transport_records = db.transport_details
    store_records = db.store_details
    db = client.get_database('track_and_trace_datahub')
    if usertype == 'Distiller':
        box_id_in = []
        box_id_out = []
        box_in_data = []
        box_out_data = []
        box_id = []
        product_id = []
        dstr_id = uid
        # mango connection end here
        print('username', username)
        if len(list(transport_records.find()))>0:
            for x in transport_records.find():
                datas = x['from_user'].split(',')[0]
                if datas == dstr_id:
                    box_id_out.append(x['box_id'])
            receiver_id = x['to_user'].split(',')[0]
            for x in store_records.find({'uid': dstr_id}):
                if (x['box_id'] not in box_id_out and x['box_id'] not in box_id_in):
                    box_id_in.append(x['box_id'])
            print(box_id_out, box_id_in)
            receiver_name = user_records.find_one({'uid': receiver_id})['registered_name']

            for x in box_id_in:
                for x1 in store_records.find({'box_id': x}):
                    box_in_data.append(x1)
            for x in box_id_out:
                for x1 in store_records.find({'box_id': x}):
                    box_out_data.append(x1)

            for x in store_records.find({'uid': dstr_id}):
                box_id.append(x['box_id'])
            box_id = list(set(box_id))
            for x in box_id:
                for x1 in store_records.find({'box_id': x}):
                    product_id.append(x1['product_qrcode'])
            product_id = list(set(product_id))
            print('box_id', box_id, 'product_id', product_id)
            print('receiver_name', receiver_name)
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                #'total_product': len(set(product_id)),
                #'total_box': len(set(box_id)),
                'receiver_name': receiver_name,
                'status': 'Out',
                'uid': uid
            }
        else:
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                # 'total_product': total_product,
                # 'total_box': total_box,
                'receiver_name': "",
                'status': 'Out',
                'uid': uid
            }
    elif usertype == 'Distributor':
        box_id_in = []
        box_id_out = []
        box_in_data = []
        box_out_data = []
        # product_id=[]
        dstr_id = uid
        if len(list(transport_records.find()))>0:
            for x in transport_records.find():
                data = x['from_user'].split(',')[-1]
                if data == dstr_id:
                    box_id_out.append(x['box_id'])
            box_id_out = list(set(box_id_out))
            for x in transport_records.find():
                data = x['to_user'].split(',')[0]
                if (data == dstr_id and x['box_id'] not in box_id_out):
                    box_id_in.append(x['box_id'])
            receiver_id = x['to_user'].split(',')[-1]
            receiver_name = user_records.find_one({'uid': receiver_id})['registered_name']
            box_id_in = list(set(box_id_in))
            print(box_id_in, box_id_out)
            for x in box_id_in:
                for x1 in store_records.find({'box_id': x}):
                    box_in_data.append(x1)
            print('box_in_data:', box_in_data)
            for x in box_id_out:
                for x1 in store_records.find({'box_id': x}):
                    box_out_data.append(x1)
            print('box_out_data', box_out_data)
            # instock box
            #total_box = len(set(box_id_in))
            #total_product = len(set(box_in_data))
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                #'total_product': total_product,
                #'total_box': total_box,
                'receiver_name': receiver_name,
                'status': 'Out',
                'uid': uid
            }
        else:
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                # 'total_product': total_product,
                # 'total_box': total_box,
                'receiver_name': "",
                'status': 'Out',
                'uid': uid
            }
    elif usertype == 'Retailor':
        retailor_id = uid
        box_id_in = []
        product_in = []
        product_out = []
        product_in_item = []
        product_out_item = []
        if len(list(transport_records.find()))>0:
            for x in transport_records.find():
                if x['to_user'].split(',')[-1] == retailor_id:
                    box_id_in.append(x['box_id'])
            print(box_id_in)
            total_product = 0
            for x in box_id_in:
                for x1 in store_records.find({'box_id': x}):
                    total_product += 1
                    if x1['product_status'] == 'out':
                        product_out.append(x1['product_qrcode'])
                        product_out_item.append(x1)
                    else:
                        product_in.append(x1['product_qrcode'])
                        product_in_item.append(x1)
            print('product_out', len(set(product_out)), 'product_in', len(set(product_in)))
            print(product_in_item)
            #total_box = len(box_id_in)

            context = {
                'username': username,
                'groups': groups,
                'data_in': product_in_item,
                'data_out': product_out_item,
                #'total_product': total_product,
                #'total_box': total_box,
                'receiver_name': "",
                'status': 'Out',
                'uid': uid
            }
        else:
            context = {
                'username': username,
                'groups': groups,
                'data_in': product_in_item,
                'data_out': product_out_item,
                # 'total_product': total_product,
                # 'total_box': total_box,
                'receiver_name': "",
                'status': 'Out',
                'uid': uid
            }
    return render(request,'out_stock.html',context)



def logoutUser(request):
    logout(request)
    return redirect('/')