from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Status(models.Model):
  name = models.CharField(
    max_length=128,
    default='To do'
  )
  description = models.CharField(max_length=256)

  def __str__(self):
    return self.name

class Priority(models.Model):
  name = models.CharField(max_length=128)
  description = models.CharField(max_length=256)

  def __str__(self):
    return self.name

class Issue(models.Model):
  summary = models.CharField(max_length=128)
  description = models.CharField(max_length=256)
  status = models.ForeignKey(
    Status,
    on_delete=models.CASCADE
  )
  priority = models.ForeignKey(
    Priority,
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

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse("detail", args=[self.id]) # TODO