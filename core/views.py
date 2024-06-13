from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model,login,logout as authlogout,authenticate
from django.contrib import messages
from .models import Profile,Post,Like
from django.contrib.auth.decorators import login_required

User=get_user_model()

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_profile=Profile.objects.get(user=request.user)
    posts=Post.objects.all()
    context={
        'user_profile':user_profile,
        'posts':posts
    }
    return render(request,'index.html',context)


@login_required(login_url='signin')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_post_length=len(user_posts)
    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length
    }
    return render(request,'profile.html',context)


@login_required(login_url='signin')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post=Post.objects.get(id=post_id)
    like_filter=Like.objects.filter(post_id=post_id,username=username).first()
    if like_filter:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')
    else:
        new_like=Like.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def uploads(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        # Fetch the user's profile
        user_profile = Profile.objects.get(user=request.user)
        
        # Create a new post with the user's profile image and the uploaded image
        new_post = Post.objects.create(user=user, profile_img=user_profile, image=image, caption=caption)
        new_post.save()
        
        return redirect('/')
    else:
        return redirect('/')


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


@login_required(login_url='signin')
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
        
        return redirect('/')
    return render(request,'setting.html',{'user_profile':user_profile})