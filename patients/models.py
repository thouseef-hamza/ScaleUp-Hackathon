from django.db import models
from accounts.models import User
# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="patient_profile")
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        null=True,
    )
    
    def __str__(self) -> str:
        return self.user.first_name

class PatientAddress(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_addresses")
    address=models.TextField()
    city=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.patient.user.first_name

class PatientVitalSign(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="patient_vitalsigns")
    blood_pressure = models.CharField(max_length=20)
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.patient.user.first_name


class PatientLaboratoryResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name="patient_laboratary_results")
    blood_tests = models.TextField()
    urinalysis = models.TextField()
    imaging_results = models.TextField()

    def __str__(self) -> str:
        return self.patient.user.first_name


class PatientMedication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name="patient_medication")
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.patient.user.first_name


class PatientAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name="patient_appointment")
    date_and_time = models.DateTimeField()
    reason_for_visit = models.TextField()
    doctor_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.patient.user.first_name


class PatientInsuranceInformation(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE,related_name="patient_insurance")
    insurance_provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    group_number = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.patient.user.first_name
