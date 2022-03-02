from re import T
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import user_passes_test, login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from backend.models import *
from backend.forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from backend.task import *
from ckeditor.fields import RichTextField
from .decorators import *
from django.template.loader import render_to_string
import datetime
from datetime import date


def homepage(request):
    params = {}
    try:
        about = About.objects.filter(current = True)[0]
        params['about'] = about
        params['age'] = date.today().year - about.about_birth_date.year
    except Exception as e:
        print(e)

    try:
        cvresume = CVResume.objects.filter(current = True)[0]
        params['cvresume'] = cvresume
        if len(CVResume.objects.filter(current = True))==0:
            params['cvresume_non_empty'] = False
        params['cvresume_non_empty'] = True
    except Exception as e:
        print(e)
        
    
    try:
        bg_image = BackgroundImages.objects.filter(current = True)[0]
        params['bg_image'] = bg_image
    except Exception as e:
        print(e)

    try:
        experience = Experience.objects.all()
        params['experience'] = experience
        params['experience_non_empty'] = True
        if len(experience) == 0:
            params['experience_non_empty'] = False
    except Exception as e:
        print(e)

    try:
        education = Education.objects.all()
        params['education'] = education
        params['education_non_empty'] = True
        if len(education) == 0:
            params['education_non_empty'] = False
    except Exception as e:
        print(e)
        
    try:
        category = Category.objects.all()
        for item in category:
            item.category_name = item.category_name.replace(" ", "-")
            item.save()
        params['category'] = category
    except Exception as e:
        print(e)
        
    try:
        projects = Projects.objects.all()
        params['projects'] = projects
        params['project_non_empty'] = True
        if len(projects) == 0:
            params['project_non_empty'] = False
            
        category_list = []
        for item in projects:
            category_list.append(item.project_category.category_name)
        category_list = set(category_list)
        params['category_list'] = category_list
        print("category", category_list)
    except Exception as e:
        print(e)
        
    try:
        skills = Skill.objects.all()
        params['skill_non_empty'] = True
        
        if len(skills) == 0:
            params['skill_non_empty'] = False
            
        params['skills'] = skills
    except Exception as e:
        print(e)
        
    


    try:
        services = Services.objects.all()
        params['services_non_empty'] = True
        
        if len(services) == 0:
            params['services_non_empty'] = False
            
        params['services'] = services
    except Exception as e:
        print(e)


    


    try:
        contact_details = ContactDetails.objects.filter(current = True)[0]
        params['contact_details_non_empty'] = True
        print("contact_details", contact_details)
        if len(ContactDetails.objects.filter(current = True))==0:
            params['contact_details_non_empty'] = False
            
        params['contact_details'] = contact_details
    except Exception as e:
        print(e)



        
    try:
        clients_stats = ClientsStats.objects.filter(clients_current = True)
        params['clients_stats_non_empty'] = True
        if len(clients_stats) == 0:
            params['clients_stats_non_empty'] = False
        params['clients_stats'] = clients_stats[0]
    except Exception as e:
        print("clients_stats error", e)

    try:
        link = Link.objects.all()
        params['link_non_empty'] = True
        if len(link) == 0:
            params['link_non_empty'] = False
        params['link'] = link
    except Exception as e:
        print(e)
    return render(request, 'frontend/index.html', params)


def admin_contact_message(request):
    if request.method == "POST":
        contact_name = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        contact_subject = request.POST.get('contact_subject')
        contact_description = request.POST.get('contact_description')
        contact = Contact(contact_name=contact_name, contact_email=contact_email, contact_subject=contact_subject, contact_description=contact_description)
        contact.save()
        print("Success")
        return redirect('homepage')



def logout_request(request):
    logout(request)
    print("Logged out successfully!")
    return redirect("/")


