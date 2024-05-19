from django.urls import path
from django.views.generic import TemplateView
from .views import custom_view, custom_login_view

app_name = 'myapp'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('BuildPc', TemplateView.as_view(template_name="shop.html")),
    path('PreMade', TemplateView.as_view(template_name="computers.html")),
    path('ContactUs', TemplateView.as_view(template_name="contact.html")),
    path('ShoppingCart', TemplateView.as_view(template_name="cart.html")),

    path('AdminPanel/', TemplateView.as_view(template_name="index2.html")),
    path('AdminPanel/History', TemplateView.as_view(template_name="history.html")),
    path('AdminPanel/Stock_Data', TemplateView.as_view(template_name="stock_data.html")),
    path('AdminPanel/User_Data', TemplateView.as_view(template_name="user_data.html")),

    path('Check', TemplateView.as_view(template_name="chackout.html")),
    path('login', custom_login_view, name='login'),
    path('ShopDetail', TemplateView.as_view(template_name="shop-detail.html")),
    path('SignUp', TemplateView.as_view(template_name="signup.html")),
    path('UserAccount', TemplateView.as_view(template_name="useraccountnew.html")),
    
    #path('api/computers/', ComputerView.as_view(), name='computers-api'),
    path('helloworld/', custom_view, name='helloworld'),
    #path('deneme', custom_view(), name='detailcreate'),

]