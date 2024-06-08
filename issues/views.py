from django.views.generic import (
  ListView,
  DetailView,
  CreateView,
  UpdateView,
  DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
  LoginRequiredMixin,
  UserPassesTestMixin
)
from .models import Issue, Priority, Status

class IssueListView(ListView):
  template_name = "issues/list.html"
  model = Issue

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["post_list"] = (
      Issue.objects
    )
    return context

class IssueDetailView(DetailView):
  template_name = "issues/detail.html"
  model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
  template_name = "issues/new.html"
  model = Issue
  fields = ["summary", "description", "status", "priority", "reporter", "assignee"]
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  template_name = "issues/edit.html"
  model = Issue
  fields = ["summary", "description", "status", "priority", "reporter", "assignee"]

  def test_func(self):
    issue = self.get_object()
    return issue.reporter == self.request.user

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  template_name = "issues/delete.html"
  model = Issue
  success_url = reverse_lazy("list") # Name of the URL pattern.

  def test_func(self):
    issue = self.get_object()
    return issue.reporter == self.request.user