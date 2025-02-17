from social_core.pipeline.user import USER_FIELDS
from accounts.models import AcademicIntern


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

        if backend.setting("FORCE_EMAIL_LOWERCASE", False):
            emailfield = fields.get("email")
            if emailfield:
                fields["email"] = emailfield.lower()

        user, created = AcademicIntern.objects.get_or_create(
            registration_number=suap_id,
            association_type=user_type,
            defaults={**fields},
        )
        if created:
            return {"is_new": False}

        return {"is_new": True, "user": user}

    return {}
