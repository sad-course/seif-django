from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label="email")
    password = forms.CharField(label="email", widget=forms.PasswordInput())


class SignupForm(forms.Form):
    name = forms.CharField(label="name", max_length=70)
    email = forms.EmailField(label="email", max_length=140)
    password = forms.CharField(widget=forms.PasswordInput())
    checkPassword = forms.CharField(widget=forms.PasswordInput())
    phone = forms.CharField(label="phone", max_length=14)
    cpf = forms.CharField(label="cpf", max_length=16)
