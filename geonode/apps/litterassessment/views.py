import json
import logging

from django.conf import settings
from django.http import (
    HttpResponseServerError,
    JsonResponse,
)

from geonode.base.models import ResourceBase
from geonode.utils import http_client

from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, APIException
from oauth2_provider.contrib import rest_framework

from litterassessment.models import Inference
from litterassessment.permissions import CanTriggerInferencePermissions
from litterassessment.apps import LITTERASSESSMENT_MODEL_API

logger = logging.getLogger(__name__)


def _forward_url(path):
    api_url = getattr(settings, LITTERASSESSMENT_MODEL_API)
    return f"{api_url}/{path}"


def _forward(method, path, headers={}, data=None):
    url = _forward_url(path)
    response, content = http_client.request(
        url, method, data=data, headers=headers, verify=False
    )
    status_code = response.status_code
    if not response:
        if status_code == 400:
            raise ValidationError(response.content)
        elif status_code == 404:
            raise NotFound(response.content)
        else:
            raise APIException(response.content)

    if status_code >= 200 and status_code < 400:
        return response
    else:
        logger.warning(f"Could not process request! -> {content}")
        return HttpResponseServerError("Error processing request.")

class ForwardToInferenceApi(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
        rest_framework.OAuth2Authentication,
    ]
    permission_classes = [
        CanTriggerInferencePermissions
    ]
    
    def get(self, request, path, format=None):
        if request.method == "GET":
            headers = {"Accept": "application/json"}
            response = _forward("GET", path, headers=headers)
            return JsonResponse(response.json())

    def post(self, request, path):
        if isinstance(request.data, dict):
            payload = request.data
        else:
            try:
                payload = json.loads(request.data)
            except Exception as e:
                logger.debug("Invalid JSON payload!", e)
                raise ValidationError("Invalid JSON payload!")

        if "pk" not in payload:
            raise ValidationError("Missing pk of resource")

        # check user permissions before forwarding request
        pk = payload["pk"]
        try:
            resource = ResourceBase.objects.get(pk=pk).get_self_resource()
            if not request.user.has_perm("base.view_resourcebase", resource):
                raise PermissionDenied("Invalid permissions to access resource!")
        except ResourceBase.DoesNotExist:
            raise ValidationError(f"Resource with id '{pk}' does not exist!")

        inference = Inference.objects.create(payload=payload, resource=resource)
        inference.group_id = payload["inferenceGroup"] if "inferenceGroup" in payload else None
        inference.initiator = request.user
        inference.save()

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = json.dumps(payload)
        response = _forward("POST", path, headers=headers, data=data)
        job = response.json()
        
        if response.status_code == 201:
            inference.job_url = response.headers["location"]
            status = job["status"]
            if status == "running":
                inference.set_running()
            else:
                message = job["msg"]
                inference.finish(Inference.Status.FAILED)
                inference.details(f"Job status: {status}, Details: '{message}'")
            inference.save()

        return JsonResponse(job)
