from django.urls import path
from .views import InteractiveResearchView

urlpatterns = [
    path("", InteractiveResearchView.as_view(), name="research"),
]
