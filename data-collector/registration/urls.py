from . import views
from django.urls import path

app_name = 'registration'

urlpatterns = [
    path("", views.register, name="register")
]