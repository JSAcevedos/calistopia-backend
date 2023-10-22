from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="index"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('main/', views.main, name='main'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', views.reset, name='reset'),
]