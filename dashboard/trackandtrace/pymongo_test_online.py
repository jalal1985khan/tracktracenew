
from pymongo import MongoClient
import certifi

client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
#db=client.get_database('track_and_trace_datahub')

"""
records=db.user_details
records.insert_one({"distiller's Name":"Amrit's Distiller","id":2})
for x in records.find():
  print(x)
"""

"""
records=db.user_details
data={"uid":'ret2',"usertype":"retailor","registered_name":"Tonique",
      "username":"Tonique","password":"123","Address":"Rathnams complex shanthala nagar",
      "contact_no":"8151134752","email":"tonique@gmail.com","status":True}
records.insert_one(data)"""
"""
for x in records.find():
  if x['status']==True:
    print(x)
"""
"""
from datetime import datetime
records=db.store_details
data={"id":2,"user_id":2,"box_id":"2","product_qrcode":"1","brand":"Signature","Quantity":90,
      "mfg_date":str(datetime.now().date()),"time_stemp":str(datetime.now().time()),"date":str(datetime.now().date()),
      "production_line":"line-1","system_id":"assdsd124"}
records.insert_one(data)
for x in records.find():
  print(x)
"""
"""
from datetime import datetime
records=db.transport_details
data={"id":2,"box_id":"2","from_user_type":"","to_user_type":"","from_user":"","to_user":"",
      "date":"","from_user_status":"","to_user_status":""}
records.insert_one(data)
for x in records.find():
  print(x)
"""
"""
from datetime import datetime
records=db.retailor_store_details
data={"id":1,"retailor_id":2,"box_id":1,"product_id":1,"instock_date":str(datetime.now().date()),
      'sold_date':str(datetime.now().date()),"status":"sold"}
records.insert_one(data)
for x in records.find():
  print(x)
  
"""
"""
#login query
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.user_details
condition1={"username":"john"}
condition2={"password":"123"}
query = {"$and": [condition1, condition2]}
data = records.find_one(query)
print(data['registered_name'],',',data['usertype'])
"""
"""
#signup query
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.user_details
password1=""
password2=""
data={"uid":"ret1","usertype":"retailor","registered_name":"The Winery","username":"winery","password":"ret1","Address":"No. 485, 9th Main, Hal 2nd Stage-indiranagar, Bangalore - 560008 (Near Indiranagar Club)",
      "contact_no":"2323234325","email":"winery@gmail.com","master_key":"rtmstr1","status":True}
if password1==password2:
    db.user_details.insert_one(data)
"""
"""
#showing all data distillerwise
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.store_details
for x in records.find({"uid":"dist1"}):
    print(x)
"""
"""
#remaining data distillerwise
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
distiller_record=list(set([x['box_id'] for x in records.find() if x['from_user'].split(',')[0]=='dist1']))
store_record=db.store_details
remaining_items_for_distiller=[x['box_id'] for x in store_record.find() if x['box_id'] not in distiller_record]

#data=[x['box_id'] for x in records.find({"from_user":"dist1"})]
print(distiller_record.copy()[::-1])
print(remaining_items_for_distiller)
"""
"""
#distributor details total data
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
distiller_id="dstr1"
data=[x['box_id'] for x in records.find() if x['to_user'].split(',')[0]==distiller_id]
print(data)
"""
"""
#distributor details remaining data
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
distiller_id="dstr1"
data=[x['box_id'] for x in records.find() if x['from_user'].split(',')[-1]!=distiller_id and x['to_user'].split(',')[0]==distiller_id]
print(data)
"""
"""
#retailorwise complete data
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
retailor_id="ret1"
data=[x['box_id'] for x in records.find() if x['to_user'].split(',')[-1]==retailor_id]
print(data)
"""
"""
#retailorwise remaining data
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
records_temp=db.store_details
retailor_id="ret1"
data=[x['box_id'] for x in records.find() if x['to_user'].split(',')[-1]==retailor_id]
data1=[x['product_qrcode'] for x in records_temp.find() if x['box_id'] in data and x['product_status']=='in']
print(data1)
"""
"""
#production line
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.store_details
production_line='line-1'
for x in records.find({'production_line':production_line}):
    print(x)
"""
"""
#traceing box
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
records_usr=db.user_details
box_id='6'
tracing_data=records.find_one({'box_id':box_id})
if tracing_data is not None:
    tracing_data=[(x['from_user'].split(','),x['to_user'].split(',')[-1]) for x in records.find({'box_id':box_id})]
    print(','.join(tracing_data[0][0])+','+tracing_data[0][1])
    list1 = tracing_data[0][0]
    list1.append(tracing_data[0][1])
    for x in list1:
        print(records_usr.find_one({'uid':x})['registered_name'])

    #print(tracing_data[0][0])
    #print(list1)
else:
    records_temp = db.store_details
    tracing_data=records_temp.find_one({'box_id':box_id})
    print(tracing_data['uid'])
    print(records_usr.find_one({'uid':tracing_data['uid']})['registered_name'])
#print(tracing_data[0][1])
#print(','.join(traceing_data[0]))
"""
"""
#user showing
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.user_details
for x in records.find():
    print(x)
"""
"""
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.store_details
records_temp=db.user_details
data1=records_temp.find_one({'username':'john'})
condition1={"uid":data1['uid']}
condition2={"production_line":"line-1"}
query = {"$and": [condition1, condition2]}
data = records.find_one(query)
for x in records.find(query):
    print(x)
"""
"""
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.store_details
box_id=[]
product_id=[]
for  x in records.find({'uid':'dist1'}):
    box_id.append(x['box_id'])
    product_id.append(x['product_qrcode'])
print(len(set(box_id)), len(set(product_id)))
"""
"""
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.store_details
box_id=[]
product_count=[]
for  x in records.find({'uid':'dist1'}):
    box_id.append(x['box_id'])
box_id=list(set(box_id))
brand=[]
quantity=[]
mfg_date=[]
date=[]
production_line=[]
system_id=[]
user_id=[]
status=[]
record_trans=db.transport_details
for x in set(box_id):
    product_count.append(len(set([x['product_qrcode'] for x in records.find({'box_id':x})])))
    data=records.find_one({'box_id':x})
    brand.append(data['brand'])
    quantity.append(data['quantity'])
    mfg_date.append(data['mfg_date'])
    date.append(data['date'])
    production_line.append(data['production_line'])
    system_id.append(data['system_id'])
    user_id.append(data['uid'])
    status_data=record_trans.find_one({'box_id':x})
    if status_data is not None:
        status.append('out-stock')
    else:
        status.append('in-stock')

print(box_id,product_count,brand,quantity,mfg_date,date,production_line,system_id,user_id,status)
"""
"""
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
user_records=db.store_details
box_id=[]
product_id=[]
dstr_id='dstr2'
for  x in records.find():
    data=x['to_user'].split(',')[0]
    if data==dstr_id:
        box_id.append(x['box_id'])
for x in box_id:
    for x1 in user_records.find({'box_id':x}):
        print(x1)
        product_id.append(x1['product_qrcode'])
print(box_id)
print(len(set(box_id)), len(set(product_id)))

"""
"""
#distributor
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
transport_records=db.transport_details
store_records=db.store_details
box_id_in=[]
box_id_out=[]
box_in_data=[]
box_out_data=[]
#product_id=[]
dstr_id='dist002'
for  x in transport_records.find():
    data=x['from_user'].split(',')[-1]
    if data==dstr_id:
        box_id_out.append(x['box_id'])
box_id_out=list(set(box_id_out))
for  x in transport_records.find():
    data=x['to_user'].split(',')[0]
    if (data==dstr_id and x['box_id'] not in box_id_out):
        box_id_in.append(x['box_id'])
box_id_in=list(set(box_id_in))
print(box_id_in,box_id_out)
for x in box_id_in:
    for x1 in store_records.find({'box_id':x}):
        print(x1)
        box_in_data.append(x1['product_qrcode'])
print('box_in_data:',box_in_data)
for x in box_id_out:
    for x1 in store_records.find({'box_id':x}):
        print(x1)
        box_out_data.append(x1['product_qrcode'])
print('box_out_data',box_out_data)
"""
"""
#retailor
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
records=db.transport_details
store_records=db.store_details
retailor_id="retr003"
box_id_in=[]
product_in=[]
product_out=[]
product_in_item=[]
product_out_item=[]
for x in records.find():
    if x['to_user'].split(',')[-1]==retailor_id:
        box_id_in.append(x['box_id'])
print(box_id_in)
for x in box_id_in:
    for x1 in store_records.find({'box_id':x}):
        if x1['product_status']=='out':
            product_out.append(x1['product_qrcode'])
            product_out_item.append(x1)
        else:
            product_in.append(x1['product_qrcode'])
            product_in_item.append(x1)
print('product_out',len(set(product_out)))
#print('product_out',len(set(product_out)),'product_in',len(set(product_in)))
#print(product_in_item)
"""
"""
#retailor
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
transport_records=db.transport_details
store_records=db.store_details
retailor_id="ret1"
box_id_in=[]
product_instock=[]
product_outstock=[]
for x in transport_records.find():
    if x['to_user'].split(',')[-1]==retailor_id:
        box_id_in.append(x['box_id'])
for x in box_id_in:
    for x1 in store_records.find({'box_id':x}):
        if x1['product_status']=='out':
            product_outstock.append(x1)
        else:
            product_instock.append(x1)
print(product_outstock)
print(len(product_outstock), len(product_instock))

"""
"""
def signup_method(usertype,registered_name,username,password1,password2,Address,contact_no,email,master_key,status=True):
    # signup query
    client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
    db = client.get_database('track_and_trace_datahub')
    records = db.user_details
    uid_temp = []
    max_id = 0
    uid_first=[]
    uid_second = []
    uid_sec = ""
    for x in records.find({'usertype': usertype}):
            uid_temp.append(x['uid'])

    for x in uid_temp:
            for x1 in x:
                    if x1.isdigit():
                            uid_first.append(x1)
                    else:
                            uid_second.append(x1)
            uid_sec = ''.join(uid_second)
            max_id = max(max_id, int(''.join(uid_first)))
            uid_first.clear()
            uid_second.clear()
    uid = uid_sec + str(max_id + 1)

    data = {"uid": uid, "usertype": usertype, "registered_name": registered_name, "username": username, "password": password1, "Address": Address,
            "contact_no": contact_no, "email": email, "master_key": master_key, "status": status}
    existed_user_check=records.find_one({"uid":uid})
    if password1 == password2 and existed_user_check is None:
        db.user_details.insert_one(data)
signup_method("distributor","test","test",123,123,"btm","1211212121","ajay@gmail.com","mstr",status=True)
"""
"""
usertype = "retailor"
uid_first=[]
uid_second=[]
client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
db = client.get_database('track_and_trace_datahub')
records = db.user_details
uid_temp=[]
max_id=0
uid_second=[]
uid_sec=""
for x in records.find({'usertype':usertype}):
        uid_temp.append(x['uid'])

for x in uid_temp:
        for x1 in x:
                if x1.isdigit():
                        uid_first.append(x1)
                else:
                        uid_second.append(x1)
        uid_sec=''.join(uid_second)
        max_id=max(max_id,int(''.join(uid_first)))
        uid_first.clear()
        uid_second.clear()
uid=uid_sec+str(max_id+1)
print(uid)
"""

