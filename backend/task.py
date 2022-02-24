from celery import shared_task
from time import sleep
from django.conf import settings
from django.core.mail import send_mail
import os
from backend.models import *
import cloudinary.uploader
import cloudinary
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

@shared_task
def remove_file_from_cloudinary(file_name):
    try:
        print("Deleted image.")
        print(file_name)
        cloudinary.uploader.destroy(file_name, invalidate=True)
    except Exception as e:
        print(e)

@shared_task
def make_all_aboutitem_false_except(latest_id):
    about = About.objects.exclude(id = latest_id)
    for item in about:
        item.current = False
        item.save()
        
    
@shared_task
def make_all_client_statsitem_false_except(latest_id):
    client_stats = ClientsStats.objects.exclude(id = latest_id)
    for item in client_stats:
        item.clients_current = False
        item.save()


@shared_task
def make_all_cvresumeitem_false_except(latest_id):
    cvresume = CVResume.objects.exclude(id = latest_id)
    for item in cvresume:
        item.current = False
        item.save()



@shared_task
def make_all_contactdetailsitem_false_except(latest_id):
    contact_details = ContactDetails.objects.exclude(id = latest_id)
    for item in contact_details:
        item.current = False
        item.save()

        
@shared_task
def make_all_bg_item_false_except(latest_id):
    about = BackgroundImages.objects.exclude(id = latest_id)
    for item in about:
        item.current = False
        item.save()
        

@shared_task
def send_mail_task(header, body, contact_email_get, contact_id):
    send_mail(header, body,
            'Ishika Desai <settings.EMAIL_HOST_USER>',   
            [contact_email_get],
            fail_silently = False
            )
    contact_model = Contact.objects.get(id=contact_id)
    contact_model.contact_replied = True
    contact_model.save()
    return None