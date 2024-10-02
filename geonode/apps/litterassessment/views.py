import json
import logging

from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from django.contrib.auth.decorators import (
    login_required, 
    permission_required,
)

from geonode.base.models import ResourceBase
from geonode.utils import (
    http_client,
)

from .apps import LITTERASSESSMENT_MODEL_API


logger = logging.getLogger(__name__)


def _forward(method, url, headers={}, data=None):
    response, content = http_client.request(
        url, method, data=data, headers=headers, verify=False
    )
    if not response:
        logger.warning(
            f"""Error on connecting backend service! -> {url}
            [headers={headers}]
            [data={data}]"""
        )
        if response == None:
            logger.error("Empty response received!")
        response = HttpResponse(response.content)
        response.status_code = response.status_code
        return response
        # return response

    if response.status_code == 200:
        return response
    else:
        logger.warning(f"Could not process request! -> {content}")
        return HttpResponseServerError("Error processing request.")


@login_required
@permission_required("litterassessment.can_trigger_inference", raise_exception=True)
def forward_request(request, path):
    api_url = getattr(settings, LITTERASSESSMENT_MODEL_API)
    url = url = f"{api_url}/{path}"
    if request.method == "GET":
        headers = {"Accept": "application/json"}
        response = _forward("GET", url=url, headers=headers)
        return JsonResponse(response.json())
    elif request.method == "POST":
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

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = json.dumps(payload)
        response = _forward("POST", url=url, headers=headers, data=data)
        return JsonResponse(response.json())

    else:
        return HttpResponseNotAllowed()
