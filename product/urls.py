from django.urls import path
from .import views


app_name = 'product'

urlpatterns = [    
    path('recepi/', views.recepi_list, name='recepi_list'),
    path('recepi/add/', views.recepi_add, name='recepi_add'),    
    path('recepi/edit/<int:recepi_id>/', views.recepi_edit, name='recepi_edit'),
    path('recepi/delete/<int:id>/', views.recepi_delete, name='recepi_delete'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),  # Add this line
    path('generate_excel/', views.generate_excel, name='generate_excel'),  # Add this line
    path('generate_labels/', views.generate_labels, name='generate_labels'),  # Add this line
    path('generate_html_report/', views.generate_html_report, name='generate_html_report'),
    path('generate_doc_report/', views.generate_doc_report, name='generate_doc_report'),
    path('generate-barcodes/', views.generate_barcodes_view, name='generate_barcodes'),

    path('mixprod/', views.mixprod_list, name='mixprod_list'),
    path('mixprod/create/', views.mixprod_create, name='mixprod_create'),    
    path('mixprod/edit/<int:pk>/', views.mixprod_edit, name='mixprod_edit'),
    path('mixprod/delete/<int:pk>/', views.mixprod_delete, name='mixprod_delete'),
    path('mixprod/view/<int:pk>/', views.mixprod_view, name='mixprod_view'),

] 
