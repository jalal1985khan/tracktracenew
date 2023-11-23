from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from trackandtrace.models import *
from trackandtrace.forms import *
import pymongo
import subprocess
import datetime


# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.info(request, 'username or password incorrect')
    context = {}
    return render(request, "login.html", context)


def dashboard(request):
    username = request.user
    uid = request.user.profile.uuid
    groups = username.groups.all()  # Get the groups associated with the user
    client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
    db=client.get_database('track_and_trace_datahub')
    store_records=db.store_details
    transport_records=db.transport_details
    user_records=db.user_details
    retailor_stock_records=db.retailor_store_details
    user_object=user_records.find_one({'uid':uid})
    box_id_in=[]
    box_id_out=[]
    total_stock=[]
    total_product_in=[]
    total_product_out=[]
    if user_object is not None:
        if user_object['usertype']=='Distiller':
            total_stock=list(store_records.find({"uid":uid},{'box_id':1,'_id':0}))
        elif user_object['usertype']=='Distributor':
            if len(list(transport_records.find())) > 0:
                    for x in transport_records.find():
                        data = x['from_user'].split(',')[-1]
                        if data == uid:
                            box_id_out.append(x['box_id'])
                    box_id_out = list(set(box_id_out))
                    for x in transport_records.find():
                        data = x['to_user'].split(',')[0]
                        if (data == uid and x['box_id'] not in box_id_out and x['box_id'] not in box_id_in):
                            box_id_in.append(x['box_id'])
                    box_id_in = list(set(box_id_in))
        elif user_object['usertype']=='Retailor':
            for x in transport_records.find():
                if x['to_user'].split(',')[-1] ==uid:
                    box_id_in.append(x['box_id'])
            print('box_id_in',box_id_in)
            for x in box_id_in:
                print("current box",x)
                ret_temp=retailor_stock_records.find_one({'box_id':x})
                if ret_temp is not None:
                    #print('hello')
                    for x1 in retailor_stock_records.find({'box_id':x},{'_id':0}):
                        
                        if x1['product_status'] == 'OUT':
                            total_product_out.append(x1['product_qrcode'])
                        else:
                            total_product_in.append(x1['product_qrcode'])
                print('total_product_in',total_product_in,'total_product_out',total_product_out)

    line_1=len(list(store_records.find({"$and":[{"uid":uid},{'production_line':'1'}]},{'box_id':1,'_id':0})))
    line_2=len(list(store_records.find({"$and":[{"uid":uid},{'production_line':'2'}]},{'box_id':1,'_id':0})))
    total_opening_balance=0
    total_outstock_balance=0
    total_production=0
    if user_object is not None:
        if user_object['usertype']=='Distiller':
            for x in total_stock:
                t1=transport_records.find_one({'box_id':x['box_id']})
                if t1 is None:
                    total_opening_balance+=1
                else:
                    total_outstock_balance+=1
            total_production =len(total_stock) # total product
        elif user_object['usertype']=='Distributor':
            total_opening_balance=len(list(set(box_id_in)))
            total_outstock_balance=len(list(set(box_id_out)))
            total_production=total_opening_balance+total_outstock_balance
        elif user_object['usertype']=='Retailor':
            total_opening_balance=len(list(set(total_product_in)))
            total_outstock_balance=len(list(set(total_product_out)))
            total_production=total_opening_balance+total_outstock_balance
            print('total_opening_balance',total_opening_balance,'total_outstock_balance',total_outstock_balance)
    #print(total_opening_balance) #total opening balance
    #total_production =len(total_stock) # total product
    in_stock_pie=total_opening_balance
    out_stock_pie=total_outstock_balance
    
    distiller_list=[]
    retailor_list=[]
    distiller_name=[]
    retailor_name=[]
    distiller_location=[]
    retailor_location=[]
    unique_distiller=[]
    unique_retailor=[]
    total_box_dist=[]
    total_box_ret=[]
    #new date
    #end date

    if len(list(transport_records.find())):
        for x in transport_records.find():
            if x['to_user'].split(',')[0]==uid:
                distiller_list.append(x['from_user'].split(',')[0])
                if x['to_user'].split(',')[-1]!=uid:
                    retailor_list.append(x['to_user'].split(',')[-1])
        #print(distiller_list,retailor_list)
        unique_distiller=list(set(distiller_list))
        unique_retailor=list(set(retailor_list))
        for x in unique_distiller:
            total_box_dist.append(distiller_list.count(x))
            data_temp=user_records.find_one({'uid':x})
            if data_temp is not None:
                distiller_name.append(data_temp['registered_name'])
                distiller_location.append(data_temp['Address'])
        for x in unique_retailor:
            total_box_ret.append(retailor_list.count(x))
            data_temp = user_records.find_one({'uid': x})
            if data_temp is not None:
                retailor_name.append(data_temp['registered_name'])
                retailor_location.append(data_temp['Address'])

    a= zip(total_box_dist,distiller_name,distiller_location)
    b=zip(total_box_ret,retailor_name,retailor_location)


    context = {
        'username': username,
        'groups': groups,
        'total_production':total_production,
        'total_closing_balance':total_opening_balance,
        'in_stock_pie':in_stock_pie,
        'out_stock_pie':out_stock_pie,
        'line_1':line_1,
        'line_2':line_2,
        'total_box':total_box_dist,
        'distiller':a,
        'retailor':b,
        'retailor_location':retailor_location,
        'date': datetime.datetime.now().date()
    }
    return render(request, "dashboard.html", context)


