from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name="homepage"),
    path('login', views.LoginPage, name="login"),
    path('register', views.Registration, name="register"),
    path('logout', views.Logout, name="logout"),
]