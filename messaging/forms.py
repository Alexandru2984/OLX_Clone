from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """Formular pentru trimiterea de mesaje"""
    
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Scrie mesajul tău aici...',
                'maxlength': 1000,
            })
        }
        labels = {
            'content': ''
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True


class QuickMessageForm(forms.Form):
    """Formular rapid pentru inițierea unei conversații"""
    
    QUICK_MESSAGES = [
        ('', 'Selectează un mesaj prestabilit'),
        ('interested', 'Sunt interessat de acest anunț. Mai este disponibil?'),
        ('price_question', 'Care este ultimul preț pentru acest produs?'),
        ('details', 'Aș dori mai multe detalii despre produs.'),
        ('meeting', 'Când și unde putem să ne întâlnim pentru a vedea produsul?'),
        ('condition', 'Poți să îmi spui mai multe despre starea produsului?'),
        ('custom', 'Mesaj personalizat'),
    ]
    
    message_type = forms.ChoiceField(
        choices=QUICK_MESSAGES,
        widget=forms.Select(attrs={
            'class': 'form-control mb-2',
            'id': 'quick-message-select'
        }),
        required=False
    )
    
    custom_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Scrie mesajul tău aici...',
        }),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        message_type = cleaned_data.get('message_type')
        custom_message = cleaned_data.get('custom_message')
        
        if message_type == 'custom' and not custom_message:
            raise forms.ValidationError('Te rog să scrii un mesaj personalizat.')
        
        if message_type and message_type != 'custom' and message_type != '':
            # Setăm mesajul prestabilit
            quick_messages_dict = {
                'interested': 'Sunt interessat de acest anunț. Mai este disponibil?',
                'price_question': 'Care este ultimul preț pentru acest produs?',
                'details': 'Aș dori mai multe detalii despre produs.',
                'meeting': 'Când și unde putem să ne întâlnim pentru a vedea produsul?',
                'condition': 'Poți să îmi spui mai multe despre starea produsului?',
            }
            cleaned_data['final_message'] = quick_messages_dict.get(message_type, '')
        elif message_type == 'custom':
            cleaned_data['final_message'] = custom_message
        else:
            raise forms.ValidationError('Te rog să selectezi un tip de mesaj.')
        
        return cleaned_data
