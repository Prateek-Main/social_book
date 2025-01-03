from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from .managers import CustomUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    # New fields
    public_visibility = models.BooleanField(default=True)  # Whether user info is visible publicly
    birth_year = models.IntegerField(null=True, blank=True)  # User's birth year
    address = models.CharField(max_length=255, null=True, blank=True)  # User's address

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No username field is required; email is used for authentication

    objects = CustomUserManager()

    @property
    def age(self):
        """Calculate the user's age based on birth year."""
        if self.birth_year:
            return date.today().year - self.birth_year
        return None  # Return None if birth_year is not set

    def __str__(self):
        return self.email



class UploadedFiles(models.Model):
    user = models.ForeignKey(CustomUser, related_name='uploaded_files', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploaded_books/')
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    published_year = models.IntegerField()
    visibility = models.BooleanField(default=True)  # Assuming public_visibility

    def __str__(self):
        return self.title
