from django.urls import path
from rest_framework.routers import DefaultRouter
from account import views

router = DefaultRouter()

urlpatterns = [
    path('info/', views.AccountInfoView.as_view()),
    path('in_whitelist/', views.InWhitelistView.as_view()),
] + router.urls