"""
client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
db = client.get_database('track_and_trace_datahub')
#for x in db.store_details.find({'product_qrcode':"0325306570".lstrip('0')}):
#        print(x)
num="325306570"
print(db.store_details.find_one({'product_qrcode':num}))
print(db.store_details.find_one({"product_qrcode": {"$toInt": int(num)}}))
#{"number": {"$toInt": 10}
"""
"""
#for update
client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
db = client.get_database('track_and_trace_datahub')
records = db.transport_details
records.insert_one({'name':'ajay'})
records1=records = db.store_details
records1.insert_one({'name':'ajay'})
"""
"""
import datetime
client = MongoClient(
        "mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())
db = client.get_database('track_and_trace_datahub')
records = db.store_details
#total
print('total records count')
print(f'Total Products: {len(set([x["product_qrcode"] for x in records.find()]))}')
print(f'Total Boxes: {len(set([x["box_id"] for x in records.find()]))}')
#daywise
print(set([x['mfg_date'] for x in records.find()]))
mfg_date=set([x['mfg_date'] for x in records.find()])
for x in mfg_date:
        dateTimeObj = datetime.datetime.strptime(x, "%Y-%m-%d").date()
        print(dateTimeObj)"""
"""
db = client.get_database('track_and_trace_datahub')
records = db.store_details
data=records.find({},{'product_qrcode':1,'_id':0})
product_id='7'
for x in data:
        if product_id in x['product_qrcode'].split(','):
                print("yes")"""
