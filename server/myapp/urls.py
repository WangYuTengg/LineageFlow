from django.urls import path
from .view import CreateRepositoryView
from .views.UploadObject.view import UploadObjectView
from .view import (
    CommitView,
    BranchView,
    LoginView,
    CreateUserView,
    GetObjectsView,
    GetRepoView,
)
from .views.onboard.view import OnboardingView

urlpatterns = [
    # LOGIN APIs
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", CreateUserView.as_view(), name="sign-up"),
    # GET APIs
    path("getAllRepo/", GetRepoView.as_view(), name="get-repos"),
    path("getFiles/", GetObjectsView.as_view(), name="get-objects"),
    # CREATE APIs
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
    path("onboard/", OnboardingView.as_view(), name="onboard"),
    path("upload/", UploadObjectView.as_view(), name="upload"),
    path("createBranch/", BranchView.as_view(), name="branch"),
    path("commit/", CommitView.as_view(), name="commit"),
]
