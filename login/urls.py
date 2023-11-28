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
    path('exercise/<int:exercise_id>', views.exercise, name='exercise'),
    path('feedback/', views.feedback, name='feedback'),
    path('user_feedback/', views.user_feedback, name='user_feedback'),
    path('user_feedback/<int:fid>/', views.feedback_content, name='feedback_content'),
    path('user_feedback/<int:fid>/delete/', views.delete_feedback, name='feedback_content_delete'),
    path('user_feedback/<int:fid>/actualice_feedback/', views.actualice_feedback, name='feedback_content_actualice'),
    path('routines/<int:routine_id>/', views.routine, name='routine'),
    path('routine/create/', views.create_routine, name='create_routine'),
    path('routine/modify/<int:routine_id>/', views.modify_routine, name='modify_routine'),
    path('routine/delete/<int:routine_id>/', views.delete_routine, name='delete_routine'),
]