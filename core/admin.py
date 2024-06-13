from django.contrib import admin
from .models import Profile,Post,Like

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_img', 'image', 'caption', 'created_at', 'posted_at')
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post,PostAdmin)
admin.site.register(Like)