from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from accounts.forms import CustomUserCreationForm  # Import the custom form
from django_filters import FilterSet, BooleanFilter
from accounts.models import CustomUser
from django import forms
from .forms import UploadedFilesForm
from .models import UploadedFiles

class HomeView(TemplateView):
    template_name = "home.html"

class SignUpView(CreateView):
    form_class = CustomUserCreationForm  # Use the custom form
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")




# Filter class to filter users by public_visibility
class UserFilter(FilterSet):
    public_visibility = BooleanFilter(field_name='public_visibility', label="Public Visibility", widget=forms.CheckboxInput)

    class Meta:
        model = CustomUser
        fields = ['public_visibility']

# View to display authors and sellers (users with public_visibility=True)
def authors_and_sellers(request):
    # Create the filter object from the GET request
    user_filter = UserFilter(request.GET, queryset=CustomUser.objects.filter(public_visibility=True)) #queryset = CustomUser.objects.filter(public_visibility=True)


    # Use the filter to get the filtered list of users
    users = user_filter.qs

    # Render the template with the filtered users
    return render(request, 'authors_and_sellers.html', {'users': users, 'filter': user_filter})



def upload_books(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadedFilesForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('uploaded_files')  # Redirect to uploaded files page
    else:
        form = UploadedFilesForm()
    
    return render(request, 'upload_books.html', {'form': form})

def uploaded_files(request):
    files = UploadedFiles.objects.filter(user=request.user)
    return render(request, 'uploaded_files.html', {'files': files})

class UploadBooksView(TemplateView):
    template_name = "upload_books.html"  # Create this template to allow users to upload files

class UploadedFilesView(TemplateView):
    template_name = "uploaded_files.html"  # Create this template to show the uploaded files