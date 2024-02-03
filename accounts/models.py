from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def generate_fernet_key():
    from cryptography.fernet import Fernet
    key=Fernet.generate_key()
    return key

class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    is_patient=models.BooleanField(default=False)
    is_researcher=models.BooleanField(default=False)
    is_healthcare=models.BooleanField(default=False)
    blockchain_address=models.CharField(max_length=100,unique=True,null=True)
    fernet_key = models.BinaryField(max_length=32,default=generate_fernet_key)
    fernet_created_at=models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS="email",

    def __str__(self) -> str:
        return self.first_name + self.email


class HeathCareProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, null=True, blank=True)
    hospital_affiliation = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=20, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)


class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    research_focus = models.CharField(max_length=100, null=True)
    affiliated_institution = models.CharField(max_length=100, null=True)
    research_experience = models.PositiveIntegerField(null=True)
    education_background = models.TextField(null=True)
    publications = models.TextField(null=True)
