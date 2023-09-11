from django.urls import path
from . import views


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('helloWorld/', views.helloWorld, name='helloWorld'),
]