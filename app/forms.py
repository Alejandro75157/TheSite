from django import forms
from app.models import Message


class MessageForm(forms.ModelForm):
    author = forms.CharField(widget=forms.HiddenInput)
    date = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(max_length=50)
    text = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'rows':2,'cols':40}))

    class Meta:
        model = Message