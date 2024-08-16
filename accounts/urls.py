# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, signup_view, home_view
from django.views.generic import RedirectView


app_name = 'account'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('home/', home_view, name='home'),  # Add your home view here
    path('logout/', auth_views.LogoutView.as_view(next_page='account:login'), name='logout'),
    path('', RedirectView.as_view(url='account:login', permanent=True)),  # Redirect root URL to login


]
