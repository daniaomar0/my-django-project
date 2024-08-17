from django.db import models
from django.contrib.auth.models import User
# Create your models here.

bg_choices=(
    ("1","Beginner"),
    ("2","Intermediate"),
    ("3","Advance"),
)
learn1=(
    ("1","None"),
    ("2","None")
)
    
    
class Step1(models.Model):
    background_knowledge = models.CharField(max_length=100,choices=bg_choices)
    speciality_target = models.CharField(max_length=100,choices=learn1)
    learn_target=models.CharField(max_length=100,choices=learn1)
    

    
class Step2(models.Model):
    current_level = models.CharField(max_length=100,choices=bg_choices)
    age = models.IntegerField()
    tell_us_about_yourself = models.CharField(max_length=200)

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    
class Booking(models.Model):
   first_name = models.CharField(max_length=200)    
   last_name = models.CharField(max_length=200)
   def __str__(self):
      return self.first_name + ' ' + self.last_name


class Course(models.Model):
   name = models.CharField(max_length=200) 
   instructor = models.CharField(max_length=200) 
   price=models.IntegerField(default=50)
   course_description = models.TextField(max_length=1000, default='') 
   image = models.ImageField(upload_to='images/')
   

   def __str__(self):
      return self.name