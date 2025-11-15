def has_role(user, role_name):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == role_name
    )
