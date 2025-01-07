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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.authentication import TokenAuthentication

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



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can log out

    def post(self, request):
        request.user.auth_token.delete()  # Delete the user's token
        return Response(status=status.HTTP_200_OK)


class UploadView(APIView):
    parser_classes = [FileUploadParser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.data.get('file_upload',None)
        import pdb; pdb.set_trace()
        print(file)
        if file:
            return Response({"message" : "File is received"}, status= 200)
        else:
            return Response({"message" : "File is missing"}, status= 400)
        
        from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.models import UploadedFiles
from django.http import Http404
from rest_framework import status

class UserFilesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        files = UploadedFiles.objects.filter(user=user)
        if not files:
            return Response({"message": "No files found"}, status=status.HTTP_404_NOT_FOUND)

        files_data = [
            {"title": file.title, "description": file.description, "file_url": file.file.url}
            for file in files
        ]
        return Response(files_data, status=status.HTTP_200_OK)


from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

# def send_email_view(request):
#     subject = "Test Email"
#     message = "This is a test email sent from Django."
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = ['recipient_email@example.com']

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         return HttpResponse("Email sent successfully!")
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")

from django.core.mail import send_mail

def send_test_email(request):
    send_mail(
        'Test Subject',
        'This is a test email.',
        'testemaildjango001@gmail.com',
        ['user@user.com'],
        fail_silently=False,
    )
    return HttpResponse("Test email sent!")
