from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeHomePage, name="emp_home"),
    path('profile/', views.EmployeeProfile, name="emp_profile"),
    path('leaves/', views.EmployeeLeaves, name="emp_leaves"),
    path('certificates/', views.EmployeeCertificates, name="emp_cetificate")
]