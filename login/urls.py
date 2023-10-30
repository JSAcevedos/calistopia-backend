from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', views.reset, name='reset'),
]