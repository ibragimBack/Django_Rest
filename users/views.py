from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, ConfirmationCode
from .serializers import UserRegistrationSerializer, UserAuthorizationSerializer, ConfirmationCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
import string
from rest_framework.views import APIView


class RegistrationAPIView(APIView):
    def get(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = CustomUser.objects.create_user(username=username, password=password, is_active=False)

            while True:
                new_code = ''.join(random.choices(string.digits, k=6))
                if not ConfirmationCode.objects.filter(code=new_code).exists():
                    ConfirmationCode.objects.create(user=user, code=new_code)
                    break

            return Response({'confirmation_code': new_code}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user and user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ConfirmationCodeAPIView(APIView):
    def confirm_code_api_view(self ,request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            try:
                confirmation_code = ConfirmationCode.objects.get(code=code)
                user = confirmation_code.user
                if user.is_active:
                    return Response({'error': 'Account already confirmed'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.is_active = True
                    user.save()
                    confirmation_code.delete()
                    return Response({'message': 'Account confirmed successfully'}, status=status.HTTP_200_OK)
            except ConfirmationCode.DoesNotExist:
                return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)