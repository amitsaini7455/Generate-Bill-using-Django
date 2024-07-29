from django.contrib import admin
from django.urls import path
from home.views import receipts, update_receipt, delete_receipt, login_page, register_page, custom_logout, pdf
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', receipts, name='receipts'),
    path('update_receipt/<int:id>/', update_receipt, name='update_receipt'), 
    path('delete_receipt/<int:id>/', delete_receipt, name='delete_receipt'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', custom_logout, name='logout'),
    path('pdf/', pdf, name='pdf'),
]