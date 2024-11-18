from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list_view, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail_view, name='chat_detail'),
]