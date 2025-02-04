from django.contrib import admin
from .models import Tag, Event


# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "tag_id",
        "name",
    )
    fields = ("name",)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "init_date",
        "end_date",
        "status",
    )
    fields = (
        "title",
        "init_date",
        "end_date",
        "status",
        "tags",
        "description",
    )


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "init_date",
        "end_date",
    )
    fields = (
        "title",
        "init_date",
        "end_date",
        "tags",
        "description",
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