def run_server(request):
    subprocess.Popen(['python3', 'trackandtrace/unique_last_updated_final4.py'])
    return redirect('/production/')


def run_transportation(request):
    subprocess.Popen(['python3', 'trackandtrace/unique_last_updated_for_database_with_retailor4.py'])
    return redirect('/production/')


def viewRegistration(request):
    username = request.user
    groups = username.groups.all()  # Get the groups associated with the user
    all_users = User.objects.all()  # Get the groups associated with the user
    context = {
        'username': username,
        'groups': groups,
        'all_users': all_users
    }
    return render(request, "view_registration.html", context)


def newRegistration(request):
    userform = CreateUserForm()
    username = request.user
    form = CreateProfileForm()
    groups = username.groups.all()  # Get the groups associated with the user
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # Profile = CreateProfileForm( instance = user )
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
            Profile.objects.create(user=user, first_name=first_name, last_name=last_name, phone=phone, email=email,
                                   address=address, registration_number=registration_number,
                                   registered_name=registered_name, usertype=usertype, username=username,
                                   password=password, status=status, master_key=master_key)
            messages.success(request, 'User created successfully ' + username)
    group_type = Group.objects.all()
    context = {
        'username': username,
        'form': form,
        'userform': userform,
        'groups': groups,
        'group_type': group_type
    }
    return render(request, "new_registration.html", context)


def Production(request):
    username = request.user
    groups = username.groups.all()  # Get the groups associated with the user

    # mango connection starts from here
    # username='dewars'
    # password='123'
    profile = Profile.objects.get(user=username)
    uid = str(profile.uuid)
    profile = Profile.objects.get(user=username)
    password = str(profile.password)
    client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
    db = client.get_database('track_and_trace_datahub')
    records = db.store_details
    transport_records = db.transport_details
    
    str_uid = uid
    line_1 = []
    line_2 = []
    date=datetime.datetime.now().date()
    for x in records.find({'uid': uid}):
        if x['production_line'] == '1':
            line_1.append(x)
        if x['production_line'] == '2':
            line_2.append(x)
    total_box_in = len(line_1)

    box_id_out=[]
    box_id_in=[]
    if len(list(transport_records.find())) > 0:
        for x in transport_records.find():
            datas = x['from_user'].split(',')[0]
            if datas == uid:
                box_id_out.append(x['box_id'])
       
    for x in records.find({'uid': uid}):
        if (x['box_id'] not in box_id_out and x['box_id'] not in box_id_in):
            box_id_in.append(x['box_id'])
    
    total_stock_out=len(box_id_out)    
    total_stock_in=len(box_id_in)
    context = {
        'username': username,
        'groups': groups,
        'date' : date,
        'total_box_in':total_box_in,
        'total_stock_in':total_stock_in,
        'total_stock_out':total_stock_out,
        'lin_1': line_1,
        'lin_2': line_2,
        
    }

    return render(request, 'production.html', context)


