from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import reset_password_request, reset_password

urlpatterns = [
    # Add your other URL patterns here
    path('signup/', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('reset-password/', reset_password_request, name='reset_password_request'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),
    
    # path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')
    
]