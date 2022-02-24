from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import *
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _








class EditAboutProfile(forms.ModelForm):
    
    about_title = forms.CharField(max_length = 2000, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }),
                                 )
    
    about_description = forms.CharField(max_length = 2000, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }),
                                 )
    about_from = forms.CharField(max_length = 2000, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }),
                                 )
    about_lives_in = forms.CharField(max_length = 2000, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }),
                                 )
    
    about_birth_date = forms.DateField(required=False, 
                                 widget = forms.DateInput(
                                     attrs={
                                         'class': 'form-control',
                                         'type': 'date'
                                         }),
                                 )
    about_img = forms.ImageField()
    
    class Meta:
        model = About
        fields = ('about_title', 'about_description', 'about_img', 'about_from', 'about_lives_in','about_birth_date')



class EditCVResumeProfile(forms.ModelForm):
    
    cvresume_name = forms.CharField(max_length = 2000, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }),
                                 )
    
     
    
    class Meta:
        model = CVResume
        fields = ('cvresume_name', 'cvresume_file')

        
        
        
        
class EditBGImageProfile(forms.ModelForm):
    
    bg_image_main = forms.ImageField()
    bg_image_sec = forms.ImageField()
    
    class Meta:
        model = BackgroundImages
        fields = ('bg_image_main', 'bg_image_sec')
        
        

class EditSkillProfile(forms.ModelForm):
    skill_name = forms.CharField(max_length = 2000, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Skill"
                                 )
    skill_percentage = forms.CharField(max_length = 2, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Percentage"
                                 )
    
    class Meta:
        model = Skill
        fields = ('skill_name', 'skill_percentage')
    
    


class EditProjectProfile(forms.ModelForm):
    project_title = forms.CharField(max_length = 200, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Project")
    project_description = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Details")
    project_img = forms.ImageField()
    
    class Meta:
        model = Projects
        fields = ('project_title', 'project_description', 'project_img', 'project_category')
        
        def __init__(self, *args, **kwargs):
            super(EditProjectProfile, self).__init__(*args, **kwargs)
            self.fields['project_category']=forms.ModelChoiceField(queryset=Category.objects.all())
        
        



class EditCategoryProfile(forms.ModelForm):
    category_name = forms.CharField(max_length = 20, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Category"
                                 )
    
    class Meta:
        model = Category
        fields = ('category_name',)




class EditExperienceProfile(forms.ModelForm):
    experience_company = forms.CharField(max_length = 200, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Company"
                                 )
    experience_duration = forms.CharField(max_length = 200, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'April 2021 - June 2022',
                                         }), label="Duration"
                                 )

    # experience_year = forms.CharField(max_length = 200, 
    #                              widget = forms.TextInput(
    #                                  attrs={
    #                                      'class': 'form-control',
    #                                      'placeholder': '2022',
    #                                      }), label="Year"
    #                              )

    
    class Meta:
        model = Experience
        fields = ('experience_company','experience_duration', 'experience_details')






class EditEducationProfile(forms.ModelForm):
    education_course = forms.CharField(max_length = 200, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Course"
                                 )

    education_university = forms.CharField(max_length = 200, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="University"
                                 )

    education_year = forms.CharField(max_length = 200, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Year"
                                 )
    education_marks = forms.CharField(max_length = 200, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Marks"
                                )
    
    class Meta:
        model = Education
        fields = ('education_course', 'education_university','education_year', 'education_marks')


class EditLinkProfile(forms.ModelForm):
    link_name = forms.CharField(max_length = 200, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Name")
    link_url = forms.URLField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="URL")
    
    class Meta:
        model = Link
        fields = ('link_name', 'link_url')




class EditServicesProfile(forms.ModelForm):
    service_heading = forms.CharField(max_length = 200, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Heading")

    service_description = forms.CharField(max_length = 2000, required=False, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Description")

    service_icon = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Icon")
    
    class Meta:
        model = Services
        fields = ('service_heading', 'service_description', 'service_icon')





class EditContactDetailsProfile(forms.ModelForm):
    contact_address = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Address")

    contact_email = forms.CharField(max_length = 2000, required=False, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Email")

    contact_number = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Number")
    
    class Meta:
        model = ContactDetails
        fields = ('contact_address', 'contact_email', 'contact_number')







class EditClientStatsProfile(forms.ModelForm):
    clients_total = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Total Clients")

    clients_project_complete = forms.CharField(max_length = 2000, required=False, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Projects Completed")

    clients_project_ongoing = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Ongoing Projects")

    clients_satisfaction = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Client Satisfaction")
    
    class Meta:
        model = ClientsStats
        fields = ('clients_total', 'clients_project_complete', 'clients_project_ongoing', 'clients_satisfaction')
