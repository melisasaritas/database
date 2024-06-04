from django.urls import path
from django.views.generic import TemplateView
from .views import custom_register_view, custom_view, custom_login_view, custom_home_view, add_to_cart, view_cart, checkout, remove_item, custom_computers_view, custom_stock_data, custom_components_view, add_components_to_cart, show_monitors, show_keyboards, show_rams, show_ssds, show_hdds, show_cpus, show_gpus, custom_insert_preassembled_view, custom_remove_preassembled_view

app_name = 'myapp'

urlpatterns = [
    path('', custom_home_view, name=""),
    path('add_to_cart/<int:product_id>/<int:ram>/<str:price>/<int:processor>/<str:name>/',
         add_to_cart, name='add_to_cart'),
    path('add_components_to_cart/<int:product_id>/<str:price>/<str:name>/',
         add_components_to_cart, name='add_components_to_cart'),
    path('monitors', show_monitors, name='show_monitors'),
    path('keyboards', show_keyboards, name='show_keyboards'),
    path('rams', show_rams, name='show_rams'),
    path('ssds', show_ssds, name='show_ssds'),
    path('hdds', show_hdds, name='show_hdds'),
    path('cpus', show_cpus, name='show_cpus'),
    path('gpus', show_gpus, name='show_gpus'),

    path('BuildPc', custom_components_view, name="shop.html"),
    path('PreMade', custom_computers_view, name="computers.html"),

    path('ContactUs', TemplateView.as_view(template_name="contact.html")),

    path('ShoppingCart', view_cart, name='view_cart'),
    path('checkout', checkout, name='checkout'),
    path('remove_item/<int:product_id>/', remove_item, name='remove_item'),

    path('AdminPanel/', TemplateView.as_view(template_name="index2.html")),
    path('AdminPanel/History', TemplateView.as_view(template_name="history.html")),
    path('AdminPanel/Stock_Data', custom_stock_data, name="stock_data.html"),
    path('AdminPanel/User_Data',
         TemplateView.as_view(template_name="user_data.html")),
    path('AdminPanel/insert_computer', custom_insert_preassembled_view,
         name="custom_insert_preassembled_view"),
    path('AdminPanel/remove_computer', custom_remove_preassembled_view,
         name="custom_remove_preassembled_view"),

    path('login', custom_login_view, name='login'),
    path('signup', custom_register_view, name='signup'),
    path('UserAccount', TemplateView.as_view(
        template_name="useraccountnew.html")),


]
