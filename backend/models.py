# from operator import mod
# from pyexpat import model
# from re import T
# from tkinter import N
from re import T
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
import uuid
from django.dispatch import receiver
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
import random
import os
from django.dispatch import receiver
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage
import os
from django.dispatch import receiver
from ckeditor.fields import RichTextField
import cloudinary







class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, username, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)
    




class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', max_length=15, unique=True, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def get_absolute_url(self):
        return redirect("datapage")
    
    
    
    
    
# Create your models here.
class About(models.Model):
    about_title = models.CharField(max_length=2000, blank = True)
    about_description = models.CharField(max_length=2000, blank = True)
    about_img = models.ImageField(upload_to='Ishika/About/', storage=MediaCloudinaryStorage())
    about_from = models.CharField(max_length=2000, blank = True)
    about_lives_in = models.CharField(max_length=2000, blank = True)
    about_birth_date = models.DateField(max_length=100)
    current = models.BooleanField(default = True)
    
    def __str__(self):
        return self.about_title
    
    class Meta:
        ordering = ('-id', )
    

     
class Category(models.Model):
    category_name = models.CharField(max_length=2000, blank = True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        ordering = ('-id', )
   
   
   
def upload_path_projects(instance, filename):
    return "Ishika/Project/{0}".format(instance.project_title)
class Projects(models.Model):
    project_title = models.CharField(max_length=2000, blank = True)
    project_description = models.CharField(max_length=2000, blank = True)
    project_img = models.ImageField(upload_to=upload_path_projects, storage=MediaCloudinaryStorage())
    project_category =  models.ForeignKey(Category, related_name="project_category", on_delete=models.CASCADE, blank=True)
    
    
    def __str__(self):
        return self.project_title[:10]
    
    class Meta:
        ordering = ('-id', )



class BackgroundImages(models.Model):
    bg_image_main = models.ImageField(upload_to="Ishika/Background Images/", storage=MediaCloudinaryStorage())
    bg_image_sec = models.ImageField(upload_to="Ishika/Background Images/", storage=MediaCloudinaryStorage())
    current = models.BooleanField(default = True)
    
    
    
    
    
class Skill(models.Model):
    skill_name = models.CharField(max_length = 2000, blank = True)
    skill_percentage = models.CharField(max_length = 3, blank = True)
    
    def __str__(self):
        return self.skill_name
    
    class Meta:
        ordering = ('-id', )
        
        
        
class Experience(models.Model):
    experience_company = models.CharField(max_length = 2000, blank = True)
    experience_duration = models.CharField(max_length = 2000, blank = True)
    experience_year = models.CharField(max_length = 2000, blank=True, null=True)
    experience_details = RichTextField(max_length = 2000, blank=True, null=True)
    
    def __str__(self):
        return self.experience_company + self.experience_year + self.experience_company
    
    class Meta:
        ordering = ('-experience_year', '-id')
        
        
        
class Education(models.Model):
    education_course = models.CharField(max_length = 2000, blank = True)
    education_university = models.CharField(max_length = 2000, blank = True)
    education_year = models.CharField(max_length = 2000, blank=True, null=True)
    education_marks = models.CharField(max_length = 2000, blank=True, null=True)
    
    def __str__(self):
        return self.education_course
    
    class Meta:
        ordering = ('-education_year', )
        
        
class Link(models.Model):
    link_name = models.CharField(max_length = 2000, blank = True)
    link_url = models.URLField(max_length = 20000)
    
    def __str__(self):
        return self.link_name
    
    class Meta:
        ordering = ('-id', )
        
    
class Contact(models.Model):
    contact_name = models.CharField(max_length=50, blank = True)
    contact_email = models.CharField(max_length=70, blank = True)
    contact_subject = models.CharField(max_length=70, blank = True)
    contact_description = models.CharField(max_length=5000, blank = True)
    contact_replied = models.BooleanField(default = False)

    def __str__(self):
        return self.contact_email
    
    class Meta:
        ordering = ('-id', )
        
        
class ClientsStats(models.Model):
    clients_total = models.CharField(max_length=10, blank = True)
    clients_project_complete = models.CharField(max_length=10, blank = True)
    clients_project_ongoing = models.CharField(max_length=10, blank = True)
    clients_satisfaction = models.CharField(max_length=10, blank = True)
    clients_current = models.BooleanField(default = True)

    def __str__(self):
        return self.clients_total
    
    class Meta:
        ordering = ('-id', )


class CVResume(models.Model):
    cvresume_name = models.CharField(max_length=2000, blank=True)
    cvresume_file = models.FileField(upload_to="Ishika/CVResume/", storage=RawMediaCloudinaryStorage(), max_length=5000)
    current = models.BooleanField(default = True)


    def __str__(self):
        return self.cvresume_name
    
    class Meta:
        ordering = ('-id', )


class Services(models.Model):
    service_heading = models.CharField(max_length=1000, blank=True, null=True)
    service_description = models.CharField(max_length=1000, blank=True, null=True)
    service_icon = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self):
        return self.service_heading
    
    class Meta:
        ordering = ('id',)


class ContactDetails(models.Model):
    contact_address = models.CharField(max_length=1000, blank=True, null=True)
    contact_email = models.CharField(max_length=1000, blank=True, null=True)
    contact_number = models.CharField(max_length=10, blank=True, null=True)
    current = models.BooleanField(default = True)

    def __str__(self):
        return self.contact_number
    
    class Meta:
        ordering = ('id',)
