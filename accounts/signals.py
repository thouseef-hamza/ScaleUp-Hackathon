from accounts.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

@receiver(pre_save, sender=User)
def set_random_password(sender, instance, **kwargs):
    if instance._state.adding:
        random_password = get_random_string(length=5)
        instance.set_password(random_password)
