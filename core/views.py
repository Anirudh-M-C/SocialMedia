from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model,login,logout as authlogout,authenticate
from django.contrib import messages
from .models import Profile,Post,Like,Followerscount,Comment,Notification
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from datetime import timedelta



User=get_user_model()

# Create your views here.

@login_required(login_url='signin')
def index(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by('-date')
    user_profile=Profile.objects.get(user=request.user)
    unread_notifications = notifications.filter(is_read=False).exists()
    posts=Post.objects.all()
    for notification in notifications:
        notification.adjusted_date = notification.date + timedelta(hours=5, minutes=30)
        notification.sender_profile_img = Profile.objects.get(user=notification.sender).profile_img

    #user suggestion
    all_profile=Profile.objects.all()

    context={
        'user_profile':user_profile,
        'posts':posts,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'all_profile':all_profile,

    }
    return render(request,'index.html',context)


@login_required(login_url='signin')
def search(request):
    profile=Profile.objects.get(user=request.user)
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    if request.POST:
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)

        username_profile=[]
        username_profile_list=[]

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list=list(chain(*username_profile_list))
    context={'profile':profile,
             'username_profile':username_profile,
            'username_profile_list': username_profile_list,
            'user_profile':user_profile,
             }

    return render(request,'search.html',context)


@login_required(login_url='signin')
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment')
        user = request.user
        user_profile = Profile.objects.get(user=request.user)
        p=Post.objects.get(id=post_id)
        post = Post.objects.filter(id=post_id).first()
        if post:
            comment = Comment.objects.create(post=post, user=user, content=comment_text, profile_img=user_profile, created_at=timezone.now())
            comment.save()

            # notification
            print(f"Post user type: {type(post.user)}, value: {post.user}")
            Notification.objects.create(
                sender=user,
                receiver=p.user,
                notification_type=2,
                text_preview=comment_text,
                date=timezone.now(),
                is_read=False
            )

            return redirect('/')  # Redirect to the homepage after adding comment

    return redirect('/') 




@login_required(login_url='signin')
def profile(request,pk):
    user_p=Profile.objects.get(user=request.user)
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)

    user_post_length=len(user_posts)
    follower=request.user.username
    user=pk
    if Followerscount.objects.filter(follower=follower,user=user).exists():
        button_text='unfollow'
    else:
        button_text='follow'
    
    user_followers=len(Followerscount.objects.filter(user=pk))
    user_following=len(Followerscount.objects.filter(follower=pk))
    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'user_p':user_p,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
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


        Notification.objects.create(
            sender=request.user,
            receiver=post.user,
            notification_type=1,
            text_preview='',
            date=timezone.now()
        )
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
    

@login_required(login_url='signin')
def edit_uploads(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        # Update existing post with form data
        post.caption = request.POST['caption']
        if 'image_upload' in request.FILES:
            post.image = request.FILES['image_upload']
        post.save()
        
        return redirect('/')
    
    return render(request, 'edit_uploads.html', {'post': post})
    

@login_required(login_url='signin')
def delete_uploads(request,pk):
    post=Post.objects.get(pk=pk)
    post.delete()
    return redirect('/')
    

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.POST:
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        
         # Update profile image if a new one is uploaded
        if request.FILES.get('profile_img'):
            user_profile.profile_img = request.FILES.get('profile_img')
        
        # Update header image if a new one is uploaded
        if request.FILES.get('header_img'):
            user_profile.header_img = request.FILES.get('header_img')
        
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        return redirect('/')
    return render(request,'setting.html',{'user_profile':user_profile})



@login_required(login_url='signin')
def follow(request):
    if request.POST:
        follower=request.POST['follower']
        user=request.POST['user']

        if Followerscount.objects.filter(follower=follower,user=user).exists():
            delete_follower=Followerscount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=Followerscount.objects.create(follower=follower,user=user)
            new_follower.save()

            Notification.objects.create(
                sender=User.objects.get(username=follower),
                receiver=User.objects.get(username=user),
                notification_type=3,
                text_preview='',
                date=timezone.now()
            )
            return redirect('/profile/'+user)
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
