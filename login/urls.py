from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = "main"),
    path('login/', views.login, name="login"),
    path('about/', views.about, name="about"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', views.reset, name='reset'),
    path("user/", views.user_view, name = "user"),
    path("user/config/", views.config, name = "config"),
    path("user/config/<str:id>/", views.change_config, name = "change"),
    path('confirm/<uidb64>/<token>/<str:email>', views.email_confirmated, name='confirmated'),
    path('exercise/<int:exercise_id>', views.exercise, name='exercise')
]