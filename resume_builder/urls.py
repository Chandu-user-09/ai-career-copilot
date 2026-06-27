from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.resume_builder,
        name='resume_builder'
    ),

    path(
        "generate-summary/",
        views.generate_summary,
        name="generate_summary"
    ),

    path(
        "my-resumes/",
        views.my_resumes,
        name="my_resumes"
    ),

    path(
        "view-resume/<int:id>/",
        views.view_resume,
        name="view_resume"
    ),

    path(
        "delete-resume/<int:id>/",
        views.delete_resume,
        name="delete_resume"
    ),
]