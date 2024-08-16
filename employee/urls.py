from django.urls import path
from .import views

app_name = 'employee'

urlpatterns = [
    path('dashboard/', views.dashboard, name='home'),
    path('show/', views.show, name='show'),
    path('showall/', views.showall, name='showall'),
    path('search/', views.search, name='search'),
    path('doc/<int:id>', views.doc, name='doc'),
    path('emp/', views.emp, name='emp'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.destroy, name='delete'),
]
