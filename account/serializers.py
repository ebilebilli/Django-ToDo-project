from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken')
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required')

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError('Incorrect password')
            if not user.is_active:
                raise serializers.ValidationError('This user is deactivated')
            refresh = RefreshToken.for_user(user)
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'non_field_errors': ['No such account. Please register'],
                'register': True
            })
        
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        token = RefreshToken(self.token)
        token.blacklist()
      