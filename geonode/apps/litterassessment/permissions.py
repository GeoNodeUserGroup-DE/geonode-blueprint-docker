from rest_framework.permissions import BasePermission

class CanTriggerInferencePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("litterassessment.can_trigger_inference")

class HasGroupAccess(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.groups.exists()

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.groups.filter(id=obj.group.id).exists()
