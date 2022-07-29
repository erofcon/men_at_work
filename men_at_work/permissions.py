from rest_framework.permissions import BasePermission


class UserHasAccess(BasePermission):
    """
    Checking the user for data access
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.creator == request.user or
            obj.executor == request.user or
            request.user.is_superuser and
            request.user.is_authenticated
        )


class UserCanCreate(BasePermission):
    """
    Checking the user for the possibility of creating
    """

    def has_permission(self, request, view):

        return bool(
            request.user.is_creator and
            request.user.is_authenticated
        )


class UserCanAnswer(BasePermission):
    """
    Checking the user for the possibility of a response
    """

    def has_permission(self, request, view):

        return bool(
            request.user.is_executor and
            request.user.is_authenticated
        )


class UserCanView(BasePermission):
    """
    Checking the user for data access
    """

    def has_permission(self, request, view):

        return bool(
            request.user.is_superuser or
            request.user.is_creator and
            request.user.is_authenticated
        )

