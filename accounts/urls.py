# urls.py

from django.urls import path
from .views import SignUpView, HomeView, login_view, logout_view, authors_and_sellers, upload_books, uploaded_files, UploadView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),  # Web logout view
    path("authors-and-sellers/", authors_and_sellers, name="authors_and_sellers"),
    path('upload-books/', upload_books, name='upload_books'),
    path('uploaded-files/', uploaded_files, name='uploaded_files'),
    
    # API URLS
    path('api/v1/', include('djoser.urls')),#
    path('api/v1/', include('djoser.urls.authtoken')),#

    path('upload/', UploadView.as_view(), name='file_upload')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
