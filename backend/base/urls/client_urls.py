from django.urls import path
from base.views import client_views as views


urlpatterns = [
    path('',views.getClients,name="clients"),

    path('create/',views.createClient,name="create_client"),
    
    #path('upload/',views.uploadImage,name="upload_image"),
     #path('top/',views.getTopClients,name="top-Clients"),

    path('<str:pk>/projects/',views.createClientProject,name="create-project"),
   
    path('<str:pk>/',views.getClient,name="client"),

    path('update/<str:pk>/',views.updateClient,name="update_client"),
    path('delete/<str:pk>/',views.deleteClient,name="delete_client"),
]