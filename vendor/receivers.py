from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import customer
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import base64

@receiver(post_save, sender=User)
def send_staff_permission_email(sender, instance, created, **kwargs):
    if not created and instance.is_staff:
        subject = 'Vendor Access Granted'
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.customer.email]
        # static_image_url = f"{settings.BASE_URL}{settings.STATIC_URL}/images/logo-blue.png"
        base_url = settings.BASE_URL
        html_content = render_to_string('vedor_access_granted_email.html', {'base_url':base_url,'instance': instance})
        email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()