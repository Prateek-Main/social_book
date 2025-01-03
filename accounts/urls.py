from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignUpView, HomeView, login_view, logout_view

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
