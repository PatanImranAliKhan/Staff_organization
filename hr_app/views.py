from django.shortcuts import render
from django.shortcuts import redirect
from authenticate_app.models import Region, Country, Location
from employee_app.forms import EmployeeForm
from employee_app.models import Employee, Department, Team, Leave, JobRole, Project

# Create your views here.

def AuthorizeHR(request):
    try:
        pro = request.session['profession']
        if(pro=="emp"):
            return redirect("emp_home")
        if(pro!="hr"):
            return redirect("login")
    except:
        return redirect("login")

def Hr_HomePage(request):
    AuthorizeHR(request)
    return render(request, "hr_home.html")

def EmployeesList(request):
    AuthorizeHR(request)
    try:
        if(request.method=="POST"):
            emp = Employee.objects.get(email = request.POST.get("deleteId"))
            emp.delete()
        employees = Employee.objects.all()
        return render(request,"employees_list.html", {"employees":employees})
    except: 
        return render(request,"employees_list.html", {"employees": []})
    
def AddEmployee(request):
    AuthorizeHR(request)
    try:
        jobroles = JobRole.objects.all()
        departments = Department.objects.all()
        teams=Team.objects.all()
        managers=Employee.objects.filter(is_manager=True)
        if request.method=="POST":
            print("post: ", request.POST)
            reg = Region(regName=request.POST.get("regName"))
            reg.save()
            con = Country(conName=request.POST.get("conName"), regId = reg)
            con.save()
            address = Location(
                city = request.POST.get("city"),
                state= request.POST.get("state"),
                zipcode= request.POST.get("zipcode"),
                conid = con 
            )
            address.save()
            jobr = JobRole.objects.get(jobRole= request.POST.get("jobRole"))
            dept = Department.objects.get(deptName= request.POST.get("department"))

            m=request.POST.get("manager")
            t=request.POST.get("team")
            managerDetails=None
            teamDetails=None
            if(m!="") :
                managerDetails=Employee.objects.get(email=m)

            if(t!="") :
                teamDetails=Team.objects.get(teamName=t)
        
            reqdata = {
                "firstname": request.POST.get("firstname"),
                "lastname": request.POST.get("lastname"),
                "dob":request.POST.get("dob"),
                "email": request.POST.get("email"),
                "mobile": request.POST.get("mobile"),
                "location": address,
                "password": request.POST.get("username"),
                "is_manager": True if request.POST.get("is_manager")=="on" else False,
                "hr_details": request.session['email'],
                "jobRole": jobr,
                "department": dept,
                "manager":managerDetails,
                "team": teamDetails
            }
            
            emp_form = EmployeeForm(reqdata)
            if emp_form.is_valid():
                emp_form.save()
                return render(request,"add_employee.html", { "jobroles": jobroles, "departments": departments,
                                                            "teams":teams, "managers":managers,
                                                            "success": "Successfully Added Employee" })
        return render(request,"add_employee.html", { "jobroles": jobroles, "departments": departments, "teams":teams, "managers":managers })
    except Exception as addE:
        print("Exception at Adding EMployees")
        print(addE)
        return render(request,"add_employee.html", { "jobroles": [], "departments": [],"managers":[], "teams":[],
                                                    "error":"unexpected Occur Occured please try after some time" })

def EditEmployee(request, info, email):
    AuthorizeHR(request)
    try:
        jobroles = JobRole.objects.all()
        departments = Department.objects.all()
        emp = Employee.objects.get(email=email)
        if request.method=="POST":
            flag1,flag2,flag3,flag4=False, False, False, False
            reg = Region(regName=request.POST.get("regName"))
            if(emp.address.conid.regId.regName != request.POST.get("regName")) :
                flag1=True
                reg.save()
            else:
                reg = Region.objects.filter(regName=request.POST.get("regName"))[0]
            con = Country(conName=request.POST.get("conName"), regId = reg)
            if(emp.address.conid.conName != request.POST.get("conName") or flag1) :
                flag2=True
                con.save()
            else:
                con = Country.objects.filter(conName = request.POST.get("conName"))[0]
            address = Location(
                city = request.POST.get("city"),
                state= request.POST.get("state"),
                zipcode= request.POST.get("zipcode"),
                conid = con 
            )
            if(emp.address.city != request.POST.get("city") or emp.address.state!=request.POST.get("state") or 
               emp.address.zipcode!=request.POST.get("zipcode") or flag2) :
                address.save()
            else: 
                address=Location.objects.filter(city = request.POST.get("city"),state = request.POST.get("state"),
                                             zipcode= request.POST.get("zipcode"))[0]
            jobr = JobRole.objects.get(jobRole= emp.jobRole)
            if(request.POST.get("jobRole")!="") :
                jobr = JobRole.objects.get(jobRole= request.POST.get("jobRole"))
            dept = Department.objects.get(deptName= emp.department)
            if(request.POST.get("department")!=""):
                dept = Department.objects.get(deptName= request.POST.get("department"))
            try: 
                emp.firstname = request.POST.get("firstname")
                emp.lastname = request.POST.get("lastname")
                emp.dob = request.POST.get("dob")
                emp.mobile=request.POST.get("mobile")
                emp.location=address
                emp.is_manager=True if request.POST.get("is_manager")=="on" else False
                emp.jobRole=jobr
                emp.department=dept
                emp.save()
                print("saved")
                return render(request,"editEmployee.html", {"employee": emp, "jobroles": jobroles, "departments": departments,
                                                            "success": "Saved the edited details"})
            except Exception as e:
                print("Exception ",e)
                return render(request,"editEmployee.html", {"employee": emp, "jobroles": jobroles, "departments": departments,
                                                            "error": "Error while editing details, please try after some time"})
    
        return render(request,"editEmployee.html", {"employee": emp, "jobroles": jobroles, "departments": departments})
    except:
        return render(request,"editEmployee.html", {"employee":{}, "jobroles": [], "departments": []})
    

