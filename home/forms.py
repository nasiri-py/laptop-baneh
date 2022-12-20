from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    subject = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': '8', 'required': 'true'}))
