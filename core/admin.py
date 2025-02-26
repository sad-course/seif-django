from django.contrib import admin
from .models import EventSubscription

# Register your models here.


class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "participant",
        "activity",
        "is_checked_in",
    )


admin.site.register(EventSubscription, EventSubscriptionAdmin)
