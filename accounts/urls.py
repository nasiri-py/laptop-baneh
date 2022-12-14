from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('resend-code/', views.ResendCodeView.as_view(), name='resend-code'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp-code-login/', views.OtpCodeLoginView.as_view(), name='otp-code-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('profile/', views.PasswordChange.as_view(), name="password-change"),
    path('profile/comment-delete/<int:pk>', views.CommentDeleteView.as_view(), name="comment-delete"),
]
