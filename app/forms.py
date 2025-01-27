from django import forms
from .models import Note 

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note 
        fields = ['context', 'is_completed', 'is_pinned'] 
        widgets = {
            'context': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
