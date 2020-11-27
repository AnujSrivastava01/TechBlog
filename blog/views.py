from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpForm, LoginForm, Postform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import PostBlog, User, postComment, Contact
from django.contrib.auth.models import Group
from blog.templatetags import extras


def home(request):
    posts = PostBlog.objects.all()
    comments = postComment.objects.filter( parent=None)
    replies = postComment.objects.filter().exclude(parent=None)
    replydict = {}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]= [reply]
        else:
            replydict[reply.parent.sno].append(reply)
    return render(request, 'blog/home.html', {'posts':posts,  'comments':comments, 'replydict':replydict})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        contact=Contact(name=name, email=email, phone=phone, content=content)
        contact.save()

    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        
        if user.is_superuser:
            posts = PostBlog.objects.all()
            full_name = user
            return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':'Admin', 'user':user})
        else:
            posts = PostBlog.objects.filter(name=user)
            full_name = user.get_full_name()
            gps = user.groups.all()
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
                slug = title.split()[0]
                pst = PostBlog(title=title, desc=desc, name= request.user, slug = slug)
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
            pi = PostBlog.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                
        else:
            pi = PostBlog.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = PostBlog.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def postcomment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = request.POST.get("comment")
            user = request.user
            postid = request.POST.get("postid")
            post = PostBlog.objects.get(id = postid)
            parentSno = request.POST.get("parentSno")
            
            if parentSno is "":
                comment = postComment(comment= comment, user = user, post =post, postid = postid)

            else:
                parent =postComment.objects.get(sno= parentSno)
                comment = postComment(comment= comment, user = user, post =post, postid = postid, parent = parent)
               
            
            comment.save()
          
    
    return redirect(f'/{post.slug}/')

def blogpage(request, slug):
    post = PostBlog.objects.filter(slug= slug).first()
    comments = postComment.objects.filter(post=post, parent=None)
    replies = postComment.objects.filter().exclude(parent=None)
    replydict = {}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]= [reply]
        else:
            replydict[reply.parent.sno].append(reply)
    
    replyusername = str(request.user )
    
    return render(request, 'blog/slugpage.html', {'post':post,  'comments':comments,'user':request.user , 'replydict':replydict, 'replyusername':replyusername})


def delete_comment(request, sno):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = postComment.objects.get(pk=sno)
            pi.delete()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')

def delete_reply(request, sno):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = postComment.objects.get(pk=sno)
            pi.delete()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=PostBlog.objects.none()
    else:
        allPostsTitle= PostBlog.objects.filter(title__icontains=query)
        allPostsAuthor= PostBlog.objects.filter(name__icontains=query)
        allPostsContent =PostBlog.objects.filter(desc__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'blog/search.html', params)