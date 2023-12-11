from django.urls import path
from App_Payment import views


urlpatterns = [
   path('checkout/', views.checkout, name='checkout')
]
