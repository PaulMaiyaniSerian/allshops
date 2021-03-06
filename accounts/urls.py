from django.urls import path

# import views
from . import views

# simplejwt views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('users/', views.UserListView.as_view(), name="test_view"),
    path("register_user/", views.RegisterView.as_view(), name="register_view"),

    # update_profile_view
    path('profile/', views.ProfileView.as_view(), name="accounts_profile"),

    # jwt views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # register_view
]