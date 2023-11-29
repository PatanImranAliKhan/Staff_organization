from django.shortcuts import render
from django.shortcuts import redirect
from .models import  Employee, Leave, Team, Certificate
from authenticate_app.models import Location, Country, Region

# Create your views here.

def AuthorizeEmployee(request):
    try:
        pro = request.session['profession']
        if(pro=="hr"):
            return redirect("hr_home")
        if(pro!="emp"):
            return redirect("login")
    except:
        return redirect("login")

def EmployeeHomePage(request):
    AuthorizeEmployee(request)
    return render(request, "emp_home.html")

def EmployeeProfile(request):
    try:
        email = request.session["email"]
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
            try: 
                emp.username = request.POST.get("username")
                emp.mobile=request.POST.get("mobile")
                emp.address=address
                emp.save()
                return render(request,"emp_profile.html", {"employee": emp, "success": "Saved the edited details"})
            except Exception as e:
                print("Exception ",e)
                return render(request,"emp_profile.html", {"employee": emp, "error": "Error while editing details, please try after some time"})
    
        return render(request,"emp_profile.html", {"employee": emp})
    except Exception as p:
        print(p)
        return render(request,"emp_profile.html", {"employee":{}, "jobroles": [], "departments": []})
    

def EmployeeLeaves(request):
    AuthorizeEmployee(request)
    email = request.session["email"]
    leaves = Leave.objects.filter(empEmail=email)
    try:
        if(request.method=="POST"):
            if "deleteId" in request.POST:
                print("Rmove")
                ler = Leave.objects.get(leaveId = request.POST.get("deleteId"))
                ler.delete()
            else:
                StartDate=request.POST.get("StartDate")
                EndDate=request.POST.get("EndDate")
                noOfHours = int(request.POST.get("NoOfHours"))
                if(noOfHours<0 or noOfHours>24):
                    return render(request, "emp_leaves.html", {"leaves": leaves, "error": "Invalid No.Of Hours"})
                if(EndDate <= StartDate):
                    return render(request, "emp_leaves.html", {"leaves": leaves, "error": "Start date and End date is invalid"})
                emp = Employee.objects.get(email=email)
                Leave.objects.create(LeaveType=request.POST.get("LeaveType"), NoOfHours=noOfHours, 
                                        EndDate=request.POST.get("EndDate"), StartDate=request.POST.get("StartDate"), empEmail=emp)
                return redirect("emp_leaves")
        return render(request,"emp_leaves.html", {"leaves": leaves})
    except Exception as e:
        print("Exception: ",e)
        return render(request,"emp_leaves.html",{"leaves":leaves})

def EmployeeCertificates(request):
    AuthorizeEmployee(request)
    email = request.session["email"]
    cert = Certificate.objects.filter(empEmail=email)
    try:
        if(request.method=="POST"):
            if "deleteId" in request.POST:
                print("Rmove")
                jbr = Certificate.objects.get(cirId = request.POST.get("deleteId"))
                jbr.delete()
            else:
                EarnDate=request.POST.get("EarnDate")
                Expdate=request.POST.get("Expdate")
                if(Expdate <= EarnDate):
                    return render(request, "emp_certificates.html",{"certificates": cert, "error":"Invalid Expire and Earn dates"})
                emp = Employee.objects.get(email=email)
                cr = Certificate.objects.create(CirTitle=request.POST.get("CirTitle"), Technology=request.POST.get("Technology"), 
                                        EarnDate=request.POST.get("EarnDate"), Expdate=request.POST.get("Expdate"), empEmail=emp)
                return redirect("emp_cetificate")
        return render(request, "emp_certificates.html",{"certificates": cert})
    except Exception as we:
        print(we)
        return render(request, "emp_certificates.html",{"certificates": cert})
