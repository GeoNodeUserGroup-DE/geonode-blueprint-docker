
from geonode.base.api.serializers import user_serializer, DynamicModelSerializer

from rest_framework import serializers

from litterassessment.models import Inference


class InferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inference
        fields = (
            "pk",
            "started",
            "updated",
            "ended",
            "details",
            "initiator",
            "group",
            "status",
        )