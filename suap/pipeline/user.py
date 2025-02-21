import logging
import requests

from social_core.pipeline.user import USER_FIELDS
from django.core.files.base import ContentFile
from accounts.models import AcademicIntern

logger = logging.getLogger(__name__)


def download_image_suap(image_url, user_identification):
    try:
        response = requests.get(image_url, timeout=1)
        response.raise_for_status()
        if response.status_code == 200:
            file_object = ContentFile(
                content=response.content, name=f"avatar_{user_identification}.jpeg"
            )
            return file_object
    except (
        requests.ConnectionError,
        requests.Timeout,
        requests.HTTPError,
    ) as exception:
        logger.exception(
            "An error occurred while downloading the SUAP user image. Exception: %s, Status: %s",
            str(exception),
            getattr(response, "status_code", "N/A"),
        )
    return None


def save_suap_user(strategy, details, response, backend, *args, **kwargs):
    """Save SUAP user data to a custom model instead of AUTH_USER_MODEL
    only for SuapOAuth2 backend."""
    if backend.name == "suap":
        suap_id = response.get("identificacao")
        user_type = response.get("tipo_usuario")

        fields = {
            name: kwargs.get(name, details.get(name))
            for name in backend.setting("USER_FIELDS", USER_FIELDS)
        }
        if not fields:
            return None

        user_image_file_object = download_image_suap(
            image_url=details.get("image"), user_identification=suap_id
        )

        fields.update({"avatar": user_image_file_object})
        if backend.setting("FORCE_EMAIL_LOWERCASE", False):
            emailfield = fields.get("email")
            if emailfield:
                fields["email"] = emailfield.lower()

        user, created = AcademicIntern.objects.get_or_create(
            registration_number=suap_id,
            association_type=user_type,
            defaults={**fields},
        )
        if user and not user.password:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        if created:
            return {"is_new": True, "user": user}

        return {"is_new": False}
    return {}
