from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from .views import SignUpView, home, login_view
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # -------------------------------------------------------------------------------------------
    # Forget Password
    # -------------------------------------------------------------------------------------------
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/reset_password.html',
             subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='accounts/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done')
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:login')
         ),
         name='password_reset_confirm'),

    path('', home, name='home')
]
