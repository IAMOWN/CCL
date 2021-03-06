from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import include
from users import views as user_views

from home import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('profile/', user_views.profile, name='profile'),

    # App includes
    path('', include('library.urls')),
    path('', include('ops.urls')),
    path('tinymce/', include('tinymce.urls')),

    # User Profile/Loyalty
    path('profiles/', user_views.ProfileListView.as_view(), name='profiles'),
    path('profiles/<int:pk>/<int:user_id>/', user_views.ProfileDetailView.as_view(), name='profile-customer'),
]
