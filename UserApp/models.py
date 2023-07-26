from django.db import models
from AdminApp.models import Ecommerce

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key = True)
    password = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "UserInfo"

class MyCart(models.Model):
    user = models.ForeignKey('UserInfo',on_delete = models.CASCADE)
    Ecommerce =models.ForeignKey('AdminApp.Ecommerce',on_delete = models.CASCADE)
    qty = models.IntegerField()  
    class Meta:
        db_table = "MyCart"          

