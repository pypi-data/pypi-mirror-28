class BasePermission:
    """
    All permission classes should inherit from this class.
    Override message to customize the message associated with the exception.
    """

    message = None

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted else false.
        """

        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted else false.
        """

        return True
