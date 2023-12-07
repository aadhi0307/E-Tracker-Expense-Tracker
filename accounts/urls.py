from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    # Add your other URL patterns here
    path('signup/', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_change.html"),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name='password_reset_complete')
    
]