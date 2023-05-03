from os import stat
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/',include('base.urls')),
 
    path('api/clients/',include('base.urls.client_urls')),
    path('api/users/',include('base.urls.user_urls')),
   
    

]
