from accounts.models import Profile
from django.shortcuts import get_object_or_404

# utils getuser profile
def get_user_profile(user):
    profile = get_object_or_404(Profile, user=user)
    return profile