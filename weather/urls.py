from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('weather/', views.weather, name='weather'),
    path('register/', views.register, name='register'),
    path('search_history/', views.search_history, name='search_history'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('search_stats/', views.search_stats, name='search_stats'),
    path('user_search_stats/', views.user_search_stats, name='user_search_stats'),
]