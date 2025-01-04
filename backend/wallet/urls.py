from django.urls import path
from rest_framework.routers import DefaultRouter
from wallet import views

router = DefaultRouter()

urlpatterns = [
    path('login_or_register/', views.WalletLoginOrRegisterView.as_view()),
] + router.urls
