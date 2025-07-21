from django.contrib import admin
from .models import Listing, ListingImage, SavedListing

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main']

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'owner', 'price', 'city', 'status', 'views', 'created_at']
    list_filter = ['status', 'condition', 'category', 'city', 'created_at']
    search_fields = ['title', 'description', 'owner__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    inlines = [ListingImageInline]
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informații generale', {
            'fields': ('title', 'slug', 'description', 'category', 'owner')
        }),
        ('Detalii produs', {
            'fields': ('price', 'is_negotiable', 'condition')
        }),
        ('Locație și contact', {
            'fields': ('city', 'county', 'phone', 'email')
        }),
        ('Status', {
            'fields': ('status', 'views', 'expires_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'is_main', 'uploaded_at']
    list_filter = ['is_main', 'uploaded_at']

@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'saved_at']
    list_filter = ['saved_at']
