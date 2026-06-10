from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'social'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('user/edit/', views.edit_user, name='edit_account'),
    path('ticket/', views.ticket, name='ticket'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='/password_reset/done/'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/password_reset/complete'), name="password_reset_confirm"),
    path('password_reset/complete/',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('posts/', views.post_list, name="post_list"),
]