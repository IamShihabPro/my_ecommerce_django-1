from django.urls import path
from App_Shop import views




urlpatterns = [
   path('', views.Home.as_view(), name='home')
]
