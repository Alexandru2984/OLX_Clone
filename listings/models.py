from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from django.urls import reverse
from django.utils.text import slugify

class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Nou'),
        ('very_good', 'Foarte bună'),
        ('good', 'Bună'),
        ('satisfactory', 'Satisfăcătoare'),
        ('for_parts', 'Pentru piese'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Activ'),
        ('sold', 'Vândut'),
        ('expired', 'Expirat'),
        ('draft', 'Ciornă'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titlu")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(verbose_name="Descriere")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preț")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Stare")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categorie")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Proprietar")
    
    # Locație
    city = models.CharField(max_length=100, verbose_name="Oraș")
    county = models.CharField(max_length=100, verbose_name="Județ")
    
    # Contact
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Status și timp
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Status")
    is_negotiable = models.BooleanField(default=True, verbose_name="Preț negociabil")
    views = models.PositiveIntegerField(default=0, verbose_name="Vizualizări")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Expiră la")

    class Meta:
        verbose_name = "Anunț"
        verbose_name_plural = "Anunțuri"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Listing.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'slug': self.slug})

    def get_main_image(self):
        """Returnează prima imagine a anunțului"""
        first_image = self.images.first()
        return first_image.image.url if first_image else None


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/%d/', verbose_name="Imagine")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Text alternativ")
    is_main = models.BooleanField(default=False, verbose_name="Imagine principală")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagine anunț"
        verbose_name_plural = "Imagini anunțuri"
        ordering = ['-is_main', 'uploaded_at']

    def __str__(self):
        return f"Imagine pentru {self.listing.title}"


class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilizator")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name="Anunț")
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name="Salvat la")

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name = "Anunț salvat"
        verbose_name_plural = "Anunțuri salvate"

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
