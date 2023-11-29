from django.urls import path
from . import views

urlpatterns = [
    path('', views.Hr_HomePage, name="hr_home"),
    path('addEmployee', views.AddEmployee, name="add_employee"),
    path('employeeInfo/<str:info>/<str:email>', views.EditEmployee, name="employee_info"),
    path('employeeList/', views.EmployeesList, name="employee_list"),
    path('leavesRequest/', views.LeaveRequestsPage, name="leaves_request"),
    path('jobroles/', views.JobRolesPage, name="job_roles"),
    path('edit_departments/', views.AddDepartmentPage, name="add_departments"),
    path('departments/', views.DepartmentsPage, name="departments"),
    path('teams/', views.TeamsPage, name="teams"),
    path('projects/', views.TeamsPage, name="projects"),
    path('editemployee/<str:info>/<str:email>/', views.EditEmployee, name="edit_employee"),
]