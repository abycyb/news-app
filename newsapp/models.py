
import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):    
    ROLE_CHOICES = [
        ('OWNER', 'owner'),
        ('SUPERVISOR', 'supervisor'),
        ('USER', 'user'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    role = models.CharField(max_length = 10, choices=ROLE_CHOICES, default='USER')
    image = models.ImageField(upload_to='userimg', blank=True, null=True, default=None)      

    def __str__(self):
        return self.user.username
    

class News(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    title = models.CharField(max_length=150,blank=True)
    image = models.FileField(upload_to='newsimg',blank=True, null=True, default=None)
    description = models.CharField(max_length=2000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30,blank=True)
    # news_id = models.IntegerField()
    voted_users = models.ManyToManyField(User, related_name='voted_news', blank=True)
    
    class Meta:
        unique_together = ('user', 'id',)

    def __str__(self):
        return self.title

    def short_description(self):
        return ' '.join(self.description.split()[:26])

    def voted_user_num(self):
        return self.voted_users.count()


class Interacted_News(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    news_id = models.IntegerField()
    interacted_users = models.ManyToManyField(User, blank=True)

    def int_user_num(self):
        return self.interacted_users.count()


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    news_comment = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    voted_comment = models.ManyToManyField(User, related_name='voted_comment', blank=True)
    image = models.FileField(upload_to='comment_img',blank=True, null=True, default=None)

    def __str__(self):
        return self.content
        # return self.news_comment.title,'>>', ' '.join(self.content.split()[:6])
    def comment_votes(self):
        return self.voted_comment.count()

    


class New_Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    news_comment = models.ForeignKey(Interacted_News, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    voted_comment = models.ManyToManyField(User, blank=True)
    image = models.FileField(upload_to='comment_img',blank=True, null=True, default=None)

    def __str__(self):
        return self.content
        # return self.news_comment.title,'>>', ' '.join(self.content.split()[:6])
    def comment_votes(self):
        return self.voted_comment.count()

    def file_extension(self):
        if self.image:
            filename = self.image.url
            file_extension = os.path.splitext(filename)[1]
            return file_extension
        return ''    


class Subcomment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    #     return self.comment.news_comment.title,'>>', ' '.join(self.comment.content.split()[:6]) , self.content.split()[:3]
        return self.content
    

class New_Subcomment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(New_Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='sub_comment_img',blank=True, null=True, default=None)

    def __str__(self):
    #     return self.comment.news_comment.title,'>>', ' '.join(self.comment.content.split()[:6]) , self.content.split()[:3]
        return self.content    
    
    def file_sub_extension(self):
        if self.image:
            filename = self.image.url
            file_extension = os.path.splitext(filename)[1]
            return file_extension
        return ''  