def JobRolesPage(request):
    AuthorizeHR(request)
    try:
        if(request.method=="POST"):
            if "editDetails" in request.POST:
                print("edit : ", request.POST.get("editDetails"))

                jbe = JobRole.objects.get(jobId = request.POST.get("editDetails"))
                jbe.jobRole = request.POST.get("jobRole")
                jbe.JobLevel = request.POST.get("JobLevel")
                jbe.salary = request.POST.get("salary")
                jbe.save()
            elif "deleteId" in request.POST:
                jbr = JobRole.objects.get(jobId = request.POST.get("deleteId"))
                jbr.delete()
            else:
                jb = JobRole.objects.create(jobRole=request.POST.get("jobRole"), JobLevel=request.POST.get("JobLevel"), 
                                        salary=request.POST.get("salary"))
        jb = JobRole.objects.all()
        return render(request,"JobRoles.html", {"job_roles": jb})
    except:
        return render(request,"JobRoles.html", {"job_roles": []})
    

def TeamsPage(request):
    AuthorizeHR(request)
    try:
        if(request.method=="POST"):
            if "editDetails" in request.POST:
                teame = Team.objects.get(teamId = request.POST.get("editDetails"))
                manE = Employee.objects.get(email = request.POST.get("manager"))
                dept = Department.objects.get(deptName = request.POST.get("department"))
                teame.teamName = request.POST.get("teamName")
                teame.manager = manE
                teame.department = dept
                teame.save()
            elif "deleteId" in request.POST:
                temr = Team.objects.get(teamId = request.POST.get("deleteId"))
                temr.delete()
            else:
                print(request.POST.get("teamName"), request.POST.get("manager"), request.POST.get("department"))
                manE = Employee.objects.get(email = request.POST.get("manager"))
                dept = Department.objects.get(deptName = request.POST.get("department"))
                t=Team(teamName=request.POST.get("teamName"), manager=manE, department=dept)
                t.save()
                print(t, "helo")
        teams = Team.objects.all()
        departments = Department.objects.all()
        managers = Employee.objects.filter(is_manager=True)
        print(departments, managers, teams)
        return render(request, "Teams.html", {"teams": teams, "departments": departments, "managers": managers })
    except:
        return render(request, "Teams.html", {"teams": [], "departments": [], "managers": [] })
    
def LeaveRequestsPage(request):
    AuthorizeHR(request)
    try:
        if(request.method=="POST"):
            print(request.POST)
            le = Leave.objects.get(leaveId=request.POST.get("changeId"))
            status = request.POST.get("status")
            if(status!=""):
                le.status = request.POST.get("status")
                le.save()
        leaves = Leave.objects.filter(status="pending")
        return render(request, "LeaveRequests.html", {"leaves": leaves})
    except:
        return render(request, "LeaveRequests.html", {"leaves": []})
    
def AddDepartmentPage(request):
    if( request.method == "POST"):
        dep = Department(deptId=request.POST.get("deptId"), deptName=request.POST.get("deptName"))
        dep.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    
def DepartmentsPage(request):
    AuthorizeHR(request)
    try:
        if(request.method=="POST"):
            if "editDetails" in request.POST:
                depte = Department.objects.get(deptId = request.POST.get("editDetails"))
                depte.deptName = request.POST.get("deptName")
                depte.save()
            elif "deleteId" in request.POST:
                deptr = Department.objects.get(deptId = request.POST.get("deleteId"))
                deptr.delete()
            else:
                Department.objects.create(deptId=request.POST.get("deptId"), deptName=request.POST.get("deptName"))
        depts = Department.objects.all()
        return render(request,"Departments.html", {"departments": depts})
    except:
        return render(request,"Departments.html", {"departments": []})
    

def HandleProjectsPage(request):
    AuthorizeHR(request)
    return render(request,"HandleProjects.html")