from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=30)


class Document(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True, blank=True)