from django.urls import path
from . import views

urlpatterns = [
    path('login',views.signin,name='login'),
    path('get_csrf',views.get_csrf)
]