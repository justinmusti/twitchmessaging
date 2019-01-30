from django.urls import path
from .views import (
    register,
    login,
    logout,
    register_do,
    login_do
)


app_name = 'user'

urlpatterns = [
    path('register/', register, name="register"),
    path('register-do/', register_do, name="register_do"),
    path('login-do/', login_do, name="login_do"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
]