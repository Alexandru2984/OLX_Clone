from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """Formular personalizat pentru înregistrare cu validări îmbunătățite"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'adresa@email.com'
        }),
        help_text='Adresa de email pentru confirmare'
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nume utilizator'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Alege un nume de utilizator'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Alege o parolă sigură'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repetă parola'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f"Numele de utilizator '{username}' este deja folosit. "
                "Te rog să alegi un alt nume de utilizator."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f"Adresa de email '{email}' este deja înregistrată. "
                "Te rog să folosești o altă adresă de email sau să te conectezi."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = False  # Va fi activat după confirmarea email-ului
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    # Câmpuri din User
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prenumele'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numele'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplu.ro'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'phone', 'avatar', 'city', 'county', 'bio', 
            'email_notifications', 'phone_public'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+40 123 456 789'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'București'
            }),
            'county': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Județul'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Scrie câteva cuvinte despre tine...'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'phone_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Actualizez și câmpurile din User
            user = profile.user
            old_email = user.email
            new_email = self.cleaned_data['email']
            
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            
            # Dacă email-ul s-a schimbat, necesită reconfirmare
            if old_email != new_email:
                user.email = new_email
                # Marchează email-ul ca neconfirmat
                try:
                    if hasattr(user, 'email_confirmation'):
                        user.email_confirmation.is_confirmed = False
                        user.email_confirmation.save()
                except:
                    # Dacă nu există email_confirmation, îl creăm
                    from .models import EmailConfirmation
                    EmailConfirmation.objects.create(user=user)
            
            user.save()
            profile.save()
        return profile


class CustomPasswordResetForm(PasswordResetForm):
    """Formular personalizat pentru resetarea parolei"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresa ta de email',
            'autocomplete': 'email'
        }),
        help_text='Introdu adresa de email asociată contului tău'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Adresa de email"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Nu există niciun cont asociat cu această adresă de email."
            )
        return email


class CustomSetPasswordForm(SetPasswordForm):
    """Formular personalizat pentru setarea unei parole noi"""
    new_password1 = forms.CharField(
        label="Parola nouă",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introdu parola nouă',
            'autocomplete': 'new-password'
        }),
        help_text='Parola trebuie să conțină cel puțin 8 caractere și să nu fie prea comună.'
    )
    new_password2 = forms.CharField(
        label="Confirmă parola nouă",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmă parola nouă',
            'autocomplete': 'new-password'
        }),
        help_text='Introdu din nou parola pentru confirmare.'
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formular personalizat pentru schimbarea parolei"""
    old_password = forms.CharField(
        label="Parola curentă",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introdu parola curentă',
            'autocomplete': 'current-password'
        }),
        help_text='Introdu parola curentă pentru a o putea schimba.'
    )
    new_password1 = forms.CharField(
        label="Parola nouă",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introdu parola nouă',
            'autocomplete': 'new-password'
        }),
        help_text='Parola trebuie să conțină cel puțin 8 caractere și să nu fie prea comună.'
    )
    new_password2 = forms.CharField(
        label="Confirmă parola nouă",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmă parola nouă',
            'autocomplete': 'new-password'
        }),
        help_text='Introdu din nou parola pentru confirmare.'
    )
