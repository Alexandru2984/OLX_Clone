from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    city = models.CharField(max_length=100, blank=True, verbose_name="Oraș")
    county = models.CharField(max_length=100, blank=True, verbose_name="Județ")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Despre mine")
    
    # Statistici
    total_listings = models.PositiveIntegerField(default=0, verbose_name="Total anunțuri")
    total_sold = models.PositiveIntegerField(default=0, verbose_name="Total vândute")
    
    # Setări
    email_notifications = models.BooleanField(default=True, verbose_name="Notificări email")
    phone_public = models.BooleanField(default=True, verbose_name="Telefon public")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil utilizator"
        verbose_name_plural = "Profiluri utilizatori"

    def __str__(self):
        return f"Profil {self.user.username}"

    def get_full_location(self):
        """Returnează locația completă"""
        if self.city and self.county:
            return f"{self.city}, {self.county}"
        elif self.city:
            return self.city
        elif self.county:
            return self.county
        return ""


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creează automat un profil când se creează un utilizator nou"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salvează profilul când se salvează utilizatorul"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class EmailConfirmation(models.Model):
    """Model pentru confirmarea email-ului utilizatorilor"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_confirmation')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Confirmare Email"
        verbose_name_plural = "Confirmări Email"
    
    def __str__(self):
        return f"Confirmare email pentru {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Verifică dacă token-ul a expirat (3 zile)"""
        from django.conf import settings
        timeout_days = getattr(settings, 'EMAIL_CONFIRMATION_TIMEOUT_DAYS', 3)
        expiry_date = self.created_at + datetime.timedelta(days=timeout_days)
        return timezone.now() > expiry_date
    
    def confirm(self):
        """Marchează email-ul ca fiind confirmat"""
        self.is_confirmed = True
        self.confirmed_at = timezone.now()
        self.user.is_active = True  # Activează contul
        self.user.save()
        self.save()


@receiver(post_save, sender=User)
def create_email_confirmation(sender, instance, created, **kwargs):
    """Creează automat o confirmare email când se creează un utilizator nou"""
    if created and not instance.is_superuser:
        EmailConfirmation.objects.create(user=instance)
