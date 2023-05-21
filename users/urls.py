from django.urls import path, include
from .views import UserRegistrationView, UsersApiView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', UsersApiView.as_view()),
    path('login/', MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', UserRegistrationView.as_view())
]