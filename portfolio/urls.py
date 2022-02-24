"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import admin_experience, admin_education
# from .views import ProjectCreateView


admin.site.site_header = 'Ishika Desai Portfolio - Admin'
admin.site.site_title = 'Ishika Desai Portfolio - Title'
admin.site.index_title = 'Welcome to Portfolio Admin - Admin Panel'


urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('admin/', admin.site.urls),
    path('login_page/', views.login_request, name = 'login_page'),
    path('logout_request/', views.logout_request, name = 'logout_request'),
    
    
    # #homepage for admin section
    path('admin_page/', views.admin_page, name = 'admin_page'),
    path('authentication_required/', views.authentication_required, name = "authenticationRequired"),
    
    
    
    # #bg image page urls for admin
    path('admin_bg_image/', views.admin_bg_image, name = 'admin_bg_image'),
    path('admin_bg_image_edit/<bg_image_id>', views.admin_bg_image_edit, name = 'admin_bg_image_edit'),
    path('admin_bg_image_delete/<bg_image_id>', views.admin_bg_image_delete, name = 'admin_bg_image_delete'),
    path('admin_change_current_bg_image/<bg_image_id>', views.admin_change_current_bg_image, name = 'admin_change_current_bg_image'),
    
    # #about page urls for admin
    path('admin_about/', views.admin_about, name = 'admin_about'),
    path('admin_about_edit/<about_id>', views.admin_about_edit, name = 'admin_about_edit'),
    path('admin_about_delete/<about_id>', views.admin_about_delete, name = 'admin_about_delete'),
    path('admin_change_current_about/<about_id>', views.admin_change_current_about, name = 'admin_change_current_about'),
    


    # #cvresume page urls for admin
    path('admin_cvresume/', views.admin_cvresume, name = 'admin_cvresume'),
    path('admin_cvresume_edit/<cvresume_id>', views.admin_cvresume_edit, name = 'admin_cvresume_edit'),
    path('admin_cvresume_delete/<cvresume_id>', views.admin_cvresume_delete, name = 'admin_cvresume_delete'),
    path('admin_change_current_cvresume/<cvresume_id>', views.admin_change_current_cvresume, name = 'admin_change_current_cvresume'),


    # #skills page urls for admin
    path('admin_skill/', views.admin_skill, name = 'admin_skill'),
    path('admin_skill_edit/<skill_id>', views.admin_skill_edit, name = 'admin_skill_edit'),
    path('admin_skill_delete/<skill_id>', views.admin_skill_delete, name = 'admin_skill_delete'),
    
    
    # #project page urls for admin
    path('admin_project/', views.admin_project, name = 'admin_project'),
    path('admin_project_edit/<project_id>', views.admin_project_edit, name = 'admin_project_edit'),
    path('admin_project_delete/<project_id>', views.admin_project_delete, name = 'admin_project_delete'),
    
    

    # #category page urls for admin
    path('admin_category/', views.admin_category, name = 'admin_category'),
    path('admin_category_edit/<category_id>', views.admin_category_edit, name = 'admin_category_edit'),
    path('admin_category_delete/<category_id>', views.admin_category_delete, name = 'admin_category_delete'),



    # #experience page urls for admin
    path('admin_experience/', admin_experience.as_view(), name = 'admin_experience'),
    path('admin_experience_edit/<experience_id>', views.admin_experience_edit, name = 'admin_experience_edit'),
    path('admin_experience_delete/<experience_id>', views.admin_experience_delete, name = 'admin_experience_delete'),
    

    # #experience page urls for admin
    path('admin_education/', admin_education.as_view(), name = 'admin_education'),
    path('admin_education_edit/<education_id>', views.admin_education_edit, name = 'admin_education_edit'),
    path('admin_education_delete/<education_id>', views.admin_education_delete, name = 'admin_education_delete'),



    # #contact page urls for admin
    path('admin_contact_message/', views.admin_contact_message, name = 'admin_contact_message'),
    path('admin_contact_page/', views.admin_contact_page, name = 'admin_contact_page'),
    path('admin_contact_delete/<contact_id>', views.admin_contact_delete, name = 'admin_contact_delete'),
    path('admin_contact_reply/<contact_id>', views.admin_contact_reply, name = 'admin_contact_reply'),
    
    
    # #links page urls for admin
    path('admin_link/', views.admin_link, name = 'admin_link'),
    path('admin_link_edit/<link_id>', views.admin_link_edit, name = 'admin_link_edit'),
    path('admin_link_delete/<link_id>', views.admin_link_delete, name = 'admin_link_delete'),
    

    # #services page urls for admin
    path('admin_services/', views.admin_services, name = 'admin_services'),
    path('admin_services_edit/<services_id>', views.admin_services_edit, name = 'admin_services_edit'),
    path('admin_services_delete/<services_id>', views.admin_services_delete, name = 'admin_services_delete'),   



    # #contact details page urls for admin
    path('admin_contact_details/', views.admin_contact_details, name = 'admin_contact_details'),
    path('admin_contact_details_edit/<contact_details_id>', views.admin_contact_details_edit, name = 'admin_contact_details_edit'),
    path('admin_contact_details_delete/<contact_details_id>', views.admin_contact_details_delete, name = 'admin_contact_details_delete'),
    path('admin_change_current_contact_details/<contact_details_id>', views.admin_change_current_contact_details, name = 'admin_change_current_contact_details') ,



    # #contact details page urls for admin
    path('admin_client_stats/', views.admin_client_stats, name = 'admin_client_stats'),
    path('admin_client_stats_edit/<client_stats_id>', views.admin_client_stats_edit, name = 'admin_client_stats_edit'),
    path('admin_client_stats_delete/<client_stats_id>', views.admin_client_stats_delete, name = 'admin_client_stats_delete'),
    path('admin_change_current_client_stats/<client_stats_id>', views.admin_change_current_client_stats, name = 'admin_change_current_client_stats') 





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'portfolio.views.error_404_view'