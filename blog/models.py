from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class PostBlog(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField(default='')
    name = models.CharField(max_length=150, default= "")
    timestamp = models.DateTimeField(default = now)
    slug = models.CharField(max_length=130)

    id = models.AutoField(primary_key= True)

    def __str__(self):
        return self.name

class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email

class postComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostBlog, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default = now)
    sno = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self',  on_delete=models.CASCADE, null =True)
    postid = models.IntegerField(default=0)

    def __str__(self):
        return self.comment +"... by " +self.user.username 

# my_code earlier for slupost 
''' 
<div class="comments">
    <form action="{% url 'postComment' %}" method="post">
        {% csrf_token %}
        <h4>Comments ({{comments.count}})</h2>
            {% if user.is_authenticated %}

            <div class="form-group">
                <label for="post comment">Post Comment</label>
                <input type="text" name="comment" id="" placeholder="enter comment here" class="form-control">
                <input type="hidden" name="postid" value="{{post.id}}">
                <input type="hidden" name="parentSno" value="">
                <br>
                <input type="submit" value="submit" class="btn-success">
            </div>
    </form>
    <div class="row my-3">
        {% for comment in comments %}
        {% ifequal comment.postid post.id %}

        <div class="col-md-1 bg-primary my-1">Image here</div>
        <div class="col-md-11 bg-success my-1"><b>{{comment.user.username}} <span
                    class="badge badge-secondary">{{comment.timestamp| naturaltime}}</span></b>
            <div>{{comment.comment}}</div>
        </div>

        <div class="reply mx-0">
            {% if user.is_authenticated %}
            <button class="btn btn-success btn-sm" type="button" data-toggle="collapse"
                data-target="#replyBox{{comment.sno}}" aria-expanded="false" aria-controls="replyBox{{comment.sno}}">
                Reply
            </button>
            <div class="collapse" id="replyBox{{comment.sno}}">

                <div class="card card-body my-2">
                    <form action="{% url 'postComment' %}" method="post">
                        {% csrf_token %}
                        <div class="form-group">
                            <label for="comment">Post a Reply</label>
                            <input type="text" name="comment" id="" placeholder="post reply here" class="form-control">
                            <input type="hidden" name="parentSno" value="{{comment.sno}}">
                            <input type="hidden" name="postid" value="{{post.id}}">
                            <br>
                        </div>
                        <input type="submit" value="submit" class="btn-success">

                    </form>
                </div>
            </div>
            {%else%}

            <button class="btn btn-success btn-sm" type="button" data-toggle="collapse"
                data-target="#replyBox{{comment.sno}}" aria-expanded="false" aria-controls="replyBox{{comment.sno}}">
                Login to Reply
            </button>

            {%endif%}

            <div class="replies bg-danger my-2">
                {% for reply in replydict|get_val:comment.sno %}
                
                    {{reply.comment}}
                    <br>

                    {% endfor %}
                
            </div>
        </div>

        {% endifequal %}


        {% endfor %}
        {% else %}
        <h2> Log in to Comment</h2>
        {% endif %}
    </div>

</div>
{% endblock msg%}
'''