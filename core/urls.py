from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name="logout"),
    path('follow/',views.follow,name="follow"),
    path('settings/',views.settings,name="settings"),
    path('uploads/',views.uploads,name="uploads"),
    path('edit_uploads/<str:pk>/',views.edit_uploads,name="edit_uploads"),
    path('delete_uploads/<str:pk>/',views.delete_uploads,name="delete_uploads"),
    path('like-post/',views.like_post,name="like-post"),
    path('profile/<pk>',views.profile,name='profile')
]
