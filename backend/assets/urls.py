from django.urls import path

from assets import views

urlpatterns = [
    path('chains/', views.AssetsChainListView.as_view()),
    path('filling_services/', views.FillingServiceListView.as_view()),
    path('games/', views.AssetsGameListView.as_view()),
    path('all_tokens/', views.AssetsTokenAllListView.as_view()),
    path('all_tokens/<int:pk>/', views.AssetsTokenAllDetailView.as_view()),
    path('tokens/', views.AssetsTokenListCreateView.as_view()),
    path('tokens/<int:pk>/', views.AssetsTokenDetailView.as_view()),
    path('tokens/validate/', views.AssetsTokenValidateView.as_view()),
    path('minute_market_data/', views.MinuteMarketDataView.as_view()),
    path('positions/', views.PositionsView.as_view()),
    path('transactions/', views.TransactionsView.as_view()),
]
