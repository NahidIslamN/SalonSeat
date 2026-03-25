from rest_framework.permissions import BasePermission



class IsSalunOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            bool(user and user.is_authenticated)
            and getattr(user, "user_role", None) == "salon_owner"
        )


class IsProfissional(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            bool(user and user.is_authenticated)
            and getattr(user, "user_role", None) == "professional"
        )