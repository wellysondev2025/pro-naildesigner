from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsNailDesignerOrReadOnly(BasePermission):
    """
    Permite leitura a qualquer um, mas escrita apenas para Nail Designer.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_nail_designer
