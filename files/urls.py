from django.urls import path
from . import views
from .views import FileListView

app_name = 'files'

urlpatterns = [
    path('', views.directory_view, name='home'),
    path('directory/<int:dir_id>/', views.directory_view, name='directory_view'),
    path('add_directory/', views.add_directory, name='add_directory'),
    path('file_list/', FileListView.as_view(), name='file_list'),  # Add this line
    path('delete_directory/<int:pk>/', views.delete_directory, name='delete_directory'),
    path('add_file/', views.add_file, name='add_file'),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('files/listing/', views.file_listing, name='file_listing'),   
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
]
