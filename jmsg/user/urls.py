from django.urls import path
from .views import (
    register,
    login,
    logout,
    register_do,
    login_do,
    conversation,
    messages,
    create_message
)


app_name = 'user'

urlpatterns = [
    path('conversation/<int:user_id>/', conversation, name='conversation'),
    path('messages/<uuid:conversation_id>/', messages, name='messages'),
    path('message/<uuid:conversation_id>/', create_message, name='create_message'),
    path('register/', register, name="register"),
    path('register-do/', register_do, name="register_do"),
    path('login-do/', login_do, name="login_do"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
]
