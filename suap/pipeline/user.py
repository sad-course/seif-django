from accounts.models import AcademicIntern


def save_suap_user(strategy, details, response, backend, *args, **kwargs):
    """Save SUAP user data to a custom model instead of AUTH_USER_MODEL
    only for SuapOAuth2 backend."""

    if backend.name == "suap":
        suap_id = response.get("identificacao")
        email = response.get("email")
        first_name, last_name = (
            response["nome"].split()[0],
            response["nome"].split()[-1],
        )

        # Save to SuapUser model
        user, __ = AcademicIntern.objects.get_or_create(
            registration_number=suap_id,
            defaults={
                "username": first_name,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        return {"suap_user": user}

    return {}
