from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings

from .views import (
    register_view, 
    login_view, 
    logout_view, 
    activate_view, 
    send_activateEmail_view,
    user_account_view,
    order_details_view,
    cancel_refund_view
    )
from .forms import UserPasswordResetForm, UserSetPasswordForm


urlpatterns =  [
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        html_email_template_name= 'users/password_reset_email.html',
        form_class = UserPasswordResetForm),
        name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_sent.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_form.html',
        form_class = UserSetPasswordForm), 
        name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_done.html'), 
        name='password_reset_complete'),
    path('activate_account/<uidb64>/<token>', activate_view, name='activate-account'),
    path('resend_activate_account/<uidb64>/<token>', send_activateEmail_view, name="resend-activate-account"),
    path('user_account/', user_account_view, name='user-account'),
    path('order_details/<slug>/', order_details_view, name='order-details'),
    path('order_details/cancel/<slug>/', cancel_refund_view, name='order-cancel'),
]