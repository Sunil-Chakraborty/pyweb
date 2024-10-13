from django.urls import path
from .import views


app_name = 'sales'

urlpatterns = [
    path('invoice/<str:invoice_no>/', views.sales_invoice_print, name='sales_invoice_print'),
]