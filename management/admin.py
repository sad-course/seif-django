from django.contrib import admin
from .models import Activity, Tag, Event, Certificate


# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tag_id",
    )
    fields = ("name",)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
        "banner",
        "campus",
        "description",
        "created_by",
    )
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "init_date",
        "end_date",
    )
    fields = (
        "event",
        "title",
        "init_date",
        "end_date",
        "instructor",
        "description",
    )


class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "activity",
        "created_at",
    )
    fields = (
        "activity",
        "created_at",
    )
    readonly_fields = ("created_at",)


admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Certificate, CertificateAdmin)
