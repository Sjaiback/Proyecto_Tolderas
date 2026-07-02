from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import UserProfile


def user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return UserProfile.Role.GENERAL_ADMIN
    profile = getattr(user, "profile", None)
    return profile.role if profile else None


def role_required(*allowed_roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role = user_role(request.user)
            if role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def is_general_admin(user):
    return user.is_authenticated and user.username == settings.OWNER_USERNAME


def owner_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_general_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


def can_manage_business(user):
    return user_role(user) in {UserProfile.Role.GENERAL_ADMIN, UserProfile.Role.OPERATOR}
