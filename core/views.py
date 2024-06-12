from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,login,logout as authlogout,authenticate
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

User=get_user_model()

# Create your views here.

@login_required(login_url='signin')
def index(request):
    context={
        'a':''
    }
    return render(request,'index.html',context)

def signup(request):
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already used")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"username already exists")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                #log user in and direct to settings 
                user_login=authenticate(username=username,password=password1)
                login(request,user_login)
                #create a profile object for the new user
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'password not matching')
            return redirect ('signup')
    else:
        return render(request,'signup.html')

def signin(request):
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
    return render(request,'signin.html')

@login_required(login_url='signin')
def logout(request):
    authlogout(request)
    return redirect('signin')

def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.POST:
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        
        # Check if a new image was uploaded
        if request.FILES.get('profile_img') is None:
            image = user_profile.profile_img
            user_profile.profile_img = image
        else:
            image = request.FILES.get('profile_img')
            user_profile.profile_img = image
        
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        return redirect('settings')
    return render(request,'setting.html',{'user_profile':user_profile})