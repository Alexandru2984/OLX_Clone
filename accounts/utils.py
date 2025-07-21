from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
import logging

logger = logging.getLogger(__name__)


def send_confirmation_email(user, request=None):
    """
    Trimite email de confirmare către utilizator
    """
    try:
        confirmation = user.email_confirmation
    except AttributeError:
        from .models import EmailConfirmation
        confirmation = EmailConfirmation.objects.create(user=user)
    
    # Generează link-ul de confirmare
    if request:
        domain = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
    else:
        try:
            site = Site.objects.get_current()
            domain = site.domain
            protocol = 'https' if settings.DEBUG is False else 'http'
        except:
            domain = 'localhost:8000'
            protocol = 'http'
    
    confirmation_url = f"{protocol}://{domain}{reverse('confirm_email', kwargs={'token': confirmation.token})}"
    
    # Context pentru template
    context = {
        'user': user,
        'confirmation_url': confirmation_url,
        'site_name': 'OLX Clone',
        'protocol': protocol,
        'domain': domain,
    }
    
    # Randare template-uri
    subject = 'Confirmă-ți adresa de email - OLX Clone'
    html_message = render_to_string('accounts/emails/email_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email de confirmare trimis către {user.email}")
        return True
    except Exception as e:
        logger.error(f"Eroare la trimiterea email-ului către {user.email}: {str(e)}")
        return False


def send_new_message_notification(message):
    """
    Trimite notificare email pentru mesaj nou
    """
    if not message.receiver.profile.email_notifications:
        return False
    
    context = {
        'message': message,
        'receiver': message.receiver,
        'sender': message.sender,
        'listing': message.conversation.listing,
        'site_name': 'OLX Clone',
    }
    
    subject = f'Mesaj nou de la {message.sender.username} - OLX Clone'
    html_message = render_to_string('messaging/emails/new_message_notification.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[message.receiver.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Notificare mesaj trimisă către {message.receiver.email}")
        return True
    except Exception as e:
        logger.error(f"Eroare la trimiterea notificării către {message.receiver.email}: {str(e)}")
        return False


def send_listing_status_notification(listing, new_status):
    """
    Trimite notificare când se schimbă statusul unui anunț
    """
    if not listing.owner.profile.email_notifications:
        return False
    
    status_messages = {
        'active': 'activat',
        'inactive': 'dezactivat',
        'sold': 'marcat ca vândut',
        'expired': 'expirat',
    }
    
    context = {
        'listing': listing,
        'user': listing.owner,
        'new_status': new_status,
        'status_message': status_messages.get(new_status, new_status),
        'site_name': 'OLX Clone',
    }
    
    subject = f'Statusul anunțului "{listing.title}" a fost modificat - OLX Clone'
    html_message = render_to_string('listings/emails/status_notification.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[listing.owner.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Notificare status anunț trimisă către {listing.owner.email}")
        return True
    except Exception as e:
        logger.error(f"Eroare la trimiterea notificării către {listing.owner.email}: {str(e)}")
        return False


def send_password_reset_notification(user, reset_url):
    """
    Trimite notificare pentru resetarea parolei
    """
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'OLX Clone',
    }
    
    subject = 'Resetare parolă - OLX Clone'
    html_message = render_to_string('accounts/emails/password_reset.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email resetare parolă trimis către {user.email}")
        return True
    except Exception as e:
        logger.error(f"Eroare la trimiterea email-ului către {user.email}: {str(e)}")
        return False
