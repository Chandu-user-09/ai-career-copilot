from django.db import models

class CourseResource(models.Model):

    RESOURCE_TYPES = [

        ("PDF", "PDF"),
        ("LINK", "LINK"),
        ("VIDEO", "VIDEO"),
        ("AI_MENTOR", "AI_MENTOR")

    ]

    course_name = models.CharField(
        max_length=100
    )

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES
    )

    title = models.CharField(
        max_length=200
    )

    url = models.URLField(
        blank=True,
        null=True
    )

    pdf_file = models.FileField(
        upload_to="course_materials/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title