def InStock(request):
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
    retailor_stock_records = db.retailor_store_details
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
        for x in transport_records.find():
            datas = x['from_user'].split(',')[0]
            if datas == dstr_id:
                box_id_out.append(x['box_id'])
        # receiver_id=x['to_user'].split(',')[0]
        for x in store_records.find({'uid': dstr_id}):
            if (x['box_id'] not in box_id_out and x['box_id'] not in box_id_in):
                box_id_in.append(x['box_id'])
        print(box_id_out, box_id_in)
        # receiver_name=user_records.find_one({'uid':receiver_id})['registered_name']
        product_counts=[]
        for x in box_id_in:
            for x1 in store_records.find({'box_id': x}):
                box_in_data.append(x1)
                product_counts+=x1['product_qrcode'].split(',')
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
        # print('receiver_name',receiver_name)
        total_products=len(product_counts)
        total_boxes_in=len(box_id_in)
        total_boxes_out=len(box_id_out)

        total_production =len(list(store_records.find({'uid':uid})))
        context = {
            'username': username,
            'groups': groups,
            'data_in': box_in_data,
            'data_out': box_out_data,
            'total_product':total_products,
            'total_box_in':total_boxes_in,
            'total_production':total_production,
            'total_box_out':total_boxes_out,
            'status': 'IN',
            'uid': uid
        }
    elif usertype == 'Distributor':
        box_id_in = []
        box_id_out = []
        box_in_data = []
        box_out_data = []
        # product_id=[]
        #dstr_id = 'dist002'
        dstr_id=uid
        for x in transport_records.find():
            data = x['from_user'].split(',')[-1]
            if data == dstr_id:
                box_id_out.append(x['box_id'])
        box_id_out = list(set(box_id_out))
        for x in transport_records.find():
            data = x['to_user'].split(',')[0]
            if (data == dstr_id and x['box_id'] not in box_id_out):
                box_id_in.append(x['box_id'])
        # receiver_id=x['to_user'].split(',')[-1]
        # receiver_name = user_records.find_one({'uid': receiver_id})['registered_name']
        # print('receiver_id',receiver_id,'receiver_name',receiver_name)
        box_id_in = list(set(box_id_in))
        print(box_id_in, box_id_out)
        product_counts=0
        for x in box_id_in:
            for x1 in store_records.find({'box_id': x}):
                box_in_data.append(x1)
                print('x1',x1['product_qrcode'].split(','))
                product_counts+=len(x1['product_qrcode'].split(','))
        print('box_in_data:', box_in_data)
        for x in box_id_out:
            for x1 in store_records.find({'box_id': x}):
                box_out_data.append(x1)
        print('box_out_data', box_out_data)
        box_id_in=list(set(box_id_in))
        # instock box
        #total_box=len(box_id_in)
        total_product=product_counts
        total_boxes_in=len(box_id_in)
        total_boxes_out=len(box_id_out)
        context = {
            'username': username,
            'groups': groups,
            'data_in': box_in_data,
            'data_out': box_out_data,
            'total_product':total_product ,
            'total_box_out': total_boxes_out,
            'total_box_in':total_boxes_in,
            'status': 'IN',
            'uid': uid
        }
    elif usertype == 'Retailor':
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
        total_product = 0
        unique_boxes=[]
        unique_products=[]
        brand = []
        quantity = []
        mfg_date = []
        for x in box_id_in:
            if retailor_stock_records.find_one({'box_id':x}) is not None:
                box_rec_data = store_records.find_one({'box_id': x})
                for x1 in retailor_stock_records.find({'box_id':x},{'_id':0}):
                    if x1['product_status'] == 'OUT':
                        #product_out.append(x1['product_qrcode'])
                        product_out_item.append(x1)
                    else:
                        #product_in.append(x1['product_qrcode'])
                        unique_boxes.append(x1['box_id'])
                        unique_products.append(x1['product_qrcode'])
                        x1['brand'] = box_rec_data['brand']
                        x1['quantity'] = box_rec_data['quantity']
                        x1['mfg_date'] = box_rec_data['mfg_date']
                        x1['date'] = datetime.datetime.now().date()
                        product_in_item.append(x1)
        print('product_out', len(set(product_out)), 'product_in', len(set(product_in)))
        print(product_in_item)
        total_box = list(set(unique_boxes))
        total_product=list(set(unique_products))
        total_boxes=len(total_box)
        total_products=len(total_product)
        context = {
            'username': username,
            'groups': groups,
            'data_in': product_in_item,
            'data_out': product_out_item,
            'total_product': total_products,
            'total_box': total_boxes,
            'status': 'IN',

            'uid': uid
        }
    return render(request, 'in_stock.html', context)


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
    retailor_stock_records=db.retailor_store_details
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
        if len(list(transport_records.find())) > 0:
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
            product_counts=[] #total product count
            for x in box_id_in:
                for x1 in store_records.find({'box_id': x}):
                    box_in_data.append(x1)
            for x in box_id_out:
                for x1 in store_records.find({'box_id': x}):
                    box_out_data.append(x1)
                    product_counts+=x1['product_qrcode'].split(',')

            for x in store_records.find({'uid': dstr_id}):
                box_id.append(x['box_id'])
            box_id = list(set(box_id))
            for x in box_id:
                for x1 in store_records.find({'box_id': x}):
                    product_id.append(x1['product_qrcode'])
            product_id = list(set(product_id))
            print('box_id', box_id, 'product_id', product_id)
            print('receiver_name', receiver_name)
            total_products=len(product_counts)
            total_boxes_out=len(box_id_out)
            total_boxes_in=len(box_id_in)
            total_production =len(list(store_records.find({'uid':uid})))
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                'total_product': total_products,
                'total_box_in': total_boxes_in,
                'total_box_out': total_boxes_out,
                'total_production':total_production,
                'receiver_name': receiver_name,
                'status': 'OUT',
                'uid': uid
            }
        else:
            total_boxes_in =len(list(store_records.find({'uid':uid})))
            total_production =len(list(store_records.find({"$and":[{'uid':uid},{'production_line':'1'}]})))
            
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                'total_product': 0,
                'total_box_out': 0,
                'total_box_in': total_boxes_in,
                'total_production':total_production,
                'receiver_name': "",
                'status': 'OUT',
                'uid': uid
            }
    elif usertype == 'Distributor':
        box_id_in = []
        box_id_out = []
        box_in_data = []
        box_out_data = []
        # product_id=[]
        dstr_id = uid
        if len(list(transport_records.find())) > 0:
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
            product_counts=0
            for x in box_id_in:
                for x1 in store_records.find({'box_id': x}):
                    box_in_data.append(x1)
            print('box_in_data:', box_in_data)
            for x in box_id_out:
                for x1 in store_records.find({'box_id': x}):
                    box_out_data.append(x1)
                    product_counts+=len(x1['product_qrcode'].split(','))
            print('box_out_data', box_out_data)
            # instock box
            box_id_out=set(box_id_out)
            total_boxes = len(box_id_out)
            total_products = product_counts
            total_boxes_out=len(box_id_out)
            total_boxes_in=len(box_id_in)
            context = {
                'username': username,
                'groups': groups,
                'data_in': box_in_data,
                'data_out': box_out_data,
                'total_product': total_products,
                'total_box_out': total_boxes_out,
                'total_box_in': total_boxes_in,
                'receiver_name': receiver_name,
                'status': 'OUT',
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
                'status': 'OUT',
                'uid': uid
            }
    elif usertype == 'Retailor':
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
        total_product = 0
        unique_products=[]
        unique_boxes=[]
        brand=[]
        quantity=[]
        mfg_date=[]
        for x in box_id_in:
            if retailor_stock_records.find_one({'box_id':x}) is not None:
                box_rec_data=store_records.find_one({'box_id':x})
                print('box_rec_data',type(box_rec_data))
                for x1 in retailor_stock_records.find({'box_id':x},{'_id':0}):
                    if x1['product_status'] == 'OUT':
                        #product_out.append(x1['product_qrcode'])
                        unique_products.append(x1['box_id'])
                        unique_boxes.append(x1['product_qrcode'])
                        ##print('x1',type(x1))
                        x1['brand']=box_rec_data['brand']
                        x1['quantity']=box_rec_data['quantity']
                        x1['mfg_date']=box_rec_data['mfg_date']
                        x1['date'] = datetime.datetime.now().date()
                        product_out_item.append(x1)
                    else:
                        #product_in.append(x1['product_qrcode'])

                        product_in_item.append(x1)
        #print('product_out', len(set(product_out)), 'product_in', len(set(product_in)))
        print(product_in_item)
        #total_box = len(box_id_in)
        total_box = list(set(unique_boxes))
        total_product = list(set(unique_products))
        total_boxes = len(total_box)
        total_products = len(total_product)
        zip_context=zip(product_out_item,brand,quantity,mfg_date)
        context = {
            'username': username,
            'groups': groups,
            'data_in': product_in_item,
            'data_out': product_out_item,
            'total_product': total_products,
            'total_box': total_boxes,
            'status': 'OUT',
            'receiver_name': 'Customer',
            'uid': uid,
        }
        print('username',username,'uid',uid)
    return render(request, 'out_stock.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')

