from django.db import models
from django.contrib.auth.models import User




class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    resume_file = models.FileField(
        upload_to='resumes/'
    )

    extracted_text = models.TextField(
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    ats_score = models.IntegerField(
        default=0
    )

    def calculate_ats_score(self):
        keywords = [
            "java",
            "python",
            "react",
            "django",
            "spring boot",
            "sql",
            "mongodb",
            "aws",
            "docker",
            "git"
        ]

        score = 0
        text = ""

        if self.extracted_text:
            text = self.extracted_text.lower()

        for keyword in keywords:
            if keyword in text:
                score += 10

        return min(score, 100)

    def get_missing_skills(self):
        keywords = [
            "java",
            "python",
            "react",
            "django",
            "spring boot",
            "sql",
            "mongodb",
            "aws",
            "docker",
            "git"
        ]

        missing_skills = []
        text = ""

        if self.extracted_text:
            text = self.extracted_text.lower()

        for skill in keywords:
            if skill not in text:
                missing_skills.append(skill)

        return missing_skills
    

    def __str__(self):
        return self.user.username
    