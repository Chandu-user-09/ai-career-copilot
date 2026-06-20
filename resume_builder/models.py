from django.db import models

class ResumeTemplate(models.Model):

    name = models.CharField(
        max_length=100
    )

    preview_image = models.ImageField(
        upload_to="resume_templates/"
    )

    template_file = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class UserResume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=200
    )

    template_name = models.CharField(
        max_length=100
    )

    data = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name    