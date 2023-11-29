from django.contrib import admin
from .models import Employee, Department, Project, JobRole, Certificate, Leave, Team

admin.site.register(JobRole)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Certificate)
admin.site.register(Leave)
admin.site.register(Team)
admin.site.register(Project)
