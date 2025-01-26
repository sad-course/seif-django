from django.contrib import admin
from .models import Participant, Teste


# Register your models here.
class TesteAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "cpf"]


admin.site.register(Teste, TesteAdmin)
admin.site.register(Participant)
