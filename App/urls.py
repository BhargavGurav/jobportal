from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerRecruiter/', views.registerRecruiter, name='registerRecruiter'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('profile/', views.profile, name='profile'),
    path('logoutUser/', views.logoutuser, name='logoutUser'),
    path('apply/<str:job_id>', views.apply, name='apply'),
    path('addPost/' , views.addPost, name='addPost'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('search/', views.searched, name='search'),
]