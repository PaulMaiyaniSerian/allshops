from re import A
from django.test import TestCase

# Create your tests here.
# django imports
from django.urls import reverse
# model imports
from .models  import User
# restframework imports
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
# serializer imports
from .serializers import RegisterSerializer, UserSerializer


# other imports
import json


class RegistrationTestCase(APITestCase):

    def test_register_emptyPayload(self):
        # test empty data
        data = {
            
        }

        response = self.client.post(reverse("register_view"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_register_correctPayload(self):
        # test with correct data
        data = {
            "email": "paulserian@gmail.com",
            "password":"Paulserian1",
            "password2": "Paulserian1"
        }

        response = self.client.post(reverse("register_view"), data)
        # test status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test return data....should return email same as one in payload
        self.assertEqual(response.data["email"], data["email"])

    def test_register_invalidPayload(self):
        # test with invalid payload ---test serializer errors is same

        # start with invalid email
        data = {
            "email" : "svbsdjvbh",
            "password": "Paulserian1",
            "password2": "Paulserian1"
        }
        response = self.client.post(reverse("register_view"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")
        # end invalid email

        # test with weak password
        data = {
            "email" : "paul@gmail.com",
            "password": "paul",
            "password2": "paul"
        }
        response = self.client.post(reverse("register_view"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        password_error_message = "This password is too short. It must contain at least 8 characters."
        self.assertEqual(response.data["password"][0], password_error_message)
        # end test weak password

        # test password match
        data = {
            "email" : "paul@gmail.com",
            "password": "paulserian",
            "password2": "paul"
        }
        response = self.client.post(reverse("register_view"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        password_error_message = "Password fields didn't match."
        self.assertEqual(response.data["password"][0], password_error_message)
        # end password match

        # test common password
        data = {
            "email": "paulserian12@gmail.com",
            "password":"12345678",
            "password2": "12345678"
        }
        response = self.client.post(reverse("register_view"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        password_error_message = "This password is too common."
        self.assertEqual(response.data["password"][0], password_error_message)
        # end common password


        data = {
            "email" : "svbsdjvbh",
            "password": "Paulseriand",
            "password2": "ssdfksdvjk"
        }
        response = self.client.post(reverse("register_view"), data)
        # test status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_emailConstraints(self):
        # testdata
        data = {
            "email": "paulserian@gmail.com",
            "password":"Paulserian1",
            "password2": "Paulserian1"
        }

        # test first action
        response = self.client.post(reverse("register_view"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])
        # run the request again
        response = self.client.post(reverse("register_view"), data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_login(self):
        # test with correct data
        data = {
            "email": "paulserian@gmail.com",
            "password":"Paulserian1",
            "password2": "Paulserian1"
        }

        response = self.client.post(reverse("register_view"), data)
        # test status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test return data....should return email same as one in payload
        self.assertEqual(response.data["email"], data["email"])

        # login test with correct payload
        data = {
            "email": "paulserian@gmail.com",
            "password":"Paulserian1",
        }
        response = self.client.post(reverse("token_obtain_pair"), data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response, "access", 1)
        self.assertContains(response, "refresh", 1)

        # test with email that does not exist should return 401 unauthorized
        # should not contain any tokens
        data = {
            "email": "doesnotExist@gmail.com",
            "password":"Paulserian1",
        }
        response = self.client.post(reverse("token_obtain_pair"), data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertNotContains(response=response, text="access",status_code=401)
        self.assertNotContains(response=response, text="refresh",status_code=401)
        detail_error = "No active account found with the given credentials"
        self.assertEqual(response.data["detail"], detail_error)

        # test with wrong password for a valid account
        # return 401 with no tokens
        data = {
            "email": "paulserian@gmail.com",
            "password":"Paulserian12",
        }
        response = self.client.post(reverse("token_obtain_pair"), data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertNotContains(response=response, text="access",status_code=401)
        self.assertNotContains(response=response, text="refresh",status_code=401)
        # test for message
        detail_error = "No active account found with the given credentials"
        self.assertEqual(response.data["detail"], detail_error)
