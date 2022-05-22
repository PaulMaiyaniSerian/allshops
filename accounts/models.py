from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# add signals
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

SUBSCRIPTION_NAME_LIST = (
    ('FREE','FREE'),
    ('BASIC','BASIC'),
    ('PREMIUM', 'PREMIUM'),
    ('UNLIMITED', 'UNLIMITED')
)
class Subscription(models.Model):
    name = models.CharField(max_length=250, choices=SUBSCRIPTION_NAME_LIST)
    old_price = models.IntegerField()
    current_price = models.IntegerField()

    def __str__(self):
        return self.name


# add a profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)

    fname = models.CharField(max_length=250, null=True, blank=True)
    lname = models.CharField(max_length=250, null=True, blank=True)
    # change path later
    profile_picture = models.ImageField(upload_to ='profile_pictures/',null=True, blank=True)
    business_document_image = models.ImageField(upload_to ='business_documents/',null=True, blank=True)

    owned_shops_count = models.IntegerField(default=0, null=True, blank=True)
    business_super_name = models.CharField(max_length=250, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    is_seller = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.email}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)