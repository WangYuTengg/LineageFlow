from django.urls import path
from .views import CreateRepositoryView
from .views import (
    LoginAdminView,
    FilesView,
    RangeView,
    MetaView,
    CommitView,
    BranchView,
)

urlpatterns = [
    path("loginAdmin", LoginAdminView.as_view(), name="login-admin"),
    path("createRepository/", CreateRepositoryView.as_view(), name="create-repository"),
    path("files/", FilesView.as_view(), name="files"),
    path("range/", RangeView.as_view(), name="range"),
    path("metarange/", MetaView.as_view(), name="meta-range"),
    path("commit/", CommitView.as_view(), name="commit"),
    path("branch/", BranchView.as_view(), name="branch"),
]
