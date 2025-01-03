from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from .models import UploadedFiles

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "public_visibility", "birth_year", "address")  # Add new fields

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "public_visibility", "birth_year", "address")  # Add new fields



class UploadedFilesForm(forms.ModelForm):
    class Meta:
        model = UploadedFiles
        fields = ['file', 'title', 'description', 'visibility', 'cost', 'published_year']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = file.content_type
            if file_type not in ['application/pdf', 'image/jpeg']:
                raise forms.ValidationError("Only PDF and JPEG files are allowed.")
        return file