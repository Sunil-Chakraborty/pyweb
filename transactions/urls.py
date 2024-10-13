from django.urls import path
from .import views

app_name = 'transactions'

urlpatterns = [    
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit_transaction/<int:transactionId>/', views.edit_transaction, name='edit_transaction'),
    
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
]