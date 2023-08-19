from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import redirect, render
from .form import UserRegistration
from django.contrib.auth.models import User
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from demo.settings import EMAIL_HOST_USER
# Create your views here.

def homepage(response):
    print(response)
    return render(response,'pages/home.html')

def search_contact(request):
    context = {}
    if request.method == 'POST':
        q = request.POST['query']

        if q:
            if q in "1234567890":
                result = Contact.objects.filter(mobile_no=q)
                if result.exists():
                    context ={
                        "Conatact" : result.mobile_no,
                        "Name" : result.username,
                        "message" : "It's a spam Conatact"if result.spam else "Safe Contact"
                    }
                else:
                    context = {
                       "message" : "Contact Not Exists" 
                    }
            else:
                result = Contact.objects.filter(username = q)
                if result.exists():
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
        #username = request.POST.get["username"]
        email = request.POST.get["email"]
        mobile_no = request.POST.get["mobile_no"]
        if  email and mobile_no:
            username = email.split('@')[0]
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
        #username = request.POST["username"]
        email = request.POST["email"]
        mobile = request.POST["mobile_no"]
        password = request.POST["password"]
        
        if  email and mobile and password:
            exist = Contact.objects.filter(mobile_no=mobile) 
            if not exist:
                username = email.split('@')[0]
                newUser = User.objects.create_user(username,email,password)
                try:
                    profile = Contact.objects.get(user=newUser)
                except Exception as e:
                    print(e)
                    profile = None
                if profile is None:
                    Contact.objects.create(user=newUser, mobile_no=mobile, username = username,  email_id=email).save()
                    messages.success(request, "Your Profile has been created successfully")
                    subject = "LeTyOuKnOw.com||Success of registration"
                    message = f"""This mail is from LeTyOuKnOw.com.
    You have successfully registered yourself with your {email} gmail account.
    HAVE NICE DAY!!! :)

                """
                    send_mail(subject,message,EMAIL_HOST_USER,[email])
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
        email  = request.POST.get('username')
        password = request.POST.get('password')

        if email and password: 
            username = email.split('@')[0]
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
        else:
             messages.error(request,"Add email and password") 
    
    return render(request,'pages/login.html')

def logoutuser(request):
    logout(request)
    messages.success(request,"You have successfully logout!")
    #return redirect("logout")
        
    return render(request,"pages/home.html")  

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        reset_pass = request.POST.get("password1")
        confirm_pass = request.POST.get("password2")
        if reset_pass == confirm_pass:
            username = email.split('@')[0]  
            exist = User.objects.filter(username = username)
            print(exist)
            if exist:
                user = User.objects.get(username = username)
                print(user)
                user.set_password(str(confirm_pass))
                user.save()
                
                
                messages.success(request,"Password is reset")
                subject = "LeTyOuKnOw.com||Success change password"
                message = f"""This mail is from LeTyOuKnOw.com.
You have successfully changed the password of gmail account {email}.
HAVE NICE DAY!!! :)

                """
                send_mail(subject,message,EMAIL_HOST_USER,[email])
                return redirect('login') 
            else:
                messages.error(request,"You don't have account")
                return  redirect('reset_password')

    return render(request,'pages/reset_pass.html') 
