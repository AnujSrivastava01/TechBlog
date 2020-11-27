"""miniblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="blog/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="blog/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="blog/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="blog/password_reset_done.html"), 
        name="password_reset_complete"),

    path('admin/', admin.site.urls),
    path('',views.home),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('signup/',views.user_signup, name='signup'),
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('search',views.search, name='search'),
    path('addpost/', views.add_post, name='addpost'),
    path('updatepost/<int:id>/', views.update_post, name='updatepost'),
    path('deletepost/<int:id>/', views.delete_post, name='deletepost'),
    path('postComment/', views.postcomment, name="postComment"),
    path('<str:slug>/', views.blogpage, name="blogpage"),
    path('deletecomment/<int:sno>/', views.delete_comment, name='deletecomment'),
    path('deletereply/<int:sno>/', views.delete_reply, name='deletereply'),

    

    


 


]

