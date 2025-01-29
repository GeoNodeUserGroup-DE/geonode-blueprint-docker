import logging 

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from geonode.base.models import ResourceBase
from geonode.groups.models import GroupProfile

logger = logging.getLogger(__name__)


class PermissionsModel(models.Model):
    """
    Auxiliary model to manage permissions without a database model.
    """
            
    class Meta:  # https://stackoverflow.com/a/37988537/2299448
        
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model. 
                
        permissions = ( 
            ("can_trigger_inference", "Can Trigger AI Inference",),
        )

class Inference(models.Model):
    """
    Tracks status of invoked AI inferences.
    """
    
    class Meta:
        verbose_name = "Invoked AI Inference"

    class Status(models.TextChoices):
        PENDING = "PENDING", _("pending")
        RUNNING = "RUNNING", _("running")
        FAILED = "FAILED", _("failed")
        CANCELLED = "CANCELLED", _("cacelled")
        COMPLETE = "COMPLETE", _("complete")
        DELETED = "DELETED", _("deleted")

    started = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ended = models.DateTimeField(null=True, blank=True)
    details = models.TextField(blank=True)
    job_url = models.URLField(blank=True)
    payload = models.JSONField(blank=True)
    group = models.ForeignKey(GroupProfile, related_name="inference_group", null=True, on_delete=models.CASCADE)
    resource = models.ForeignKey(ResourceBase, related_name="input_resource", on_delete=models.CASCADE)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # def cancel(self) -> None:
    #     if self.status in (self.Status.PENDING, self.Status.RUNNING):
    #         self.finish(self.Status.CANCELLED)
    #     else:
    #         logger.debug(f"AI inference {self} is not currently in an state that can be cancelled, skipping...")
    #     self.save()

    def finish(self, status: Status, details="") -> Status:
        self.status = status
        self.details = details
        self.ended = timezone.now()
        self.save()
        return status

    def set_running(self):
        if self.status == self.Status.CANCELLED:
            self.finish(self.Status.CANCELLED)
        elif self.status == self.Status.PENDING:
            self.status = self.Status.RUNNING
            self.updated = timezone.now()
            self.save()
            return True
        elif self.status == self.Status.RUNNING:
            self.updated = timezone.now()
            self.save()
            return True
        return False

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    def __str__(self) -> str:
        return f"{self.pk}"