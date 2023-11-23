from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
import pymongo
from pymongo import MongoClient
import certifi

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    registration_number = models.CharField(max_length=200, null=True)
    
    usertype = models.CharField(max_length=20, null=True)
    registered_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=128, null=True)
    status = models.BooleanField(default=True, null=True)
    uuid = models.CharField(max_length=10, unique=True,null=True)
    master_key = models.CharField(max_length=10, null=True)
    #user_image = models.ImageField(upload_to='userprofile', null=True, default='default.jpg')
    

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Save to SQLite
        super(Profile, self).save(*args, **kwargs)

        # Save to MongoDB
        client=MongoClient("mongodb+srv://ajaytiwarinitjsr:Ajt02011998@cluster0.umftw04.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        db=client.get_database('track_and_trace_datahub')
        collection = db["user_details"]
        user_detail = {
            "usertype": self.usertype,
            "registered_name": self.registered_name,
            "username": self.username,
            "password": self.password,
            "Address": self.address,
            "contact_no": self.phone,
            "email": self.email,
            "status": self.status,
            "uid": self.uuid,
            "master_key": self.master_key,
        }
        collection.insert_one(user_detail)
        client.close()
