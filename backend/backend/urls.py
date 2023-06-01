from django.contrib import admin
from django.urls import path
from fittify import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin', admin.site.urls),
    path('register', views.RegisterView.as_view(), name='auth_register'),
    path('login', obtain_auth_token, name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('user', views.UserInfoView.as_view(), name='user_info'),
    path('user/change_password', views.UserChangePasswordView.as_view(), name="change_user_password"),
    path('user/<int:user_id>', views.UserInfoView.as_view(), name='user_info_by_id'),
    path('user/<int:user_id>/change_password', views.UserChangePasswordView.as_view(), name="change_user_password_by_id"),
    path('users', views.UserListView.as_view(), name="user_list")
]
