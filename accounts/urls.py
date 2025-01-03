from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignUpView, HomeView, login_view, logout_view, authors_and_sellers, upload_books, uploaded_files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("authors-and-sellers/", authors_and_sellers, name="authors_and_sellers"),
    path('upload-books/', upload_books, name='upload_books'),
    path('uploaded-files/', uploaded_files, name='uploaded_files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


