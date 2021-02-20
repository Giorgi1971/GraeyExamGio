from django.urls import path
from .views import user_registration, user_login, user_logout

app_name = 'user'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('registration/', user_registration, name='user_registration'),
]
