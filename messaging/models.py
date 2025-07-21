from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing
from django.utils import timezone

class Conversation(models.Model):
    """Conversația dintre doi utilizatori despre un anunț specific"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name="Anunț")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_conversations', verbose_name="Cumpărător")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_conversations', verbose_name="Vânzător")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")
    
    # Status conversație
    is_active = models.BooleanField(default=True, verbose_name="Activ")
    
    class Meta:
        verbose_name = "Conversație"
        verbose_name_plural = "Conversații"
        unique_together = ['listing', 'buyer', 'seller']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversație despre {self.listing.title} între {self.buyer.username} și {self.seller.username}"
    
    def get_other_participant(self, current_user):
        """Returnează celălalt participant din conversație"""
        if current_user == self.buyer:
            return self.seller
        return self.buyer
    
    def get_last_message(self):
        """Returnează ultimul mesaj din conversație"""
        return self.messages.order_by('-created_at').first()
    
    def get_unread_count_for_user(self, user):
        """Returnează numărul de mesaje necitite pentru un utilizator"""
        return self.messages.filter(receiver=user, is_read=False).count()


class Message(models.Model):
    """Mesajul individual într-o conversație"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="Conversație")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Expeditor")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Destinatar")
    
    content = models.TextField(verbose_name="Conținut mesaj")
    
    # Status mesaj
    is_read = models.BooleanField(default=False, verbose_name="Citit")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Citit la")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Trimis la")
    
    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesaje"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Mesaj de la {self.sender.username} către {self.receiver.username}"
    
    def mark_as_read(self):
        """Marchează mesajul ca citit"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class MessageNotification(models.Model):
    """Notificări pentru mesaje noi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilizator")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Mesaj")
    
    is_read = models.BooleanField(default=False, verbose_name="Citit")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creat la")
    
    class Meta:
        verbose_name = "Notificare mesaj"
        verbose_name_plural = "Notificări mesaje"
        unique_together = ['user', 'message']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notificare pentru {self.user.username} - {self.message}"
