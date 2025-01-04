from django.urls import path
from rest_framework.routers import DefaultRouter
from generic import views

router = DefaultRouter()

urlpatterns = [
    path('basic_info/', views.BasicInfoListView.as_view()),
] + router.urls
