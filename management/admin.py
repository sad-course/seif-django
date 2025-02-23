from django.contrib import admin
from accounts.views import create_certificate
from .models import Activity, Tag, Event, Certificate


# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tag_id",
    )
    fields = ("name",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "init_date", "end_date", "status", "campus")
    fields = (
        "title",
        "init_date",
        "end_date",
        "campus",
        "status",
        "tags",
        "banner",
        "description",
        "created_by",
        "organizers",
    )
    readonly_fields = ("created_by",)
    list_filter = ("status", "campus")
    search_fields = ("title", "status", "campus", "created_by__email")

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "init_date",
        "end_date",
        "event",
        "instructor",
        "is_active",
    )
    fields = (
        "event",
        "title",
        "init_date",
        "end_date",
        "instructor",
        "description",
        "capacity",
        "activity_type",
        "is_active",
    )
    list_filter = ("is_active", "event")
    search_fields = ("title", "instructor")


class CertificateAdmin(admin.ModelAdmin):
    list_display = ("activity", "created_at", "participant")
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        if not obj.image:
            image_file = create_certificate(
                obj.participant.username, obj.activity.title
            )
            obj.image = image_file
        super().save_model(request, obj, form, change)


admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Certificate, CertificateAdmin)
