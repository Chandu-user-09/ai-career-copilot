from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.resume_builder,
        name='resume_builder'
    ),

    path(
        'download/',
        views.download_resume,
        name='download_resume'
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

#path(
 #   "download-resume/<int:id>/",
  #  views.download_template_pdf,
   # name="download_resume_pdf"
#),
#path(
 #   "download-resume/<int:id>/",
  #  views.download_resume_pdf,
   # name="download_resume_pdf"
#),
]