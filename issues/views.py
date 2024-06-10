from django.views.generic import (
  ListView,
  CreateView,
  DetailView,
  UpdateView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
  LoginRequiredMixin,
  UserPassesTestMixin
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .models import Issue, Status
from accounts.models import Role

class IssueListView(LoginRequiredMixin, ListView):
  template_name = "issues/board.html"
  model = Issue

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    to_do = Status.objects.get(name="To do")
    in_progress = Status.objects.get(name="In progress")
    done = Status.objects.get(name="Done")
    context["issues_list"] = (
      Issue.objects
    )
    context["to_do_list"] = (
      Issue.objects
      .filter(status=to_do)
      .order_by("created_on")
    )
    context["in_progress_list"] = (
      Issue.objects
      .filter(status=in_progress)
      .order_by("created_on")
    )
    context["done_list"] = (
      Issue.objects
      .filter(status=done)
      .order_by("created_on")
    )
    return context

class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  template_name = "issues/new.html"
  model = Issue
  fields = ["name", "summary", "description", "assignee", "complexity", "priority"]

  def test_func(self):
    user_role = self.request.user.role
    return user_role.name == "Product Owner"

  def form_valid(self, form):
    form.instance.reporter = self.request.user
    to_do = Status.objects.get(name="To do")
    form.instance.status = to_do
    return super().form_valid(form)

class IssueDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  template_name = "issues/detail.html"
  model = Issue

  def test_func(self):
    team = self.request.user.team
    po_role = Role.objects.get(name="Product Owner")
    try:
      reporter = get_user_model().objects.filter(team=team).get(role=po_role)
    except ObjectDoesNotExist as objexc:
      print("Error: Team has no PO")
      reporter = self.request.user
    finally:
      return team == reporter.team

class IssueUpdateView(LoginRequiredMixin, UpdateView):
  template_name = "issues/edit.html"
  model = Issue
  fields = ["name", "summary", "description", "assignee", "complexity", "priority"]

class StatusUpdateView(UserPassesTestMixin, UpdateView):
  template_name = "issues/board.html"
  model = Issue
  fields = ["status"]
  success_url = reverse_lazy("board")

  def test_func(self):
    user_role = self.request.user.role
    return user_role.name == "Developer"