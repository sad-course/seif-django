import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Event


class EventPublishRequestForm(forms.Form):
    local = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "IFRN - Pau dos Ferros",
            }
        ),
    )
    cargo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "ex: Professor, Aluno",
            }
        ),
    )
    nome = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "Nome do evento",
            }
        ),
    )
    tipo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "ex: Comemorativo, Tecnólogico, Acadêmico",
            }
        ),
    )
    descricao = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full h-24 rounded-lg bg-gray-100",
                "placeholder": "Breve descrição do evento",
            }
        )
    )
    solicitacao = forms.BooleanField(
        initial=False, required=False, widget=forms.HiddenInput()
    )

    def clean_nome(self):
        nome = self.cleaned_data.get("nome", "").strip()
        if not nome:
            raise ValidationError("O nome do evento não pode estar vazio.")
        return nome

    def clean_descricao(self):
        descricao = self.cleaned_data.get("descricao", "").strip()
        if not descricao:
            raise ValidationError("A descrição do evento não pode estar vazia.")
        return descricao


class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    init_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    init_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    initial_status = forms.ChoiceField(choices=[("rascunho", "Rascunho")])
    tags = forms.CharField(max_length=100)
    campus = forms.ChoiceField(choices=Event.Campus.choices)
    organizers = forms.EmailField()
    banner = forms.FileField(required=True)
    solicitation = forms.BooleanField(
        initial=False, required=False, widget=forms.HiddenInput()
    )  # Campo oculto

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicando classes CSS e placeholders aos campos
        self.fields["title"].widget = forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "Título do evento",
            }
        )
        self.fields["description"].widget = forms.Textarea(
            attrs={
                "class": "w-full h-36 rounded-lg bg-gray-100",
                "placeholder": "Descrição do evento",
            }
        )
        self.fields["init_date"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full  rounded-lg bg-gray-100 text-gray-400",
            }
        )
        self.fields["end_date"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-lg bg-gray-100 text-gray-400",
            }
        )
        self.fields["init_time"].widget = forms.TimeInput(
            attrs={
                "type": "time",
                "class": "w-full rounded-lg bg-gray-100 text-gray-400",
            }
        )
        self.fields["initial_status"].widget = forms.Select(
            attrs={"class": "w-full rounded-lg bg-gray-100"}
        )
        self.fields["tags"].widget = forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "ex: tecnologia, inovação",
                "data-role": "tagsinput",
            }
        )
        self.fields["campus"].widget = forms.Select(
            attrs={"class": "w-full rounded-lg bg-gray-100"}
        )
        self.fields["organizers"].widget = forms.EmailInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "fulano@gmail.com",
            }
        )
        self.fields["banner"].widget = forms.FileInput(attrs={"class": "hidden h-full"})

    def clean_init_date(self):
        init_date = self.cleaned_data["init_date"]
        if init_date < datetime.date.today():
            raise ValidationError(
                "A data de início não pode ser anterior à data de hoje."
            )
        return init_date

    def clean_end_date(self):
        end_date = self.cleaned_data["end_date"]
        inicio = self.cleaned_data.get("inicio")
        if inicio and end_date < inicio:
            raise ValidationError(
                "A data de fim não pode ser anterior à data de início."
            )
        return end_date

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "").strip()
        if not tags:
            raise ValidationError("As tags não podem estar vazias.")
        if any(char in tags for char in "!@#$%^&*()[]{};:/<>?\\|`~=_+"):
            raise ValidationError("As tags não podem conter caracteres especiais.")
        # Verifica se as tags são uma lista separada por vírgulas
        tags_list = tags.split(",")
        if len(tags_list) < 1:
            raise ValidationError("Deve haver pelo menos uma tag.")
        return tags

    def clean_banner(self):
        banner = self.cleaned_data.get("banner")
        if banner:
            # Verificar tamanho da banner
            if banner.size > 5 * 1024 * 1024:  # Limite de 5MB
                raise ValidationError("A imagem não pode exceder 5MB.")
            # Verificar tipo de arquivo (imagem)
            valid_extensions = [".jpg", ".jpeg", ".png"]
            if not any(banner.name.endswith(ext) for ext in valid_extensions):
                raise ValidationError("A imagem deve ser no formato JPG, JPEG ou PNG.")
        return banner

    def clean_initial_status(self):
        inital_status = self.cleaned_data["initial_status"]
        if inital_status not in ["rascunho", "rascunho"]:
            raise ValidationError("Status inválido.")
        return inital_status

    def clean_organizers(self):
        organizers = self.cleaned_data["organizers"]
        # Se houver mais de um organizador, os e-mails devem ser separados por vírgula
        organizers = organizers.split(",")
        for email in organizers:
            email = email.strip()
            if not forms.EmailField().clean(email):
                raise ValidationError(f"O e-mail '{email}' é inválido.")
        return organizers


class ActivityForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 \
                    shadow-sm focus:border-green-500 focus:ring-green-500",
                "placeholder": "Título da atividade",
            }
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 \
                    shadow-sm focus:border-green-500 focus:ring-green-500",
                "rows": 4,
                "placeholder": "Descrição da atividade",
            }
        ),
    )
    init_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "mt-1 block w-full text-gray-400 rounded-md \
                    border-gray-300 shadow-sm focus:border-green-500 \
                        focus:ring-green-500",
            }
        ),
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "mt-1 block w-full text-gray-400 rounded-md \
                    border-gray-300 shadow-sm focus:border-green-500 \
                        focus:ring-green-500",
            }
        ),
    )
    init_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "mt-1 block w-full text-gray-400 rounded-md \
                    border-gray-300 shadow-sm focus:border-green-500 \
                        focus:ring-green-500",
            }
        ),
    )
    type = forms.ChoiceField(
        choices=[("", "Selecione"), ("opcao1", "Opção 1"), ("opcao2", "Opção 2")],
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full text-gray-400 rounded-md \
                    border-gray-300 shadow-sm focus:border-green-500 \
                        focus:ring-green-500",
            }
        ),
    )
    instructor = forms.MultipleChoiceField(
        choices=[("1", "Fulano da Silva")],
        widget=forms.SelectMultiple(
            attrs={
                "class": "mt-1 block w-full h-full text-gray-400 rounded-md \
                    border-gray-300 shadow-sm focus:border-green-500 \
                        focus:ring-green-500 text-gray",
            }
        ),
    )
    estimated_duration = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 \
                    shadow-sm focus:border-green-500 focus:ring-green-500",
                "placeholder": "X horas",
            }
        ),
    )

    def clean_init_date(self):
        init_date = self.cleaned_data["init_date"]
        if init_date < datetime.date.today():
            raise forms.ValidationError(
                "A data de início não pode ser anterior a hoje."
            )
        return init_date

    def clean_end_date(self):
        end_date = self.cleaned_data["end_date"]
        inicio = self.cleaned_data.get("inicio")
        if inicio and end_date < inicio:
            raise forms.ValidationError(
                "A data de fim não pode ser anterior à data de início."
            )
        return end_date
