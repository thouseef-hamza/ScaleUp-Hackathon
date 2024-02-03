from django.shortcuts import render
from rest_framework.views import APIView
from patients.serializers import PatientListSerializer,PatientPOSTSerializer,PatientModelSerializer,PatientDetailModelSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from django.db.models import Q
from cryptography.fernet import Fernet
from patients.models import Patient
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

def decrypt_user(key,token):
    fernetKey=Fernet(key)
    user_data=fernetKey.decrypt(token)
    return user_data

def encrypt_user(serialized_data):
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(serialized_data.encode('utf-8'))
    return token,key


class PatientProfileListCreateAPIView(APIView):

    @swagger_auto_schema(
        tags=["patients"],
        operation_description="Before Executing this endpoint try to authorize the Login add --- Bearer access_token ---",
        operation_summary="This endpoint is used for Property List",
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search term",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: PatientModelSerializer,
        },
    )
    def get(self,request,*args, **kwargs):
        serializer=PatientListSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        search=serializer.validated_data.get("search",None)
        serialized_data={}
        if search:
            queryset=User.objects.filter(Q(first_name__istartswith=search)|Q(email__iexact=search))
            serialized_data=PatientModelSerializer(queryset,many=True).data
        return Response({"data":serialized_data},status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer=PatientPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        key=request.GET.get("fernetKey")
        token=request.GET.get("token")
        user_data=decrypt_user(key,token)
        if user_data:
            try:
                user_obj=User.objects.get(id=user_data.id)
            except User.DoesNotExist:
                return Response({"errors":"Provided key with user not found"},status=status.HTTP_404_NOT_FOUND)
            Patient.objects.create(
                user=user_obj.id,
                gender=serializer.validated_data.get("gender",None),
                date_of_birth=serializer.validated_data.get("date_of_birth",None),
            )
            return Response({"data":serializer.data})
        return Response({"errors":"Provided Key or Token is not Valid"},status=status.HTTP_400_BAD_REQUEST)

class PatientRetrieveUpdateAPIView(APIView):
    def get(self,request,*args, **kwargs):
        key=request.GET.get("fernetKey")
        token=request.GET.get("token")
        user_data = decrypt_user(key, token)
        if user_data:
            return Response({"data":user_data},status=status.HTTP_200_OK)
        return Response({"errors":"No User with this token and key"},status=status.HTTP_400_BAD_REQUEST)

class SendUserToken(APIView):
    def post(self,request,id,*args, **kwargs):
        user = User.objects.prefetch_related(
            "patient_profile",
            "patient_addresses",
            "patient_vitalsigns",
            "patient_laboratary_results",
            "patient_medication",
            "patient_appointment",
            "patient_insurance",
        ).get(id=id)
        serializer =PatientDetailModelSerializer(user)
        token,key=encrypt_user(serialized_data=serializer.data)
        from django.core.mail import send_mail
        subject = 'Hello from Django!'
        message = """This is a test email sent from Django.
        Token :-  {}
        Key :- {}
        """.format(token,key)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]  
        send_mail(subject, message, from_email, recipient_list)
        return Response({"data":"Patient Token Sent Successfully"},status=status.HTTP_200_OK)
