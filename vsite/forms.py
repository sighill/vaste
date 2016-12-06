from django import forms
from .models import PjNote , Pnj

class PjNoteForm(forms.Form):
	note = forms.CharField(widget=forms.Textarea(), label='')