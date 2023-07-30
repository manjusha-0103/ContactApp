from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import redirect, render
from .form import UserRegistration
from django.contrib.auth.models import User
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def homepage(response):
    print(response)
    return render(response,'pages/home.html')

def result(request):
    context = {}
    if request.method == 'POST':
        q = request.POST['query']

        if q:
            if q in "1234567890":
                result = Contact.objects.filter(mobile_no=q)
                if result:
                    context ={
                        "Conatact" : result.mobile_no,
                        "Name" : result.username,
                        "message" : "It's a spam Conatact"if result.spam else "Safe Contact"
                    }
                else:
                    context = {
                       "message" : "Contact Not Exists" 
                    }

    return render(request,'pages/home.html',{"data" : context})

def addContacts(request):
    if request.method == "POST" :
        username = request.POST.get["username"]
        email = request.POST.get["email"]
        mobile_no = request.POST.get["mobile_no"]
        if username and email and mobile_no:
            if Contact.objects.filter(mobile_no=mobile_no):
                messages.error(request,"Phone number is allredy register")
            else:
                contact = Contact.objects.create(username=username,email_id =email,mobile_no = mobile_no)
                contact.save()
        else:
            print(request)  
        return redirect(request,'pages/components/addcontacts.html') 

def registeruser(request):
    print(len(request.POST))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        mobile = request.POST["mobile_no"]
        password = request.POST["password"]
        
        if username and email and mobile and password:
            exist = Contact.objects.filter(mobile_no=mobile) 
            if not exist:
                newUser = User.objects.create_user(username,email,password)
                try:
                    profile = Contact.objects.get(user=newUser)
                except Exception as e:
                    print(e)
                    profile = None
                if profile is None:
                    Contact.objects.create(user=newUser, mobile_no=mobile, username = username,  email_id=email).save()
                    messages.success(request, "Your Profile has been created successfully")
                    return redirect('login')
                else:
                    Contact.objects.filter(id=profile.id).update(user=newUser, mobile_no=mobile, username = username,  email_id=email)
                    return redirect('login')
            else:
                messages.error(request,"Phone Number is already register")
        else:
            print(request.POST)  
            user = UserRegistration()
            return redirect('register')
        
      
    return render(request,'pages/register.html')


def login_user(request):
    if request.method == "POST" :
        username  = request.POST.get('username')
        password = request.POST.get('password')
        print(username)

        _user = authenticate(username = username ,password = password)
        print(_user)
        if _user is not None :
            login(request,_user)
            messages.success(request,"You have logged in successfully .......")
            return redirect('home')
        else :
            messages.error(request,"Wrong credentials")    
            return redirect('login')
    
    return render(request,'pages/login.html')

def logoutuser(request):
    logout(request)
    messages.success(request,"You have successfully logout!")
    #return redirect("logout")
        
    return render(request,"pages/home.html")    
