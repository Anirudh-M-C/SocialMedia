from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone

User=get_user_model()

# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio= models.TextField(blank=True)
    profile_img= models.ImageField(upload_to='profile_imgages', default='blank-image.webp')
    header_img = models.ImageField(upload_to='header_images', default='timelineheader.jpg')
    location= models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='other')

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.CharField(max_length=100)
    profile_img=models.ForeignKey(Profile,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)
    posted_at=models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.user

class Like(models.Model):
    post_id=models.CharField(max_length=200)
    username=models.CharField(max_length=200)

    def __str__(self):
        return self.username
    

class Followerscount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=200)

    def __str__(self):
        return self.user

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img=models.ForeignKey(Profile,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
    

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Like'),
        (2, 'Comment'),
        (3, 'Follow')
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent')
    receiver = models.CharField(max_length=100)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}to {self.receiver}'