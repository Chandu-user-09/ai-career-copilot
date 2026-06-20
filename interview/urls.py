from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.interview_home,
        name='interview_home'
    ),

    path(
        'java/',
        views.java_questions,
        name='java_questions'
    ),

]