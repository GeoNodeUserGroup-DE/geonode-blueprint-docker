
from django.apps import apps, AppConfig as BaseAppConfig
from django.urls import include, re_path


LITTERASSESSMENT_MODEL_API = "LITTERASSESSMENT_MODEL_API"


def run_setup_hooks(*args, **kwargs):
    from django.conf import settings
    from geonode.urls import urlpatterns
    from litterassessment.models import PermissionsModel

    if not settings.LITTERASSESSMENT_MODEL_API:
        setattr(
            settings,
            LITTERASSESSMENT_MODEL_API,
            "http://litterassessment:9000/v2/models/predict/",
        )

    urlpatterns += [
        re_path(r"^litterassessment/", include("litterassessment.urls")),
        re_path(r"^inferences/", include("litterassessment.api.urls")),
    ]


class LitterAssessmentConfig(BaseAppConfig):
    name = "litterassessment"
    label = "litterassessment"

    def ready(self):
        super(LitterAssessmentConfig, self).ready()

        if not apps.ready:
            run_setup_hooks()


default_app_config = "litterassessment.LitterAssessmentConfig"