#new added
def tracking_items(request):
    username = request.user
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
    retailor_stock_records = db.retailor_store_details
    context = {}
    showing_status=[]
    box_ids = []
    showing_status.clear()
    if request.method == 'POST':
        box_id = request.POST.get('box_id')
        product_id=request.POST.get('product_id')
        print('box_id', len(box_id),"product_id",len(product_id))
        traced = []
        ids = []
        name_traced = []
        status=['IN']
        if len(box_id)>0:
            box_data = store_records.find_one({'box_id': box_id})
            if box_data is not None:
                traced = [box_data['uid']]
                box_ids.append(box_id)
                ids.append(box_data['id'])
                trns_data = transport_records.find_one({'box_id': box_id})
                # traced.append(trns_data['from_user'].split(',')[0])
                if trns_data is not None:
                    traced += trns_data['to_user'].split(',')
                    #flag = 0
                    #new added
                    retailor_has_data=retailor_stock_records.find_one({'box_id': box_id})
                    #end added
                    if retailor_has_data is not None:
                        flag = 0
                        for x in retailor_stock_records.find({'box_id': box_id}):
                            if x['product_status'] == 'IN':
                                flag = 1
                        if flag == 0:
                            traced.append('OUT')
                        else:
                            traced.append('IN')
                    else:
                        traced.append('IN')
            for x in traced:
                if x != 'IN' or x != 'OUT':
                    userdt = user_records.find_one({'uid': x})
                    if userdt is not None:
                        name_traced.append(userdt['registered_name'])
            if len(traced)>0:
                if traced[-1] != 'IN' and traced[-1] != 'OUT':
                    name_traced.append('IN')
                else:
                    name_traced.append(traced[-1])
            if len(name_traced) == 4:
                context = {'id': ids[0], 'box_id': box_ids[0], 'product_qrcode': '---', 'distiller': name_traced[0],
                           'distributor': name_traced[1], 'retailor': name_traced[2], 'status': name_traced[3]}
            elif len(name_traced) == 3:
                context = {'id': ids[0], 'box_id': box_ids[0], 'product_qrcode': '---', 'distiller': name_traced[0],
                           'distributor': name_traced[1], 'retailor': '---', 'status': name_traced[2]}
            elif len(name_traced) == 2:
                context = {'id': ids[0], 'box_id': box_ids[0], 'product_qrcode': '---', 'distiller': name_traced[0],
                           'distributor': '---', 'retailor': '---', 'status': name_traced[1]}
            #print(context)
        elif len(product_id)>0:
            #traced = []
            #name_traced = []
            #ids = []
            for x in store_records.find():
                if product_id in x['product_qrcode'].split(','):
                    box_ids.append(x['box_id'])
                    traced.append(x['uid'])
                    ids.append(x['id'])
                    break
            if len(box_ids) > 0:
                trns_data = transport_records.find_one({'box_id': box_ids[0]})
                if trns_data is not None:
                    traced += trns_data['to_user'].split(',')
                    flag = 0
                    ret_data=retailor_stock_records.find_one({'product_qrcode': product_id})
                    if ret_data['product_status']=='OUT':
                        traced.append('OUT')
                    else:
                        traced.append('IN')
                #traced.append('IN')
            for x in traced:
                if x != 'IN' or x != 'OUT':
                    userdt = user_records.find_one({'uid': x})
                    if userdt is not None:
                        name_traced.append(userdt['registered_name'])
            if traced[-1] != 'IN' and traced[-1] != 'OUT':
                name_traced.append('IN')
            else:
                name_traced.append(traced[-1])
            #context = {}
            if len(name_traced) == 4:
                context = {'id': ids[0], 'box_id': box_ids[0], 'product_qrcode': product_id, 'distiller': name_traced[0],
                           'distributor': name_traced[1], 'retailor': name_traced[2], 'status': name_traced[3]}
            elif len(name_traced) == 3:
                context = {'id': ids[0], 'box_id': box_ids[0], 'product_qrcode': product_id, 'distiller': name_traced[0],
                           'distributor': name_traced[1], 'retailor': '---', 'status': name_traced[2]}
            elif len(name_traced) == 2:
                context = {'id': ids[0], 'box_id': box_ids[0], 'product_qrcode': product_id, 'distiller': name_traced[0],
                           'distributor': '---', 'retailor': '---', 'status': name_traced[1]}
        #print(f'context for product:{context}')
        if len(box_ids)>0:
            box_temp_data=store_records.find_one({'box_id':box_ids[0]})
            user_dt = user_records.find_one({'uid': box_temp_data['uid']})
            #print('box_temp_data',box_temp_data,'user_dt',user_dt,"user_dt['usertype']",user_dt['usertype'],user_dt['uid']==uid)
            if box_temp_data is not None and user_dt is not None and user_dt['usertype'] == 'Distiller' and user_dt['uid']==uid:
                showing_status.append('yes')
            else:
                usr_type = user_records.find_one({'uid': uid})
                if  box_temp_data is not None and usr_type is not None and usr_type['usertype'] == 'Distributor':
                    showing_status.append('yes')
                else:
                    showing_status.append('no')
            if showing_status[0]=='no':
                context={}

    return render(request, 'tracking_items.html',context)

def download_invoice_pdf(request):
    pass

