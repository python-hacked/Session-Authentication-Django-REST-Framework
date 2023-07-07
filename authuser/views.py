from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializers
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
# from.utils import send_activation_email, send_reset_password_email

class RagistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_dta)
             # Send Acctount Activation EMail

            uid = urlsafe_base64_decode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uid':uid,'token':token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email = (user.email,activation_url)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ActivationView(APIView):
    parser_classes = [AllowAny]
    