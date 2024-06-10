from django.urls import path
from issues import views

urlpatterns = [
  path("board/", views.IssueListView.as_view(), name="board"),
  path("new/", views.IssueCreateView.as_view(), name="new"),
  path("<int:pk>/", views.IssueDetailView.as_view(), name="detail"),
  path("<int:pk>/edit/", views.IssueUpdateView.as_view(), name="edit"),
  path("edit/status/<int:pk>/", views.StatusUpdateView.as_view(), name="update_status"),
]