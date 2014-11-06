import os
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def upload_path(self, filename):

    return os.path.join('content/', self.user.username, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to=upload_path, blank=True)
    description = models.TextField(max_length=500)

    def __unicode__(self):
        return self.user.username

class Category(models.Model):
    category = models.CharField(max_length=120)

    def __unicode__(self):
        return self.category

class Notebook(models.Model):
    users = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=upload_path)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=20, blank=True)
    category = models.ForeignKey(Category)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return "/%s/%s/" % (self.user, self.slug)

    def __unicode__(self):
        return self.title



