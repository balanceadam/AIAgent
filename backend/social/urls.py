from django.urls import path
from rest_framework.routers import DefaultRouter
from social import views

router = DefaultRouter()

urlpatterns = [
    path('follow/', views.FollowView.as_view()),
    path('followed/', views.FollowedView.as_view()),
    path('fans/', views.FansView.as_view()),
    path('followings/', views.FollowingsView.as_view()),
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDeleteView.as_view()),
] + router.urls
