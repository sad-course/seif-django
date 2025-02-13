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
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "(XX)XXXX-XXXX"}),
    )
    cpf = forms.CharField(
        label="cpf",
        max_length=20,
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
