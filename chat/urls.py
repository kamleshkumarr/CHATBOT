from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
  
    path('session/<int:session_id>/', views.chat_view, name='chat_session'),
    path('new-chat/', views.new_chat, name='new_chat'),
    path('get-response/', views.get_response, name='get_response'),
    path('sentiment/', views.sentiment_view, name='sentiment'),
    path('summary/', views.summary_view, name='summary'),
]
