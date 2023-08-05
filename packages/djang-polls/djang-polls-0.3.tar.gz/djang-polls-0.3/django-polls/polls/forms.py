from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Name", max_length=24)
    password = forms.CharField(label="Password", max_length=128,
                               widget=forms.PasswordInput())
