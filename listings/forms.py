from django import forms
from django.forms import inlineformset_factory
from .models import Listing, ListingImage
from categories.models import Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'price', 'condition', 'category',
            'city', 'county', 'phone', 'email', 'is_negotiable'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titlul anunțului'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descrierea detaliată a produsului'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Preț în LEI'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'București'
            }),
            'county': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Județul'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+40 123 456 789'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplu.ro'
            }),
            'is_negotiable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afișez categoriile ierarhic
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Selectează categoria"
        
        # Fac email-ul opțional vizual
        self.fields['email'].required = False


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image', 'alt_text', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrierea imaginii'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# Formset pentru multiple imagini
ListingImageFormSet = inlineformset_factory(
    Listing,
    ListingImage,
    form=ListingImageForm,
    extra=5,  # Numărul de forme goale afișate
    max_num=10,  # Maxim 10 imagini
    can_delete=True
)
