from django.urls import path
from .views.UploadObject.view import UploadObjectView
from .views.onboard.view import OnboardingView
from .view import (
    CommitView,
    BranchView,
    LoginView,
    CreateUserView,
    GetObjectsView,
    GetRepoView,
)

urlpatterns = [
    # LOGIN APIs
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", CreateUserView.as_view(), name="sign-up"),
    # GET APIs
    path("getAllRepo/", GetRepoView.as_view(), name="get-repos"),
    path("getFiles/", GetObjectsView.as_view(), name="get-objects"),
    # CREATE APIs
    path("onboard/", OnboardingView.as_view(), name="onboard"),  # Creating repo
    path("upload/", UploadObjectView.as_view(), name="upload"),
    path("createBranch/", BranchView.as_view(), name="branch"),
    path("commit/", CommitView.as_view(), name="commit"),
]
