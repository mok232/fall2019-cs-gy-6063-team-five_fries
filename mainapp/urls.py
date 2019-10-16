from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("account", views.account, name="account"),
    path('Search', views.search, name='search'),
]
