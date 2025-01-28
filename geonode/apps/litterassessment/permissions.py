from rest_framework.permissions import BasePermission

class CanTriggerInferencePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("litterassessment.can_trigger_inference")
    