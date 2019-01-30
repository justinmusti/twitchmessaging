from django.urls import path
from .views import index, contact_list


app_name = 'home'
urlpatterns = [
    path('contact-list/', contact_list, name='contact_list'),
    path('', index, name='index')
]
