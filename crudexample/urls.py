"""crudexample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('employee/', include('employee.urls',  namespace='employee' )),
    path('', RedirectView.as_view(url='accounts/login/', permanent=True)),  # Redirect root URL to login
    path('transaction/', include('transactions.urls',  namespace='transactions')),
    path('files/', include('files.urls',  namespace='files' )),
    path('photos/', include('photo_gallery.urls', namespace='photo_gallery')),
    path('product/', include('product.urls',  namespace='product' )),
    path('sales/', include('sales.urls',  namespace='sales' )),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


