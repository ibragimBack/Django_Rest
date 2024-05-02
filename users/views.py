import smtplib
from email.message import EmailMessage
import ssl
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import CustomUser, EmaiConfirmation
from . serializers import UserRegistrationSerializer, UserAuthorizationSerializer, ConfirmationCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.conf import settings
import random
import string

@api_view(['GET'])
def registration_api_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')
        user = CustomUser.objects.create_user(username=username, password=password, email=email,is_active=False)
        confirmation_code = ''.join(random.choices(string.digits, k=6))
        EmaiConfirmation.objects.create(user=user, code=confirmation_code)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        msg = EmailMessage()
        msg.set_content(f'Your confirmation code is: {confirmation_code}')
        msg['Subject'] = 'Confirmation Code'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = email

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)

        return Response({'message': 'Confirmation code sent successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthorizationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user and user.is_active:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def confirm_code_api_view(request):
    serializer = ConfirmationCodeSerializer(request.data)
    if serializer.is_valid():
        code = serializer.validated_data.get('code')
        try:
            confirmation_code = EmaiConfirmation.objects.get(code=code)
            user = confirmation_code.user
            user.is_active = True
            user.save()
            confirmation_code.delete()
            return Response({'message': 'Account confirmed successfully'}, status=status.HTTP_200_OK)
        except EmaiConfirmation.DoesNotExist:
            return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
