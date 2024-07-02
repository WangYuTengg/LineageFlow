from django.urls import path
<<<<<<< HEAD
from .view import HelloWorldView
from .view import CreateRepositoryView
from .view import TestView, RangeView, MetaView, CommitView, BranchView
from .views.onboard.view import OnboardingView
=======
from .views import CreateRepositoryView
from .views import (
    LoginAdminView,
    FilesView,
    RangeView,
    MetaView,
    CommitView,
    BranchView,
)
>>>>>>> 4ac4a7151a236d040ada07f55b2a8994db77ef46

urlpatterns = [
    path("loginAdmin", LoginAdminView.as_view(), name="login-admin"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
<<<<<<< HEAD
    path("test/", TestView.as_view(), name="test"),
    path("range/",RangeView.as_view(), name="range"),
    path("metarange/",MetaView.as_view(), name="meta-range"),
    path("commit/",CommitView.as_view(), name="commit"),
    path("branch/",BranchView.as_view(), name="branch"),
    path("onboard/", OnboardingView.as_view(), name='onboard')
=======
    path("files/", FilesView.as_view(), name="files"),
    path("range/", RangeView.as_view(), name="range"),
    path("metarange/", MetaView.as_view(), name="meta-range"),
    path("commit/", CommitView.as_view(), name="commit"),
    path("branch/", BranchView.as_view(), name="branch"),
>>>>>>> 4ac4a7151a236d040ada07f55b2a8994db77ef46
]
