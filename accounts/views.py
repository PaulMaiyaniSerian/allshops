from django.shortcuts import render,get_object_or_404
# model imports
from .models import Profile, User
from .models import SUBSCRIPTION_NAME_LIST, Subscription
# import utils
from .utils import dbops


# rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes as login_required
from rest_framework.decorators import api_view
# Create your views here.

# serializers import
from .serializers import RegisterSerializer, UserSerializer
from .serializers import ProfileSerializer
from accounts import serializers

# import logs
import logging
# setup logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logs

# create test view
class UserListView(APIView):
    """
    list all users
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        logger.info(f"user --{request.user}-- accessing all users in site \n")

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



# create a signup view for seller
class RegisterView(APIView):
    """ register view """
    def post(self, request):
        data = request.data

        serializer = RegisterSerializer(data=data, many=False)
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"user {serializer.data['email']} created  account successfully \n ")

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.info(f"user--- account creation revoked  with errors:{str(serializer.errors)} \n")

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#profile actions crud
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        data = request.data
        data.update({"user": request.user.id})
        # get profile from authenticated user
        profile = dbops.get_user_profile(request.user)
        logger.info(f"user---{request.user}--- accessing profile update view: \n")
        
        # update instance profile data with data from payload
        # serialize update data
        serializer = ProfileSerializer(data=data, instance=profile, many=False)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"user {request.user} profile  updated successfully \n ")

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.info(f"user {request.user} profile  update revoked with errors {serializer.errors} \n ")

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request):
        # get profile from auth user
        profile = dbops.get_user_profile(request.user)

        serializer = ProfileSerializer(profile, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


 
