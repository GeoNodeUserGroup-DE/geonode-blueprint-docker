from django.apps import apps, AppConfig as BaseAppConfig
from django.urls import include, re_path


LITTERASSESSMENT_MODEL_API = "LITTERASSESSMENT_MODEL_API"


def run_setup_hooks(*args, **kwargs):
    from django.conf import settings
    from geonode.urls import urlpatterns

    setattr(
        settings,
        LITTERASSESSMENT_MODEL_API,
        "http://litterassessment:9000/v2/models/predict/",
        # "http://172.18.0.1:9000/v2/models/predict/",
    )

    urlpatterns += [
        re_path(r"^litterassessment/", include("litterassessment.urls"))
    ]


class LitterAssessmentConfig(BaseAppConfig):
    name = "litterassessment"

    def ready(self):
        super(LitterAssessmentConfig, self).ready()

        if not apps.ready:
            run_setup_hooks()


default_app_config = "litterassessment.LitterAssessmentConfig"
