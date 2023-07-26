from django.contrib import admin
from .models import Category,Ecommerce,Accounts

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cat_name']

class productAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','price','description','image','cat_fk']
    
class AccountsAdmin(admin.ModelAdmin):
    list_display = ['cardno','cvv','expiry','balance']

admin.site.register(Ecommerce,productAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Accounts,AccountsAdmin)

