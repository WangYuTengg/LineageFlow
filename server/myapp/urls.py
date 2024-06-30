from django.urls import path
from .views import HelloWorldView
from .views import CreateRepositoryView

urlpatterns = [
    path("hello/", HelloWorldView.as_view(), name="hello-world"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
]
