from rest_framework import serializers
from .models import User, Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["user","username", "fname","lname" , "profile_picture", "business_document_image", "business_super_name", "is_seller"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','password', 'password2')
        extra_kwargs = {
            'password': {'required': True},
            'password2': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

        # override serializer behaviour
    # def to_representation(self, instance):
    #     """remove `is_seller` from serializer."""
    #     ret = super().to_representation(instance)

    #     # print(ret)

    #     ret.pop("is_seller")
    #     return ret

