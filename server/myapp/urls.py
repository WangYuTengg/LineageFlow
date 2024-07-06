from django.urls import path
from .views.UploadObject.view import UploadObjectView
from .views.GetAllRepo.view import GetRepoView
from .views.GetAllObject.view import GetObjectsView
from .views.onboard.view import OnboardingView
from .views.FetchFiles.view import FetchLatestCommitDataView
from .view import (
    CommitView,
    BranchView,
    LoginView,
    CreateUserView,
)

urlpatterns = [
    # LOGIN APIs
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", CreateUserView.as_view(), name="sign-up"),
    # GET APIs
    path("getAllRepo/", GetRepoView.as_view(), name="get-repos"),
    path("getObjects/", GetObjectsView.as_view(), name="get-objects"),
    path("getCommitData", FetchLatestCommitDataView.as_view(), name= 'get-commit-data'),
    # CREATE APIs
    path("onboard/", OnboardingView.as_view(), name="onboard"),  # Creating repo
    path("upload/", UploadObjectView.as_view(), name="upload"),
    path("createBranch/", BranchView.as_view(), name="branch"),
    path("commit/", CommitView.as_view(), name="commit"),
    
]
