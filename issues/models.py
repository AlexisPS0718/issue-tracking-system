from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

PRIORITES = [
  ("LO", "Low"),
  ("MD", "Medium"),
  ("HI", "High")
]

COMPLEXITY = [
  (1, "Smallest"),
  (2, "Low mid"),
  (3, "Medium"),
  (5, "High mid"),
  (8, "High"),
  (13, "Very high")
]

class Status(models.Model):
  name = models.CharField(max_length=128)
  description = models.CharField(max_length=256)

  def __str__(self):
    return self.name

class Issue(models.Model):
  name = models.CharField(max_length=64)
  summary = models.CharField(max_length=128)
  description = models.TextField()
  status = models.ForeignKey(
    Status,
    default=1,
    on_delete=models.CASCADE
  )
  reporter = models.ForeignKey(
    get_user_model(),
    related_name = 'reporter',
    on_delete=models.CASCADE
  )
  assignee = models.ForeignKey(
    get_user_model(),
    related_name = 'assignee',
    on_delete=models.CASCADE
  )
  complexity = models.IntegerField(
    choices=COMPLEXITY,
    default=1,
    blank=True,
    null=True
  )
  priority = models.CharField(
    max_length=2, 
    choices=PRIORITES,
    blank=True,
    null=True
  )
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now_add=True)
  is_archived = models.BooleanField(default=0)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse("detail", args=[self.id])