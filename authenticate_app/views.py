from django.shortcuts import render
from django.shortcuts import redirect
from hr_app.forms import HRForm
from hr_app.models import HR
from employee_app.models import Employee
from .models import Location, Country, Region

# Create your views here.

def CheckData(request):
    try:
        pro=request.session['profession']
        if(pro=="emp"):
            print("employe")
            return redirect("emp_home")
        elif pro=="hr":
            print("hr")
            return redirect("hr_home")
        return pro
    except:
        return None
    return None

def HomePage(request):
    return render(request,'home.html')

def LoginPage(request):
    if request.method=="POST":
        try:
            category = request.POST.get("category")
            if(category==None):
                return render(request,'login.html',{'error':'Please select the category'})
            email = request.POST.get("email")
            password = request.POST.get("password")
            if category == "employee":
                try: 
                    emp_data = Employee.objects.get(email=email, password=password)
                    if(emp_data==None) :
                        return render(request,"login.html",{"error": "Unexpected error occured please try login after some time"})
                    request.session['username']=emp_data.username
                    request.session['email']=emp_data.email
                    request.session['profession']="emp"
                    return redirect("emp_home")
                except:
                    return render(request,"login.html",{"error": "Invalid Email or Password"})
            else :
                try: 
                    hr_data = HR.objects.get(email=email, password=password)
                    if(hr_data==None) :
                        return render(request,"login.html",{"error": "Unexpected error occured please try login after some time"})
                    request.session['username']=hr_data.username
                    request.session['email']=hr_data.email
                    request.session['profession']="hr"
                    return redirect("hr_home")
                except:
                    return render(request,"login.html",{"error": "Invalid Email or Password"})
        except:
            return render(request,"login.html",{"error": "Unexpected error occured please try login after some time"})
    return render(request,"login.html")

def Registration(request):
    if(request.method=="POST"):
        try:
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
            reqdata = {
                "username": request.POST.get("username"),
                "email": request.POST.get("email"),
                "mobile": request.POST.get("mobile"),
                "address": address,
                "password": request.POST.get("password")
            }
            hr_form = HRForm(reqdata)
            if hr_form.is_valid():
                hr_form.save()
                return redirect("login")
        except:
            return render(request,"register.html", {"error": "Some Error occured Please try after some time"})
    return render(request,"register.html")

def Logout(request):
    try:
        del request.session['username']
        del request.session['email']
        del request.session['profession']
        return redirect('login')
    except:
        return redirect('login')