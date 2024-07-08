import json
import logging

from django.conf import settings
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from django.contrib.auth.decorators import login_required

from geonode.base.models import ResourceBase
from geonode.utils import (
    http_client,
)

from .apps import LITTERASSESSMENT_MODEL_API


logger = logging.getLogger(__name__)


@login_required
def forward_request(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception as e:
            logger.debug("Invalid JSON payload!", e)
            return HttpResponseBadRequest()

        if "pk" not in payload:
            return HttpResponseBadRequest("Missing pk of resource")

        # check user permissions before forwarding request
        resource = ResourceBase.objects.get(pk=payload["pk"]).get_self_resource()
        if not request.user.has_perm("base.view_resourcebase", resource):
            return HttpResponseForbidden()
        # remove pk before forwarding request
        payload.pop("pk")

        data = json.dumps(payload)
        headers = {"Content-Type": "application/json"}

        api_url = getattr(settings, LITTERASSESSMENT_MODEL_API)
        response, content = http_client.post(api_url, headers=headers, data=data)
        if not response:
            logger.warn(f"No connection to AI service API! -> {api_url} [headers={headers}][data={data}]")
            return HttpResponseServerError("Could not connect to backend service!")

        if response.status_code == 200:
            return JsonResponse(content)
        else:
            logger.warn(f"Could not process request! -> {content}")
            return HttpResponseServerError("Error processing request.")
    else:
        return HttpResponseNotAllowed()
