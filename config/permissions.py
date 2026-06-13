from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allows access only to users flagged ``is_admin`` (our own flag, since
    AppUser has no Django ``is_staff``)."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_admin', False)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Anyone can read (GET/HEAD/OPTIONS); only users flagged ``is_admin``
    may create, edit or delete. Shared by every admin-managed resource
    (services, emergency hotlines) so the rule stays consistent."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_admin', False)
        )

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Anyone can read, owners can edit/delete, admins can edit/delete."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and getattr(request.user, 'is_admin', False):
            return True
        # For User objects, obj might be the user itself; for reviews, obj.user_id
        owner_id = getattr(obj, 'user_id', getattr(obj, 'pk', None))
        return owner_id == request.user.pk