def login_request(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('admin_page')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            username = request.POST.get('email')
            password = request.POST.get('password')
            user_exists = User.objects.filter(email=username).exists()
            if user_exists:
                try:
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    print("You are now logged in as", username)
                    return redirect('admin_about')
                    # return redirect('homepage')
                except:
                    messages.info(request, f"Incorrect Password for {username}")
                    errors = "Incorrect Password"
                    print("Incorrect Password")
                    context['errors'] = errors
            else:
                messages.info(request, f"{username} does not exist.")
                print("username does not exists.")
                errors = "Username/Email does not exists."
                context['errors'] = errors
        form = AuthenticationForm()
        context['form'] = form
    return render(request, "frontend/login.html", context)




@login_required(login_url='/authentication_required/')
@active_user_required
def admin_page(request):
    return render(request, 'frontend/admin.html')







# ADMIN ABOUT SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_about(request):
    about_model = About.objects.all()
    if request.method == "POST":
        about_title = request.POST.get('about_title')
        about_description = request.POST.get('about_description')
        about_from = request.POST.get('about_from')
        about_lives_in = request.POST.get('about_lives_in')
        about_birth_date = request.POST.get('about_birth_date')
        about_img = request.FILES.get('about_img')
        about = About(about_title=about_title, about_description=about_description, about_from=about_from, about_lives_in=about_lives_in, about_birth_date=about_birth_date, about_img=about_img)
        about.save()
        latest_id = About.objects.latest('id').id
        make_all_aboutitem_false_except.delay(latest_id)
        return redirect('admin_about')
    params = {
        'about_model': about_model,
        'about_page': True
    }
    return render(request, 'frontend/admin_about.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_about_edit(request, about_id):
    instance = get_object_or_404(About, id = about_id)
    old_image = str(instance.about_img)
    print(old_image)
    form = EditAboutProfile(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        print("Inside")
        remove_file_from_cloudinary.delay(old_image)
        return redirect('admin_about')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_about.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_about_delete(request, about_id):
    instance = get_object_or_404(About, id = about_id)
    old_image = str(instance.about_img)
    instance.delete()
    try:
        latest_about = About.objects.latest('id')
        latest_id = latest_about.id
        remove_file_from_cloudinary.delay(old_image)
        make_all_aboutitem_false_except.delay(latest_id)
        latest_about.current = True
        latest_about.save()
    except Exception as e:
        print(e)
    params = {
        'about_page': True
    }
    return redirect('admin_about')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_change_current_about(request, about_id):
    about = About.objects.all()
    our_about = about.get(id = about_id)
    about_id_celery = our_about.id
    make_all_aboutitem_false_except.delay(about_id_celery)
    our_about.current = True
    our_about.save()
    params = {
        'about_page': True
    }
    return redirect('admin_about')
# ADMIN ABOUT SECTION ENDS    







# ADMIN CVRESUME SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_cvresume(request):
    cvresume_model = CVResume.objects.all()
    if request.method == "POST":
        cvresume_name = request.POST.get('cvresume_name')
        cvresume_file = request.FILES.get('cvresume_file')
        cvresume = CVResume(cvresume_name=cvresume_name, cvresume_file=cvresume_file)
        cvresume.save()
        latest_id = CVResume.objects.latest('id').id
        make_all_cvresumeitem_false_except.delay(latest_id)
        return redirect('admin_cvresume')
    params = {
        'cvresume_model': cvresume_model,
        'cvresume_page': True
    }
    return render(request, 'frontend/admin_cvresume.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_cvresume_edit(request, cvresume_id):
    instance = get_object_or_404(CVResume, id = cvresume_id)
    old_file = str(instance.cvresume_file)
    print(old_file)
    form = EditCVResumeProfile(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        print("Inside")
        remove_file_from_cloudinary.delay(old_file)
        return redirect('admin_cvresume')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_cvresume.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_cvresume_delete(request, cvresume_id):
    instance = get_object_or_404(CVResume, id = cvresume_id)
    old_file = str(instance.cvresume_file.url)
    print("old file", old_file)
    instance.delete()
    try:
        latest_cvresume = CVResume.objects.latest('id')
        latest_id = latest_cvresume.id
        remove_file_from_cloudinary.delay(old_file)
        make_all_cvresumeitem_false_except.delay(latest_id)
        latest_cvresume.current = True
        latest_cvresume.save()
    except Exception as e:
        print(e)
    params = {
        'cvresume_page': True
    }
    return redirect('admin_cvresume')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_change_current_cvresume(request, cvresume_id):
    cvresume = CVResume.objects.all()
    our_cvresume = cvresume.get(id = cvresume_id)
    cvresume_id_celery = our_cvresume.id
    make_all_cvresumeitem_false_except.delay(cvresume_id_celery)
    our_cvresume.current = True
    our_cvresume.save()
    params = {
        'cvresume_page': True
    }
    return redirect('admin_cvresume')
# ADMIN CVRESUME SECTION ENDS 







# ADMIN BACKGROUND IMAGE SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_bg_image(request):
    bg_image_model = BackgroundImages.objects.all()
    if request.method == "POST":
        bg_image_main = request.FILES.get('bg_image_main')
        bg_image_sec = request.FILES.get('bg_image_sec')
        bg_image = BackgroundImages(bg_image_main=bg_image_main, bg_image_sec=bg_image_sec)
        bg_image.save()
        latest_id = BackgroundImages.objects.latest('id').id
        make_all_bg_item_false_except.delay(latest_id)
        print("success")
        return redirect('admin_bg_image')
    params = {
        'bg_image_model': bg_image_model,
        'bg_image_page': True
    }
    return render(request, 'frontend/admin_bg_image.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_bg_image_edit(request, bg_image_id):
    instance = get_object_or_404(BackgroundImages, id = bg_image_id)
    main_image = str(instance.bg_image_main)
    sec_image = str(instance.bg_image_sec)
    form = EditBGImageProfile(request.POST or None, request.FILES or None, instance=instance)
    
    if form.is_valid():
        form.save()
        return redirect('admin_bg_image')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_bg_image.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_bg_image_delete(request, bg_image_id):
    instance = get_object_or_404(BackgroundImages, id = bg_image_id)
    main_image = str(instance.bg_image_main)
    sec_image = str(instance.bg_image_sec)
    demo_image = main_image + " @#$%" + sec_image
    instance.delete()
    
    try:
        latest_bg_image = BackgroundImages.objects.latest('id')
        latest_id = latest_bg_image.id
        make_all_bg_item_false_except.delay(latest_id)
        latest_bg_image.current = True
        latest_bg_image.save()
    except Exception as e:
        print(e)
    try:
        for item in demo_image.split("@#$%"):
            remove_file_from_cloudinary.delay(item)
        
    except Exception as e:
        print(e)
    params = {
        'bg_image_page': True
    }
    return redirect('admin_bg_image')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_change_current_bg_image(request, bg_image_id):
    bg_image = BackgroundImages.objects.all()
    our_bg_image = bg_image.get(id = bg_image_id)
    bg_image_id_celery = our_bg_image.id
    make_all_bg_item_false_except.delay(bg_image_id_celery)
    our_bg_image.current = True
    our_bg_image.save()
    params = {
        'bg_image_page': True
    }
    return redirect('admin_bg_image')
# ADMIN BACKGROUND IMAGE SECTION ENDS







# ADMIN SKILL SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_skill(request):
    skill_model = Skill.objects.all()
    if request.method == "POST":
        skill_name = request.POST.get('skill_name')
        skill_percentage = request.POST.get('skill_percentage')
        skill = Skill(skill_name=skill_name, skill_percentage=skill_percentage)
        skill.save()
        return redirect('admin_skill')
    params = {
        'skill_model': skill_model,
        'skill_page': True
    }
    return render(request, 'frontend/admin_skill.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_skill_edit(request, skill_id):
    instance = get_object_or_404(Skill, id = skill_id)
    form = EditSkillProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_skill')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_skill.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_skill_delete(request, skill_id):
    instance = get_object_or_404(Skill, id = skill_id)
    instance.delete()
    params = {
        'skill_page': True
    }
    return redirect('admin_skill')
# ADMIN SKILL SECTION ENDS







# ADMIN CATEGORY SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_category(request):
    category_model = Category.objects.all()
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        if(Category.objects.filter(category_name=category_name).exists()):
            messages.success(request, f'Category with name {category_name} already exists.')
        else:
            category = Category(category_name=category_name)
            category.save()
        return redirect('admin_category')
    params = {
        'category_model': category_model,
        'category_page': True
    }
    return render(request, 'frontend/admin_category.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_category_edit(request, category_id):
    instance = get_object_or_404(Category, id = category_id)
    form = EditCategoryProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_category')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_category.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_category_delete(request, category_id):
    instance = get_object_or_404(Category, id = category_id)
    instance.delete()
    params = {
        'category_page': True
    }
    return redirect('admin_category')
# ADMIN CATEGORY SECTION ENDS







# ADMIN PROJECTS SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_project(request):
    category_list = Category.objects.all()
    project_model = Projects.objects.all()
    if request.method == "POST":
        project_title = request.POST.get('project_title')
        project_description = request.POST.get('project_description')
        project_img = request.FILES.get('project_img')
        project_category = request.POST.get('project_category')
        # cat_obj = Category.objects.get(category_name=project_category)
        cat_obj = Category.objects.filter(category_name=project_category)[0]
        project = Projects(project_title=project_title, project_description=project_description, 
                                project_img=project_img, project_category=Category.objects.get(id=cat_obj.id))
        project.save()
        return redirect('admin_project')
    params = {
        'project_model': project_model,
        'category_list': category_list,
        'project_page': True
    }
    return render(request, 'frontend/admin_project.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_project_edit(request, project_id):
    instance = get_object_or_404(Projects, id = project_id)
    form = EditProjectProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_project')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_project.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_project_delete(request, project_id):
    instance = get_object_or_404(Projects, id = project_id)
    instance.delete()
    params = {
        'project_page': True
    }
    return redirect('admin_project')
# ADMIN PROJECT SECTION ENDS







# ADMIN CONTACT SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_page(request):
    contact_model = Contact.objects.all()
    params = {
        'contact_model': contact_model,
        'contact_page': True,
    }
    return render(request, 'frontend/admin_contact_page.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_reply(request, contact_id):
    instance = get_object_or_404(Contact, id = contact_id)
    contact_name = instance.contact_name
    contact_email = instance.contact_email
    contact_subject = instance.contact_subject
    contact_description = instance.contact_description
    
    if request.method == "POST":
        contact_name_get = request.POST.get('contact_name_get')
        contact_email_get = request.POST.get('contact_email_get')
        contact_description_get = request.POST.get('contact_description_get')
        contact_reply_get = request.POST.get('contact_reply_get')
        contact_subject_get = request.POST.get('contact_subject_get')
        email_template_name = "frontend/reply_mail.txt"
        c = {
             'contact_name_get': contact_name_get,
             'contact_email_get' : contact_email_get,
             'contact_description_get' : contact_description_get,
             'contact_reply_get' : contact_reply_get,
             'contact_subject_get': contact_subject_get,
             }
        email_body = render_to_string(email_template_name, c)
        send_mail_task.delay(contact_subject_get, email_body,   
             contact_email_get,
             contact_id,
             )
        #send_mail_task.delay(contact_email_get, contact_description_get, contact_reply_get, "Reply", contact_id)
        return redirect('admin_contact_page')
    params = {
        'contact_name': contact_name,
        'contact_email': contact_email,
        'contact_subject': contact_subject,
        'contact_description': contact_description,
        }
    return render(request, 'frontend/admin_contact_page.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_delete(request, contact_id):
    instance = get_object_or_404(Contact, id = contact_id)
    instance.delete()
    params = {
        'contact_page': True
    }
    return redirect('admin_contact_page')
# ADMIN CONTACT SECTION ENDS







# ADMIN LINK SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_link(request):
    link_model = Link.objects.all()
    if request.method == "POST":
        link_name = request.POST.get('link_name')
        link_url = request.POST.get('link_url')
        link = Link(link_name=link_name, link_url=link_url)
        link.save()
        return redirect('admin_link')
    params = {
        'link_model': link_model,
        'link_page': True,
    }
    return render(request, 'frontend/admin_link.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_link_edit(request, link_id):
    instance = get_object_or_404(Link, id = link_id)
    form = EditLinkProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_link')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_link.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_link_delete(request, link_id):
    instance = get_object_or_404(Link, id = link_id)
    instance.delete()
    params = {
        'link_page': True
    }
    return redirect('admin_link')
# ADMIN LINK SECTION ENDS







# ADMIN EXPERIENCE SECTION STARTS
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
class admin_experience(LoggedInRedirectMixin, CreateView):
    model = Experience
    template_name = 'frontend/admin_experience.html'
    form_class = EditExperienceProfile
    success_url = reverse_lazy('admin_experience')
    

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.experience_year = obj.experience_duration.split(' ')[-1]
        obj.save()
        return redirect('admin_experience')


    def get_context_data(self, *args, **kwargs):
        experience_model = Experience.objects.all()
        params = super(admin_experience, self).get_context_data(*args, **kwargs)
        params["experience_model"] = experience_model
        params["experience_page"] = True
        return params



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_experience_edit(request, experience_id):
    instance = get_object_or_404(Experience, id = experience_id)
    form = EditExperienceProfile(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.experience_year = obj.experience_duration.split(' ')[-1]
        obj.save()
        form.save()
        return redirect('admin_experience')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_experience.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_experience_delete(request, experience_id):
    instance = get_object_or_404(Experience, id = experience_id)
    instance.delete()
    params = {
        'experience_page': True
    }
    return redirect('admin_experience')
# ADMIN EXPERIENCE SECTION ENDS







# ADMIN EDUCATION SECTION STARTS
class admin_education(LoggedInRedirectMixin, CreateView):
    model = Education
    template_name = 'frontend/admin_education.html'
    form_class = EditEducationProfile
    success_url = reverse_lazy('admin_education')
    

    def get_context_data(self, *args, **kwargs):
        education_model = Education.objects.all()
        params = super(admin_education, self).get_context_data(*args, **kwargs)
        params["education_model"] = education_model
        params["education_page"] = True
        return params



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_education_edit(request, education_id):
    instance = get_object_or_404(Education, id = education_id)
    form = EditEducationProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_education')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_education.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_education_delete(request, education_id):
    instance = get_object_or_404(Education, id = education_id)
    instance.delete()
    params = {
        'education_page': True
    }
    return redirect('admin_education')
# ADMIN EDUCATION SECTION ENDS







# ADMIN SERVICES SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_services(request):
    services_model = Services.objects.all()
    if request.method == "POST":
        service_heading = request.POST.get('service_heading')
        service_description = request.POST.get('service_description')
        service_icon = request.POST.get('service_icon')
        services = Services(service_heading=service_heading, service_description=service_description, service_icon=service_icon)
        services.save()
        return redirect('admin_services')
    params = {
        'services_model': services_model,
        'services_page': True,
    }
    return render(request, 'frontend/admin_services.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_services_edit(request, services_id):
    instance = get_object_or_404(Services, id = services_id)
    form = EditServicesProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_services')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_services.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_services_delete(request, services_id):
    instance = get_object_or_404(Services, id = services_id)
    instance.delete()
    params = {
        'services_page': True
    }
    return redirect('admin_services')
# ADMIN SERVICES SECTION ENDS






# ADMIN ABOUT SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_details(request):
    contact_details_model = ContactDetails.objects.all()
    if request.method == "POST":
        contact_address = request.POST.get('contact_address')
        contact_email = request.POST.get('contact_email')
        contact_number = request.POST.get('contact_number')
        contact_details = ContactDetails(contact_address=contact_address, contact_email=contact_email, contact_number=contact_number)
        contact_details.save()
        latest_id = ContactDetails.objects.latest('id').id
        make_all_contactdetailsitem_false_except.delay(latest_id)
        return redirect('admin_contact_details')
    params = {
        'contact_details_model': contact_details_model,
        'contact_details_page': True
    }
    return render(request, 'frontend/admin_contact_details.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_details_edit(request, contact_details_id):
    instance = get_object_or_404(ContactDetails, id = contact_details_id)
    form = EditContactDetailsProfile(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_contact_details')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_contact_details.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_details_delete(request, contact_details_id):
    instance = get_object_or_404(ContactDetails, id = contact_details_id)
    instance.delete()
    try:
        latest_contact_details = ContactDetails.objects.latest('id')
        latest_id = latest_contact_details.id
        make_all_contactdetailsitem_false_except.delay(latest_id)
        latest_contact_details.current = True
        latest_contact_details.save()
    except Exception as e:
        print(e)
    params = {
        'contact_details_page': True
    }
    return redirect('admin_contact_details')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_change_current_contact_details(request, contact_details_id):
    contact_details = ContactDetails.objects.all()
    our_contact_details = contact_details.get(id = contact_details_id)
    contact_details_id_celery = our_contact_details.id
    make_all_contactdetailsitem_false_except.delay(contact_details_id_celery)
    our_contact_details.current = True
    our_contact_details.save()
    params = {
        'contact_details_page': True
    }
    return redirect('admin_contact_details')
# ADMIN ABOUT SECTION ENDS    








# ADMIN CLIENT STATS SECTION STARTS
@login_required(login_url='/authentication_required/')
@active_user_required
def admin_client_stats(request):
    client_stats_model = ClientsStats.objects.all()
    if request.method == "POST":
        clients_total = request.POST.get('clients_total')
        clients_project_complete = request.POST.get('clients_project_complete')
        clients_project_ongoing = request.POST.get('clients_project_ongoing')
        clients_satisfaction = request.POST.get('clients_satisfaction')
        client_stats = ClientsStats(clients_total=clients_total, clients_project_complete=clients_project_complete, 
                                        clients_project_ongoing=clients_project_ongoing, clients_satisfaction=clients_satisfaction)
        client_stats.save()
        latest_id = ClientsStats.objects.latest('id').id
        make_all_client_statsitem_false_except.delay(latest_id)
        return redirect('admin_client_stats')
    params = {
        'client_stats_model': client_stats_model,
        'client_stats_page': True
    }
    return render(request, 'frontend/admin_client_stats.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_client_stats_edit(request, client_stats_id):
    instance = get_object_or_404(ClientsStats, id = client_stats_id)
    form = EditClientStatsProfile(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_client_stats')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_client_stats.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_client_stats_delete(request, client_stats_id):
    instance = get_object_or_404(ClientsStats, id = client_stats_id)
    instance.delete()
    try:
        latest_client_stats = ClientsStats.objects.latest('id')
        latest_id = latest_client_stats.id
        make_all_client_statsitem_false_except.delay(latest_id)
        latest_client_stats.current = True
        latest_client_stats.save()
    except Exception as e:
        print(e)
    params = {
        'client_stats_page': True
    }
    return redirect('admin_client_stats')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_change_current_client_stats(request, client_stats_id):
    client_stats = ClientsStats.objects.all()
    our_client_stats = client_stats.get(id = client_stats_id)
    client_stats_id_celery = our_client_stats.id
    make_all_client_statsitem_false_except.delay(client_stats_id_celery)
    our_client_stats.clients_current = True
    our_client_stats.save()
    params = {
        'client_stats_page': True
    }
    return redirect('admin_client_stats')









# ADMIN ABOUT SECTION ENDS
def error_404_view(request, exception):
    data = {
        "error": "404",
        "message": "The page you requested was not found."
        }
    return render(request, 'frontend/login_required.html', data)