"""
#here is the logic for retailor table
db = client.get_database('track_and_trace_datahub')
user_records = db.user_details
receiver_id='retr003'
box_id='12'
user_type = user_records.find_one({'uid': receiver_id})['usertype']
if user_type=='Retailor':
        retailor_records=db.retailor_store_details
        store_records=db.store_details
        transport_records=db.transport_details
        query={"box_id": box_id}
        transport_status=transport_records.find_one(query)
        store_status=store_records.find_one(query)
        #print('transport_status',transport_status,'store_status',store_status)
        if transport_status is not None and store_status is not None:
                list_of_all_product_qrcode=store_status['product_qrcode'].split(',')
                for x in list_of_all_product_qrcode:
                        data={'box_id':box_id,'product_qrcode':x,'product_status':'IN'}
                        retailor_records.insert_one(data)
        else:
                print('invalid box number')
"""
"""
#here is the logic for retailor table
#retailor
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
transport_records=db.transport_details
#store_records=db.store_details
retailor_stock_records=db.retailor_store_details
retailor_id="retr003"
box_id_in=[]
product_instock=[]
product_outstock=[]
for x in transport_records.find():
    if x['to_user'].split(',')[-1]==retailor_id:
        box_id_in.append(x['box_id'])
for x in box_id_in:
        if retailor_stock_records.find_one({'box_id':x}) is not None:
                for x1 in retailor_stock_records.find({'box_id':x},{'_id':0}):
                        if x1['product_status']=='OUT':
                                product_outstock.append(x1)
                        else:
                                product_instock.append(x1)
print(product_outstock)
print(len(product_outstock), len(product_instock))
"""
"""
#boxwise
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
transport_records=db.transport_details
store_records=db.store_details
retailor_stock_records=db.retailor_store_details
usr_details=db.user_details
box_id='1'
box_data=store_records.find_one({'box_id':box_id})
#print(box_data)
traced=[box_data['uid']]
ids=box_data['id']
name_traced=[]
if box_data is not None:
    trns_data=transport_records.find_one({'box_id':box_id})
    #traced.append(trns_data['from_user'].split(',')[0])
    if trns_data is not None:
        traced+=trns_data['to_user'].split(',')
        flag=0
        for x in retailor_stock_records.find({'box_id':box_id}):
            if x['product_status']=='IN':
                flag=1
        if flag==0:
            traced.append('OUT')
        else:
            traced.append('IN')
for x in traced:
    if x!='IN' or x!='OUT':
        userdt=usr_details.find_one({'uid':x})
        if userdt is not None:
            name_traced.append(userdt['registered_name'])
if traced[-1]!='IN' and traced[-1]!='OUT':
    name_traced.append('IN')
else:
    name_traced.append(traced[-1])
print(name_traced)
context={}
if len(name_traced)==4:
    context={'id':ids,'box_id':box_id,'product_id':'---','distiller':name_traced[0],
             'distributor':name_traced[1],'retailor':name_traced[2],'status':name_traced[3]}
elif len(name_traced)==3:
    context = {'id': ids, 'box_id': box_id, 'product_id': '---', 'distiller': name_traced[0],
               'distributor': name_traced[1], 'retailor': '---', 'status': name_traced[2]}
elif len(name_traced)==2:
    context = {'id': ids, 'box_id': box_id, 'product_id': '---', 'distiller': name_traced[0],
               'distributor': '---', 'retailor': '---', 'status': name_traced[1]}
print(context)
"""
"""
#productwise
client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.get_database('track_and_trace_datahub')
transport_records=db.transport_details
store_records=db.store_details
retailor_stock_records=db.retailor_store_details
usr_details=db.user_details
product_id='2'
box_ids=[]
traced=[]
name_traced=[]
ids=[]
for x in store_records.find():
    if product_id in x['product_qrcode'].split(','):
        box_ids.append(x['box_id'])
        traced.append(x['uid'])
        ids.append(x['id'])
        break
if len(box_ids)>0:
    trns_data=transport_records.find_one({'box_id':box_ids[0]})
    if trns_data is not None:
        traced+=trns_data['to_user'].split(',')
        flag=0
        for x in retailor_stock_records.find({'box_id':box_ids[0]}):
            if x['product_status']=='IN':
                flag=1
        if flag==0:
            traced.append('OUT')
        else:
            traced.append('IN')
for x in traced:
    if x!='IN' or x!='OUT':
        userdt=usr_details.find_one({'uid':x})
        if userdt is not None:
            name_traced.append(userdt['registered_name'])
if traced[-1]!='IN' and traced[-1]!='OUT':
    name_traced.append('IN')
else:
    name_traced.append(traced[-1])
context={}
if len(name_traced)==4:
    context={'id':ids[0],'box_id':box_ids[0],'product_id':product_id,'distiller':name_traced[0],
    'distributor':name_traced[1],'retailor':name_traced[2],'status':name_traced[3]}
elif len(name_traced)==3:
    context = {'id': ids, 'box_id': box_ids[0], 'product_id': '---', 'distiller': name_traced[0],
               'distributor': name_traced[1], 'retailor': '---', 'status': name_traced[2]}
elif len(name_traced)==2:
    context = {'id': ids, 'box_id': box_ids[0], 'product_id': '---', 'distiller': name_traced[0],
               'distributor': '---', 'retailor': '---', 'status': name_traced[1]}
#context={'id':ids[0],'box_id':box_ids[0],'product_id':product_id,'distiller':name_traced[0],'distributor':name_traced[1],'retailor':name_traced[2],'status':name_traced[3]}
print(context)
"""



