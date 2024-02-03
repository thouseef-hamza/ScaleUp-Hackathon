from rest_framework.views import APIView
from accounts.serializers import RegisterationSerializer
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from web3 import Web3
from django.conf import settings
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

def create_blockchain_address():
    web3 = Web3(
        Web3.HTTPProvider(
            "https://mainnet.infura.io/v3/a6a357c5c5d74c2785bd655c8b2dad4d"
        )
    )
    account = web3.eth.account.create()
    return account.address, account.key.hex()

class ResgisterationAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Institute Profile Updation",
        request_body=RegisterationSerializer,
        responses={
            200: RegisterationSerializer,
            400: "Bad Request",
            500: "Server Error",
        },
    )
    def post(self,request,*args, **kwargs):
        serializer=RegisterationSerializer(data=request.data)
        if not serializer.is_valid():
                return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        user_type = serializer.validated_data.get("user_type",None)
        is_patient,is_researcher,is_healthcare=False,False,False
        if user_type is not None and user_type=='researcher':
            is_researcher = True
        elif user_type is not None and user_type=='healthcare':
            is_healthcare=True
        else:
            is_patient=True
        blockchain_address,blockchain_privatekey=create_blockchain_address()
        User.objects.create(
            first_name=serializer.validated_data.get('first_name',None),
            last_name=serializer.validated_data.get('last_name',None),
            email=serializer.validated_data.get('email',None),
            phone_number=serializer.validated_data.get('phone_number',None),
            is_healthcare=is_healthcare,
            is_patient=is_patient,
            is_researcher=is_researcher,
            blockchain_address=blockchain_address,
        )
        return Response({"message":"User Registered Successfully","privateKey":blockchain_privatekey},status=status.HTTP_201_CREATED)

# class LoginAPIView(APIView):
#     def post(Self,request,*args, **kwargs):
#         email=request.POST.get("email")
#         User.objects.get(email=email)
