from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path('', views.Dashboard, name="home"),
    path('login/', views.LoginHandler, name="login"),
    path('logout/', views.logout, name="logout"),
]