import logging

from rest_framework import generics, authentication
from oauth2_provider.contrib import rest_framework

from litterassessment.permissions import CanTriggerInferencePermissions
from litterassessment.api.serializers import InferenceSerializer
from litterassessment.models import Inference

logger = logging.getLogger(__name__)


class InferenceList(generics.ListCreateAPIView):
    queryset = Inference.objects.all()
    serializer_class = InferenceSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
        rest_framework.OAuth2Authentication,
    ]
    permission_classes = [CanTriggerInferencePermissions]

    def filter_queryset(self, queryset):
        user = self.request.user
        group_ids = user.groups.values_list("id", flat=True)
        return queryset.filter(group_id__in=set(group_ids))

    # TODO Set target group on a triggered inference and filter on group permissions