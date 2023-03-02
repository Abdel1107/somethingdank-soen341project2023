from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    degree = models.CharField(max_length=100)
    school = models.CharField(max_length=150)
    skills = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)

    def __str__(self):
        return self.user.username
