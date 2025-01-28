from django.urls import re_path

from litterassessment import views
from litterassessment.views import ForwardToInferenceApi

urlpatterns = [
    re_path(r"^(?P<path>.*)/$", ForwardToInferenceApi.as_view()),
]
