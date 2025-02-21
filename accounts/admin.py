from django.contrib import admin
from .models import Participant

# Register your models here.


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "cpf", "phone"]
    fields = ("username", "email")
    search_fields = ("username", "email")


admin.site.register(Participant, ParticipantAdmin)
