from django.urls import path
from .views import PropertyListAPIView, UserPropertyAPIView, PropertyDetailAPIView

urlpatterns = [
    path('', PropertyListAPIView.as_view()),
    path('<int:pk>/', PropertyDetailAPIView.as_view()),
    path('<username>/', UserPropertyAPIView.as_view()),
]
