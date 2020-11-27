from django.contrib import admin
from .models import PostBlog, postComment, Contact
# Register your models here.

@admin.register(PostBlog)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug', 'timestamp','title', 'desc']


admin.site.register(Contact)

@admin.register(postComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['sno','postid', 'comment', 'timestamp', 'user', 'parent', 'post']
    