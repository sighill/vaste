from django import forms
from .models import pj_note , pnj

class pj_note_form(forms.Form):
	note = forms.CharField(widget=forms.Textarea(), label='')

# attrs={'cols':2000 , 'height':48}