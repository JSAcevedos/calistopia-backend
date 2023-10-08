from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="index"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('main/', views.main, name='main'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]