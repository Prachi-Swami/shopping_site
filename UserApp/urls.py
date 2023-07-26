from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('ShowEcommerces/<id>',views.ShowEcommerces),
    path('ViewDetails/<id>',views.ViewDetails),
    path('Login',views.Login),
    path('SignUp',views.SignUp),
    path('Logout',views.Logout),
    path('AddToCart',views.AddToCart),
    path('ShowCart',views.ShowCart),
    path('ModifyCart',views.ModifyCart),
     path('MakePayment',views.MakePayment),
]
    
