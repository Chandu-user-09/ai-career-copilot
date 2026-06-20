from django.urls import path
from . import views

urlpatterns = [

    path(
        'upload/',
        views.upload_resume,
        name='upload_resume'
    ),
    path(
    'view/',
    views.view_resumes,
    name='view_resumes'
),
 path('analyzer/', views.resume_analyzer, name='resume_analyzer'),
    path('analyzer/analyze/', views.analyze_resume, name='analyze_resume'),
]