from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models import Ecommerce,Category,Accounts,OrderMaster
from UserApp.models import UserInfo,MyCart

# Create your views here.
def homepage(request):
    cats = Category.objects.all()
    Ecommerces = Ecommerce.objects.all()
    return render(request,"homepage.html",{"cats":cats,"Ecommerces": Ecommerces})
def ShowEcommerces(request,id):
    cat = Category.objects.get(id=id)
    Ecommerces  = Ecommerce.objects.filter(cat_fk = id)
    cats = Category.objects.all()
    return render(request,"homepage.html",{"Ecommerces":Ecommerces,"cats":cats,"cat":cat})
def ViewDetails(request,id):
    Ecommerces = Ecommerce.objects.get(id=id)
    cats = Category.objects.all()
    return render(request,"ViewDetails.html",{"Ecommerces":Ecommerces,"cats":cats})
def AddToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):                    
            eid = request.POST["eid"]
            qty = request.POST["qty"]
            uname = request.session["uname"]
            item = MyCart()
            item.user = UserInfo.objects.get(username = uname)
            item.Ecommerce = Ecommerce.objects.get(id=eid)
            item.qty = qty
            item.save()
            return redirect(ShowCart)
        else:
            return redirect("Login")

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv  = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = Accounts.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            owner = Accounts.objects.get(cardno='222',cvv='222',expiry='12/2030')
            amount = request.session["total"]
            buyer.balance -= amount
            owner.balance +=amount
            buyer.save()
            owner.save()
            #delete all items from cart
            items = MyCart.objects.filter(user = request.session["uname"])
            order = OrderMaster()
            order.user = UserInfo.objects.get(username = request.session["uname"])
            order.amount = request.session["total"]
            details = []
            for item in items:
                details.append(item.Ecommerce.product_name)
                item.delete()
            
            order.details = ",".join(details)
            order.save()

            return redirect(homepage)

        
def ShowCart(request):
    items = MyCart.objects.filter(user = request.session["uname"])
    total = 0 
    for item in items:
        total += item.qty * item.Ecommerce.price
    request.session["total"] = total
    cats = Category.objects.all()
    return render(request,"ShowCart.html",{"items":items,"cats":cats})
   
def ModifyCart(request):
    action = request.POST["action"] #action -> remove / update
    eid = request.POST["eid"]   #Hidden field  
    item = MyCart.objects.get(user = request.session["uname"],Ecommerce = eid)
    
    if(action == "Remove"):
        item.delete()
    else: #update
        item.qty = request.POST["qty"]
        item.save() #update
    return redirect(ShowCart)    

def Login(request):
    if(request.method == "GET"):
        return render(request,"Login.html",{})
    else: 
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        try:
            user = UserInfo.objects.get(username=uname,password=pwd)
        except:
            #return HttpResponse("User not present")
            return redirect(Login)
        else:
            request.session["uname"]=uname
            return redirect(homepage)

def SignUp(request):
    if(request.method == "GET"):
        return render(request,"SignUp.html",{})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        email = request.POST["email"]
        try:
            user = UserInfo.objects.get(username=uname)
        except:
            #return HttpResponse("User not present")
            user = UserInfo(uname,pwd,email)
            user.save()
            return redirect(homepage)
        else:
            return redirect(SignUp)
        
def Logout(request):
    request.session.clear()
    return redirect(homepage)        


