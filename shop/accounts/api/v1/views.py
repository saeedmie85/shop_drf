from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import PhoneNumberSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from extensions.utils import send_otp
from random import randint
from accounts.models import OtpCode


class SendOTP(APIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone_number")
            otp = OtpCode.objects.filter(phone_number=phone).last()
            if not otp:
                otp = randint(1000, 9999)
                OtpCode.objects.get_or_create(phone_number=phone, code=otp)
            send_otp(otp, phone)
            return Response({"info": "otp sent"}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            otp = serializer.validated_data.get("otp")
            phone_number = serializer.validated_data.get("phone_number")
            obj = get_object_or_404(OtpCode, phone_number=phone_number, code=otp)
            obj.delete()
            return Response({"info": "user created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
