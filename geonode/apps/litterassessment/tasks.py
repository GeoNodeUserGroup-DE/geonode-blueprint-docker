import json
import logging

from django.utils import timezone
from geonode.utils import http_client
from geonode.celery_app import app
from celery import shared_task

from litterassessment.models import Inference

logger = logging.getLogger(__name__)

QUEUE = "geonode"

POLLABLE_STATES = [
    Inference.Status.PENDING,
    Inference.Status.RUNNING,
]

@app.task(queue=QUEUE)
def poll_inference_status():
    inferences = Inference.objects.filter(status__in = POLLABLE_STATES)
    for inference in inferences:
        url = inference.job_url
        response, _ = http_client.get(url)
        inference.updated = timezone.now()
        
        if response.status_code == 404:
            inference.status = Inference.Status.DELETED
        elif response:
            content = response.json()
            status = content["status"]
            message = content["msg"]
            
            try:
                inference_status = Inference.Status[status.upper()]
                if inference_status in POLLABLE_STATES:
                    inference.finish(inference_status, message)
            except KeyError:
                logger.error(f"Received unknown status: '{status}'")
            inference.details = message
            
        else:
            logging.error(f"Error polling inference status of '{inference.job_url}'")
        
        inference.save()