from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('anunt/<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('adauga-anunt/', views.listing_create, name='listing_create'),
    path('editeaza/<slug:slug>/', views.listing_edit, name='listing_edit'),
    path('salveaza/<slug:slug>/', views.toggle_save_listing, name='toggle_save_listing'),
    path('anunturile-mele/', views.my_listings, name='my_listings'),
    path('anunturi-salvate/', views.saved_listings, name='saved_listings'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('toggle-status/<slug:slug>/', views.toggle_listing_status, name='toggle_listing_status'),
]
