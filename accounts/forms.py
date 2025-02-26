import re
from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        label="email", widget=forms.TextInput(attrs={"placeholder": "Email"})
    )
    password = forms.CharField(
        min_length=6,
        label="email",
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )


class SignupForm(forms.Form):
    name = forms.CharField(
        label="name",
        max_length=70,
        min_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Nome"}),
    )
    email = forms.EmailField(
        label="email",
        max_length=140,
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"}),
    )
    checkPassword = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar senha"}),
    )
    phone = forms.CharField(
        label="phone",
        max_length=14,
        widget=forms.TextInput(attrs={"placeholder": "(XX)XXXX-XXXX"}),
    )
    cpf = forms.CharField(
        label="cpf",
        max_length=14,
        widget=forms.TextInput(attrs={"placeholder": "XXX.XXX.XXX-XX"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )
        self.fields["checkPassword"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )
        self.fields["cpf"].widget.attrs.update(
            {"class": "w-full rounded-lg bg-gray-200"}
        )

    def clean(self):
        cleaned_data = super().clean()

        cpf = self.cleaned_data.get("cpf")
        cleaned_cpf = re.sub(r"\D", "", cpf)

        if len(cleaned_cpf) != 11:
            self.add_error("cpf", "CPF inválido. Deve conter 11 dígitos.")
        else:
            cleaned_data["cpf"] = cleaned_cpf

        password = self.cleaned_data.get("password")
        check_password = self.cleaned_data.get("checkPassword")
        if password != check_password:
            self.add_error("password", "Senhas não coincidem")

        return cleaned_data
