from django.urls import path
from .view import HelloWorldView
from .view import CreateRepositoryView
from .view import TestView, RangeView, MetaView, CommitView, BranchView
from .views.onboard.view import OnboardingView

urlpatterns = [
    path("hello/", HelloWorldView.as_view(), name="hello-world"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
    path("test/", TestView.as_view(), name="test"),
    path("range/",RangeView.as_view(), name="range"),
    path("metarange/",MetaView.as_view(), name="meta-range"),
    path("commit/",CommitView.as_view(), name="commit"),
    path("branch/",BranchView.as_view(), name="branch"),
    path("onboard/", OnboardingView.as_view(), name='onboard')
]
