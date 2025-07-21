from django.urls import path
from . import views

urlpatterns = [
    # Lista conversațiilor
    path('', views.conversation_list, name='conversation_list'),
    
    # Detalii conversație
    path('conversatie/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    
    # Începerea unei conversații noi
    path('start/<int:listing_id>/', views.start_conversation, name='start_conversation'),
    
    # AJAX endpoints
    path('mark-read/<int:conversation_id>/', views.mark_messages_read, name='mark_messages_read'),
    path('unread-count/', views.get_unread_count, name='get_unread_count'),
    
    # Ștergerea conversației
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]
