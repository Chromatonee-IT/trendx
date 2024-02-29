from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from store.models import LastLogin
import re

@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    last_login, created = LastLogin.objects.get_or_create(user=user)
    user_agent_raw = request.META.get('HTTP_USER_AGENT', '')[:100]
    browser_name = user_agent_raw.split('(')[0].strip()
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, user_agent_raw)
    device_name = matches[0]
    last_login_ip = request.META.get('REMOTE_ADDR')
    last_login.last_login_ip = last_login_ip

    print(browser_name)
    print(device_name)
    last_login.browser_name = str(browser_name)
    last_login.device_name = str(device_name)
    last_login.save()
