from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.index, name='home'),
    path("about", views. about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    path("signup", views.signup, name='signup'),
    path("login", views.log, name='login'),
    path("profile", views.profile, name='profile'),
    path("logout", views.logout_view, name='logout'),
    path('search', views.search_view, name='search'),
    path('details', views.details, name='details'),
]