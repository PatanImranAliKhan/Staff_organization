from django.db import models
from hr_app.models import HR
from authenticate_app.models import Location

# Create your models here.

class JobRole(models.Model):
    jobId = models.AutoField(primary_key=True)
    jobRole = models.CharField(max_length=200, unique=True)
    JobLevel = models.IntegerField()
    salary = models.CharField(max_length=100)

    def __str__(self):
        return self.jobRole



class Department(models.Model):
    deptId = models.CharField(max_length=100, primary_key=True)
    deptName = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.deptName
        


class Project(models.Model):
    projectId = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=200)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    departmentId = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    LocationId = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.projectName
    


class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=200, default="HR")
    teamMem = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    manager = models.CharField(max_length=200)

    def __str__(self):
        return self.teamName



class Employee(models.Model):
    EmpID=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50, null=True)
    dob=models.DateField(null=True)
    email=models.EmailField(max_length=30,unique=True,blank=False)
    mobile=models.CharField(null=True, max_length=15)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    password=models.CharField(max_length=30)
    hr_details = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True)
    jobRole = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    is_manager = models.BooleanField(default=False)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    team=models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
         return self.email



class Certificate(models.Model):
    cirId = models.AutoField(primary_key=True)
    CirTitle = models.CharField(max_length=200)
    Technology = models.CharField(max_length=200)
    EarnDate = models.DateField(null=True)
    Expdate = models.DateField(null=True)
    empEmail = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1)



class Leave(models.Model):
    leaveId = models.AutoField(primary_key=True)
    LeaveType = models.CharField(max_length=200)
    StartDate = models.DateField(null=True)
    EndDate = models.DateField(null=True)
    NoOfHours = models.IntegerField(default=1)
    status = models.CharField(max_length=200, default="pending")
    empEmail = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1)



class Work(models.Model):
    wordId = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)