from django.urls import path
from .view import CreateRepositoryView
from .view import (
    RangeView, 
    MetaView, 
    CommitView, 
    BranchView, 
    LoginView, 
    CreateUserView,
    GetRepoView)
from .views.onboard.view import OnboardingView

urlpatterns = [
    path("loginAdmin/", LoginView.as_view(), name="login"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
    path("range/", RangeView.as_view(), name="range"),
    path("metarange/", MetaView.as_view(), name="meta-range"),
    path("commit/", CommitView.as_view(), name="commit"),
    path("createBranch/", BranchView.as_view(), name="branch"),
    path("onboard/", OnboardingView.as_view(), name="onboard"),
    path("signup/", CreateUserView.as_view(), name="sign-up"),
    path("getAllRepo/", GetRepoView.as_view(), name="get-repos"),
]
