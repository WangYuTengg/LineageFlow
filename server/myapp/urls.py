from django.urls import path
from .views import HelloWorldView
from .views import CreateRepositoryView
from .views import TestView, FilesView, RangeView, MetaView, CommitView, BranchView

urlpatterns = [
    # path("hello/", HelloWorldView.as_view(), name="hello-world"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
    # path("test/", TestView.as_view(), name="test"),
    path("files/",FilesView.as_view(), name="files"),
    path("range/",RangeView.as_view(), name="range"),
    path("metarange/",MetaView.as_view(), name="meta-range"),
    path("commit/",CommitView.as_view(), name="commit"),
    path("branch/",BranchView.as_view(), name="branch")
]
