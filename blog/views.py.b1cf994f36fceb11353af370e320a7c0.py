from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm, LoginForm, Postform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post, postComment, User
from django.contrib.auth.models import Group

# Home
def home(request):
    posts = Post.objects.all()
    comments = postComment.objects.all()
    return render(request, 'blog/home.html', {'posts':posts, 'comments':comments})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        gps = user.groups.all()

        if user.is_superuser:
            posts = Post.objects.all()
             full_name = user.name()
              print(full_name)
            
            return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps, 'user':user})
        else:
            posts = Post.objects.filter(name=user)
            full_name = user.get_full_name()
            return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps, 'user':user})
    else:
        return HttpResponseRedirect('/login/')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations! you have become an author")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
   
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc, name= request.user)
                pst.save()
                form = Postform()
        else:
            form = Postform()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('login')
    
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def postcomment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = request.POST.get("comment")
            user = request.user
            sno = request.POST.get("sno")
            post = Post.objects.get(id=sno)
            comment = postComment(comment= comment, user = user, post =post)
            comment.save()
            messages.success(request, "commented succesfully")
    
    return redirect('/')
