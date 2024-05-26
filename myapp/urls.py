from django.urls import path
from django.views.generic import TemplateView
from .views import custom_register_view, custom_view, custom_login_view, custom_home_view, add_to_cart, view_cart, checkout, remove_item

app_name = 'myapp'

urlpatterns = [
    path('', custom_home_view, name=""),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    
    path('BuildPc', TemplateView.as_view(template_name="shop.html")),
    path('PreMade', TemplateView.as_view(template_name="computers.html")),
    path('ContactUs', TemplateView.as_view(template_name="contact.html")),
    
    path('ShoppingCart', view_cart, name='view_cart'),
    path('checkout', checkout, name='checkout'),
    path('remove_item/<int:product_id>/', remove_item, name='remove_item'),
    
    path('AdminPanel/', TemplateView.as_view(template_name="index2.html")),
    path('AdminPanel/History', TemplateView.as_view(template_name="history.html")),
    path('AdminPanel/Stock_Data',
         TemplateView.as_view(template_name="stock_data.html")),
    path('AdminPanel/User_Data',
         TemplateView.as_view(template_name="user_data.html")),

    path('login', custom_login_view, name='login'),
    path('signup', custom_register_view , name='signup'),
    path('UserAccount', TemplateView.as_view(
        template_name="useraccountnew.html")),

]
