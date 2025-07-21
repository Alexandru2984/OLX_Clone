from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from .forms import UserProfileForm, CustomUserCreationForm, CustomPasswordChangeForm
from .models import EmailConfirmation
from .utils import send_confirmation_email

def register(request):
    """Înregistrarea unui utilizator nou"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Trimite email de confirmare
            if send_confirmation_email(user, request):
                messages.success(request, 
                    'Contul a fost creat cu succes! Verifică-ți email-ul pentru a confirma adresa.')
            else:
                messages.warning(request, 
                    'Contul a fost creat, dar a apărut o problemă la trimiterea email-ului de confirmare.')
            
            return redirect('login')
        else:
            # Adaugă un mesaj general pentru erori
            messages.error(request, 
                'Au fost găsite erori în formular. Te rog să le corectezi și să încerci din nou.')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    """Pagina de profil a utilizatorului"""
    user_profile = request.user.profile
    context = {'user_profile': user_profile}
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Editarea profilului utilizatorului"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            old_email = request.user.email
            new_email = form.cleaned_data['email']
            
            form.save()
            
            # Verifică dacă email-ul s-a schimbat
            if old_email != new_email:
                # Trimite email de confirmare pentru noua adresă
                if send_confirmation_email(request.user, request):
                    messages.success(request, 
                        'Profilul a fost actualizat cu succes! '
                        'Un email de confirmare a fost trimis la noua adresă de email.')
                else:
                    messages.warning(request, 
                        'Profilul a fost actualizat, dar a apărut o problemă la trimiterea email-ului de confirmare.')
            else:
                messages.success(request, 'Profilul a fost actualizat cu succes!')
            
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)


def confirm_email(request, token):
    """Confirmă email-ul utilizatorului folosind token-ul"""
    try:
        confirmation = get_object_or_404(EmailConfirmation, token=token)
        
        if confirmation.is_confirmed:
            messages.info(request, 'Email-ul tău a fost deja confirmat.')
            return redirect('login')
        
        if confirmation.is_expired():
            messages.error(request, 
                'Link-ul de confirmare a expirat. Te rugăm să soliciti un nou email de confirmare.')
            return redirect('resend_confirmation')
        
        # Confirmă email-ul
        confirmation.confirm()
        messages.success(request, 
            'Email-ul a fost confirmat cu succes! Acum te poți conecta.')
        return redirect('login')
        
    except Http404:
        messages.error(request, 'Link de confirmare invalid.')
        return redirect('home')


@login_required
def resend_confirmation(request):
    """Retrimite email-ul de confirmare"""
    if request.user.email_confirmation.is_confirmed:
        messages.info(request, 'Email-ul tău este deja confirmat.')
        return redirect('profile')
    
    if request.method == 'POST':
        if send_confirmation_email(request.user, request):
            messages.success(request, 
                'Email-ul de confirmare a fost retrimis. Verifică-ți inbox-ul.')
        else:
            messages.error(request, 
                'A apărut o problemă la trimiterea email-ului. Te rugăm să încerci din nou.')
        return redirect('profile')
    
    return render(request, 'accounts/resend_confirmation.html')


def email_confirmation_sent(request):
    """Pagina care confirmă că email-ul a fost trimis"""
    return render(request, 'accounts/email_confirmation_sent.html')


@login_required
def change_password(request):
    """Schimbarea parolei utilizatorului"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parola a fost schimbată cu succes!')
            return redirect('profile')
        else:
            messages.error(request, 'Te rugăm să corectezi erorile din formular.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)
