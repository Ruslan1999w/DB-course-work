from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:pk>/', views.book, name='book'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('logout', views.logout, name='logout'),
    path('editor', views.editor, name='editor'),
    path('editor/result', views.editor_result, name='editor_result'),
]
