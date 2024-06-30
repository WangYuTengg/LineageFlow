from django.urls import path
from .views import HelloWorldView
from .views import CreateRepositoryView
from .views import TestView

urlpatterns = [
    path("hello/", HelloWorldView.as_view(), name="hello-world"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
    path("test/", TestView.as_view(), name="test")
]
