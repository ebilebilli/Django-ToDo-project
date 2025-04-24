import logging
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer, serializers

from utils.permission import HeHasPermission

logger = logging.getLogger('account')

  
class RegisterAPIView(APIView):
    """User registration endpoint (public access)."""
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'[Register] User {user.id} registered successfully.Date: {datetime.now()}')
            return Response({'message': 'User registered successfully.'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class LoginAPIView(APIView):
    """User login endpoint (public access)."""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            logger.info(f'[Login] User {data["user"]["email"]} logged in at {datetime.now()}')
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            if 'account' in str(e):
                return HttpResponseRedirect(reverse('register'))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """User logout endpoint (JWT auth required)."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    
    def post(self, request):
        user = request.user
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f'[Logout] User {user.id} Successfully logged out.Date:{datetime.now}')
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)