from django.contrib import admin
from .models import Participant, AcademicIntern

# Register your models here.


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "cpf", "phone"]


class SuapUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "cpf", "phone"]


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(AcademicIntern, SuapUserAdmin)
