from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Listing, ListingImage, SavedListing
from .forms import ListingForm, ListingImageFormSet
from categories.models import Category

def home(request):
    """Pagina principală cu ultimele anunțuri"""
    try:
        listings = Listing.objects.filter(status='active').select_related('category', 'owner').order_by('-created_at')
        categories = Category.objects.filter(parent=None, is_active=True)
        
        # Filtrare după categorie
        category_slug = request.GET.get('category')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                listings = listings.filter(
                    Q(category=category) | Q(category__parent=category)
                )
            except Category.DoesNotExist:
                pass
        
        # Căutare
        search_query = request.GET.get('search')
        if search_query:
            listings = listings.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Filtrare după oraș
        city = request.GET.get('city')
        if city:
            listings = listings.filter(city__icontains=city)
        
        # Paginare
        paginator = Paginator(listings, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'categories': categories,
            'search_query': search_query,
            'selected_category': category_slug,
            'selected_city': city,
        }
        return render(request, 'listings/home.html', context)
    except Exception as e:
        print(f"Error in home view: {e}")
        # Fallback pentru debugging
        return render(request, 'listings/home.html', {
            'page_obj': None,
            'categories': [],
            'search_query': None,
            'selected_category': None,
            'selected_city': None,
        })

def listing_detail(request, slug):
    """Detaliile unui anunț"""
    listing = get_object_or_404(
        Listing.objects.select_related('category', 'owner', 'owner__profile'),
        slug=slug
    )
    
    # Incrementez numărul de vizualizări
    listing.views += 1
    listing.save(update_fields=['views'])
    
    # Verific dacă utilizatorul a salvat anunțul
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedListing.objects.filter(
            user=request.user, 
            listing=listing
        ).exists()
    
    # Anunțuri similare
    similar_listings = Listing.objects.filter(
        category=listing.category,
        status='active'
    ).exclude(id=listing.id)[:4]
    
    context = {
        'listing': listing,
        'is_saved': is_saved,
        'similar_listings': similar_listings,
    }
    return render(request, 'listings/detail.html', context)

@login_required
def listing_create(request):
    """Crearea unui anunț nou"""
    if request.method == 'POST':
        form = ListingForm(request.POST)
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            
            # Salvez imaginile din input-ul personalizat
            images = request.FILES.getlist('images')
            for i, image_file in enumerate(images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image_file,
                    is_main=(i == 0)  # Prima imagine este principală
                )
            
            messages.success(request, 'Anunțul a fost creat cu succes!')
            return redirect('listing_detail', slug=listing.slug)
        else:
            messages.error(request, 'Te rog să corectezi erorile din formular.')
    else:
        form = ListingForm()
    
    context = {
        'form': form,
    }
    return render(request, 'listings/create.html', context)

@login_required
def listing_edit(request, slug):
    """Editarea unui anunț"""
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        image_formset = ListingImageFormSet(request.POST, request.FILES, instance=listing)
        
        if form.is_valid() and image_formset.is_valid():
            listing = form.save()
            image_formset.save()
            
            messages.success(request, 'Anunțul a fost actualizat cu succes!')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm(instance=listing)
        image_formset = ListingImageFormSet(instance=listing)
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'listing': listing,
    }
    return render(request, 'listings/edit.html', context)

@login_required
def toggle_save_listing(request, slug):
    """Salvează/unsalvează un anunț"""
    listing = get_object_or_404(Listing, slug=slug)
    saved_listing, created = SavedListing.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    
    if not created:
        saved_listing.delete()
        messages.success(request, 'Anunțul a fost eliminat din salvate.')
    else:
        messages.success(request, 'Anunțul a fost salvat.')
    
    return redirect('listing_detail', slug=slug)

@login_required
def my_listings(request):
    """Anunțurile utilizatorului curent"""
    listings = Listing.objects.filter(owner=request.user).order_by('-created_at')
    
    paginator = Paginator(listings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'listings': page_obj.object_list,  # Pentru compatibilitate cu template
    }
    return render(request, 'listings/my_listings.html', context)

@login_required
def saved_listings(request):
    """Anunțurile salvate de utilizator"""
    saved = SavedListing.objects.filter(user=request.user).select_related('listing').order_by('-saved_at')
    
    paginator = Paginator(saved, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'saved_listings': page_obj.object_list,  # Pentru compatibilitate cu template
    }
    return render(request, 'listings/saved.html', context)

@login_required
def delete_image(request, image_id):
    """Șterge o imagine dintr-un anunț"""
    from django.http import JsonResponse
    from .models import ListingImage
    
    try:
        image = get_object_or_404(ListingImage, id=image_id, listing__owner=request.user)
        image.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def toggle_listing_status(request, slug):
    """Activează/dezactivează un anunț"""
    listing = get_object_or_404(Listing, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['active', 'sold', 'expired', 'draft']:
            listing.status = new_status
            listing.save()
            
            status_messages = {
                'active': 'Anunțul a fost activat cu succes!',
                'sold': 'Anunțul a fost marcat ca vândut!',
                'expired': 'Anunțul a fost dezactivat!',
                'draft': 'Anunțul a fost salvat ca ciornă!'
            }
            
            messages.success(request, status_messages.get(new_status, 'Status actualizat!'))
        else:
            messages.error(request, 'Status invalid!')
    
    return redirect('my_listings')
