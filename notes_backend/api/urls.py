from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health, RegisterView, LoginView, LogoutView, UserView, NoteViewSet
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', UserView.as_view(), name='me'),
    path('', include(router.urls)),
]
