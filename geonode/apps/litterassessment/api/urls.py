from django.urls import re_path
from litterassessment.api import views

urlpatterns = [
    re_path(r"", views.InferenceList.as_view())
]
