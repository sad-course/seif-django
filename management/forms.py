import datetime
from django import forms
from django.core.exceptions import ValidationError


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
    titulo = forms.CharField(max_length=100)
    descricao = forms.CharField(widget=forms.Textarea)
    inicio = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fim = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    horario_inicio = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    status_inicial = forms.ChoiceField(
        choices=[("ativo", "Ativo"), ("inativo", "Inativo")]
    )
    tags = forms.CharField(max_length=100)
    campus = forms.ChoiceField(
        choices=[("IFRN - campus Pau dos Ferros", "IFRN - campus Pau dos Ferros")]
    )
    organizadores = forms.EmailField()
    imagem = forms.FileField(required=True)
    solicitacao = forms.BooleanField(
        initial=False, required=False, widget=forms.HiddenInput()
    )  # Campo oculto

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicando classes CSS e placeholders aos campos
        self.fields["titulo"].widget = forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "Título do evento",
            }
        )
        self.fields["descricao"].widget = forms.Textarea(
            attrs={
                "class": "w-full h-36 rounded-lg bg-gray-100",
                "placeholder": "Descrição do evento",
            }
        )
        self.fields["inicio"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full  rounded-lg bg-gray-100 text-gray-400",
            }
        )
        self.fields["fim"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-lg bg-gray-100 text-gray-400",
            }
        )
        self.fields["horario_inicio"].widget = forms.TimeInput(
            attrs={
                "type": "time",
                "class": "w-full rounded-lg bg-gray-100 text-gray-400",
            }
        )
        self.fields["status_inicial"].widget = forms.Select(
            attrs={"class": "w-full rounded-lg bg-gray-100"}
        )
        self.fields["tags"].widget = forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "ex: tecnologia, inovação",
            }
        )
        self.fields["campus"].widget = forms.Select(
            attrs={"class": "w-full rounded-lg bg-gray-100"}
        )
        self.fields["organizadores"].widget = forms.EmailInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-100",
                "placeholder": "fulano@gmail.com",
            }
        )
        self.fields["imagem"].widget = forms.FileInput(attrs={"class": "hidden h-full"})

    def clean_inicio(self):
        inicio = self.cleaned_data["inicio"]
        if inicio < datetime.date.today():
            raise ValidationError(
                "A data de início não pode ser anterior à data de hoje."
            )
        return inicio

    def clean_fim(self):
        fim = self.cleaned_data["fim"]
        inicio = self.cleaned_data.get(
            "inicio"
        )  # Usando get() para evitar erro se 'inicio' for inválido
        if inicio and fim < inicio:
            raise ValidationError(
                "A data de fim não pode ser anterior à data de início."
            )
        return fim

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

    def clean_imagem(self):
        imagem = self.cleaned_data.get("imagem")
        if imagem:
            # Verificar tamanho da imagem
            if imagem.size > 5 * 1024 * 1024:  # Limite de 5MB
                raise ValidationError("A imagem não pode exceder 5MB.")
            # Verificar tipo de arquivo (imagem)
            valid_extensions = [".jpg", ".jpeg", ".png"]
            if not any(imagem.name.endswith(ext) for ext in valid_extensions):
                raise ValidationError("A imagem deve ser no formato JPG, JPEG ou PNG.")
        return imagem

    def clean_status_inicial(self):
        status_inicial = self.cleaned_data["status_inicial"]
        if status_inicial not in ["ativo", "inativo"]:
            raise ValidationError("Status inválido.")
        return status_inicial

    def clean_organizadores(self):
        organizadores = self.cleaned_data["organizadores"]
        # Se houver mais de um organizador, os e-mails devem ser separados por vírgula
        organizadores = organizadores.split(",")
        for email in organizadores:
            email = email.strip()
            if not forms.EmailField().clean(email):
                raise ValidationError(f"O e-mail '{email}' é inválido.")
        return organizadores

    def clean_campus(self):
        campus = self.cleaned_data["campus"]
        # Verificar se o campus é válido
        valid_campus = ["IFRN - campus Pau dos Ferros"]
        if campus not in valid_campus:
            raise ValidationError("Campus inválido.")
        return campus


class ActivityForm(forms.Form):
    titulo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "w-full border rounded px-3 py-2 \
                    focus:outline-none focus:ring focus:border-green-800",
                "placeholder": "Título da atividade",
            }
        ),
    )
    descricao = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800",
                "rows": 4,
                "placeholder": "Descrição da atividade",
            }
        )
    )
    inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800",
            }
        )
    )
    fim = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800",
            }
        )
    )
    horario_inicio = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800",
            }
        )
    )
    tipo = forms.ChoiceField(
        choices=[("", "Selecione"), ("opcao1", "Opção 1"), ("opcao2", "Opção 2")],
        widget=forms.Select(
            attrs={
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800"
            }
        ),
    )
    responsaveis = forms.MultipleChoiceField(
        choices=[
            ("1", "Fulano da Silva")
        ],  # Substituir por dados dinâmicos se necessário
        widget=forms.SelectMultiple(
            attrs={
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800 h-[42px]"
            }
        ),
    )
    horas_previstas = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "w-full border rounded px-3 py-2 focus:outline-none \
                    focus:ring focus:border-green-800",
                "placeholder": "X horas",
            }
        ),
    )

    def clean_inicio(self):
        inicio = self.cleaned_data["inicio"]
        if inicio < datetime.date.today():
            raise ValidationError("A data de início não pode ser anterior a hoje.")
        return inicio

    def clean_fim(self):
        fim = self.cleaned_data["fim"]
        inicio = self.cleaned_data.get("inicio")
        if inicio and fim < inicio:
            raise ValidationError(
                "A data de fim não pode ser anterior à data de início."
            )
        return fim
