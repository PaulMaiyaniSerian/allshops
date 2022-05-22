from django.shortcuts import render
# model imports
from .models import Profile, User


# drf imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
# Create your views here.

# serializers import
from .serializers import RegisterSerializer, UserSerializer
from .serializers import SellerSerializer

# create test view
class UserListView(APIView):
    """
    list all users
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
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
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)