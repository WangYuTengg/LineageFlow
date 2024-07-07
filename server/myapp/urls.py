from django.urls import path
from .views.UploadObject.test import Test
from .views.GetAllRepo.view import GetRepoView
from .views.GetAllObject.view import GetObjectsView
from .views.onboard.view import OnboardingView
from .views.DeleteFiles.view import DeleteFile
from .views.FetchFiles.view import FetchLatestCommitDataView
from .views.Commit.view import CommitView
from .views.Branch.view import BranchView
from .views.Login.view import (
    LoginView,
    CreateUserView,
)
from .views.RevertCommit.view import RevertCommit

urlpatterns = [
    # LOGIN APIs
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", CreateUserView.as_view(), name="sign-up"),
    # GET APIs
    path("getAllRepo/", GetRepoView.as_view(), name="get-repos"),
    path("getObjects/", GetObjectsView.as_view(), name="get-objects"),
    path("getCommitData/", FetchLatestCommitDataView.as_view(), name="get-commit-data"),
    path("getCommitsOfBranch/", CommitView.as_view(), name="get-commits-of-branch"),
    # CREATE APIs
    path("onboard/", OnboardingView.as_view(), name="onboard"),  # Creating repo
    path("upload/", Test.as_view(), name="upload"),
    path("createBranch/", BranchView.as_view(), name="branch"),
    path("commit/", CommitView.as_view(), name="commit"),
    path("revertCommit/", RevertCommit.as_view(), name="revert-commit"),
    # DELETE APIs
    path("deleteFiles/", DeleteFile.as_view(), name="delete-files"),
]
