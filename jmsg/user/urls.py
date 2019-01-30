from django.urls import path
from .views import register, login, logout


app_name = 'user'

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
]