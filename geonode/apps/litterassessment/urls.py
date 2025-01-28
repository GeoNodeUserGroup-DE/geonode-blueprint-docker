from django.urls import re_path

from litterassessment import views

urlpatterns = [
    re_path(r"^openapi/$", views.openapi),
    re_path(r"^(?P<path>.*)/$", views.forward_request),
]
