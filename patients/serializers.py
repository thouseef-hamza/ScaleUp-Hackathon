from rest_framework import serializers
from patients.models import Patient,PatientAddress,PatientAppointment,PatientVitalSign,PatientMedication,PatientLaboratoryResult,PatientInsuranceInformation
from accounts.models import User

class PatientListSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    limit = serializers.IntegerField(
        required=False, default=10, min_value=10, max_value=100000
    )
    search = serializers.CharField(required=False)
    order_by = serializers.CharField(required=False)

class PatientPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields=("date_of_birth","gender")


class PatientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id","first_name","last_name","email","phone_number")

class PatientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        exclude="id",

class PatientAddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientAddress
        exclude=("id",)

class PatientAppointmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientAppointment
        exclude=("id",)

class PatientAppointmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientVitalSign
        exclude=("id",)

class PatientAppointmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientMedication
        exclude=("id",)

class PatientAppointmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientLaboratoryResult
        exclude=("id",)

class PatientAppointmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientInsuranceInformation
        exclude=("id",)


class PatientDetailModelSerializer(serializers.ModelSerializer):
    profile = PatientModelSerializer(source="patient_profile")
    addresses = PatientModelSerializer(source="patient_addresses",many=True)
    vital_signs = PatientModelSerializer(source="patient_vitalsigns",many=True)
    laboratary_results = PatientModelSerializer(
        source="patient_laboratary_results", many=True
    )
    medications = PatientModelSerializer(source="patient_medication", many=True)
    appointments = PatientModelSerializer(source="patient_appointment", many=True)
    insurance = PatientModelSerializer(source="patient_insurance")

    class Meta:
        model=User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "addresses",
            "vital_signs",
            "laboratary_results",
            "medications",
            "appointments",
            "insurance",
        )
