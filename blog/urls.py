from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:pk>/', views.book, name='book'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('login/check/', views.check, name='check'),
    path('cabinet', views.cabinet, name='cabinet')
]
