from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Max
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Conversation, Message, MessageNotification
from .forms import MessageForm, QuickMessageForm
from listings.models import Listing
from accounts.utils import send_new_message_notification


@login_required
def conversation_list(request):
    """Listează toate conversațiile utilizatorului"""
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user),
        is_active=True
    ).annotate(
        last_message_time=Max('messages__created_at'),
        unread_count=Count('messages', filter=Q(messages__receiver=request.user, messages__is_read=False))
    ).order_by('-last_message_time')
    
    # Paginare
    paginator = Paginator(conversations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Adaugă participantul pentru fiecare conversație
    for conversation in page_obj:
        conversation.other_participant = conversation.get_other_participant(request.user)
    
    # Calculăm numărul total de mesaje necitite
    total_unread = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    
    context = {
        'page_obj': page_obj,
        'total_unread': total_unread,
    }
    
    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Afișează detaliile unei conversații și permite trimiterea de mesaje"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        is_active=True
    )
    
    # Verifică dacă utilizatorul face parte din conversație
    if request.user not in [conversation.buyer, conversation.seller]:
        messages.error(request, 'Nu ai acces la această conversație.')
        return redirect('conversation_list')
    
    # Marchează toate mesajele ca citite pentru utilizatorul curent
    unread_messages = conversation.messages.filter(
        receiver=request.user,
        is_read=False
    )
    for message in unread_messages:
        message.mark_as_read()
    
    # Obține toate mesajele din conversație
    conversation_messages = conversation.messages.all().order_by('created_at')
    
    # Procesează formularul de mesaj nou
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.receiver = conversation.get_other_participant(request.user)
            message.save()
            
            # Actualizează timestamp-ul conversației
            conversation.updated_at = timezone.now()
            conversation.save()
            
            # Creează notificare pentru destinatar
            MessageNotification.objects.get_or_create(
                user=message.receiver,
                message=message
            )
            
            # Trimite notificare email
            send_new_message_notification(message)
            
            messages.success(request, 'Mesajul a fost trimis cu succes!')
            
            # Pentru AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Mesajul a fost trimis cu succes!',
                    'message_html': render(request, 'messaging/message_bubble.html', {
                        'message': message,
                        'user': request.user
                    }).content.decode('utf-8')
                })
            
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    # Calculează participantul din cealaltă parte
    other_participant = conversation.get_other_participant(request.user)
    
    context = {
        'conversation': conversation,
        'messages': conversation_messages,
        'form': form,
        'other_participant': other_participant,
        'listing': conversation.listing,
    }
    
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def start_conversation(request, listing_id):
    """Începe o conversație nouă despre un anunț"""
    listing = get_object_or_404(Listing, id=listing_id, status='active')
    
    # Verifică că utilizatorul nu încearcă să inițieze o conversație cu el însuși
    if listing.owner == request.user:
        messages.error(request, 'Nu poți iniția o conversație cu tine însuți.')
        return redirect('listing_detail', slug=listing.slug)
    
    # Verifică dacă există deja o conversație
    existing_conversation = Conversation.objects.filter(
        listing=listing,
        buyer=request.user,
        seller=listing.owner
    ).first()
    
    if existing_conversation:
        return redirect('conversation_detail', conversation_id=existing_conversation.id)
    
    if request.method == 'POST':
        form = QuickMessageForm(request.POST)
        if form.is_valid():
            # Creează conversația
            conversation = Conversation.objects.create(
                listing=listing,
                buyer=request.user,
                seller=listing.owner
            )
            
            # Creează primul mesaj
            message_content = form.cleaned_data['final_message']
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                receiver=listing.owner,
                content=message_content
            )
            
            # Creează notificare
            MessageNotification.objects.create(
                user=listing.owner,
                message=message
            )
            
            # Trimite notificare email
            send_new_message_notification(message)
            
            messages.success(request, 'Conversația a fost inițiată cu succes!')
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = QuickMessageForm()
    
    context = {
        'form': form,
        'listing': listing,
    }
    
    return render(request, 'messaging/start_conversation.html', context)


@login_required
@require_POST
def mark_messages_read(request, conversation_id):
    """Marchează toate mesajele din conversație ca citite (AJAX)"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        is_active=True
    )
    
    if request.user not in [conversation.buyer, conversation.seller]:
        return JsonResponse({'success': False, 'error': 'Acces interzis'})
    
    # Marchează mesajele ca citite
    unread_messages = conversation.messages.filter(
        receiver=request.user,
        is_read=False
    )
    
    for message in unread_messages:
        message.mark_as_read()
    
    return JsonResponse({
        'success': True,
        'unread_count': 0
    })


@login_required
def get_unread_count(request):
    """Returnează numărul de mesaje necitite (AJAX pentru notificări)"""
    unread_count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    
    # Obține și ultimele notificări
    recent_notifications = MessageNotification.objects.filter(
        user=request.user,
        is_read=False
    )[:5]
    
    notifications_data = []
    for notification in recent_notifications:
        notifications_data.append({
            'id': notification.id,
            'sender': notification.message.sender.username,
            'listing_title': notification.message.conversation.listing.title,
            'message_preview': notification.message.content[:50] + '...' if len(notification.message.content) > 50 else notification.message.content,
            'created_at': notification.created_at.strftime('%H:%M'),
            'conversation_id': notification.message.conversation.id,
        })
    
    return JsonResponse({
        'unread_count': unread_count,
        'notifications': notifications_data
    })


@login_required
def delete_conversation(request, conversation_id):
    """Șterge o conversație (doar pentru utilizatorul curent)"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        is_active=True
    )
    
    if request.user not in [conversation.buyer, conversation.seller]:
        messages.error(request, 'Nu ai acces la această conversație.')
        return redirect('conversation_list')
    
    if request.method == 'POST':
        # În loc să ștergi complet, poți marca conversația ca inactivă pentru utilizatorul curent
        # Pentru simplitate, vom dezactiva conversația complet
        conversation.is_active = False
        conversation.save()
        
        messages.success(request, 'Conversația a fost ștearsă.')
        return redirect('conversation_list')
    
    context = {
        'conversation': conversation,
    }
    
    # Adaugă participantul pentru template
    conversation.other_participant = conversation.get_other_participant(request.user)
    
    return render(request, 'messaging/delete_conversation.html', context)
