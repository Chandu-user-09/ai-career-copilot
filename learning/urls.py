from django.urls import path
from . import views

urlpatterns = [

path(
    "ai-mentor/",
    views.ai_mentor,
    name="ai_mentor"
),

path(
    "",
    views.learning_home,
    name="learning_home"
),

path(
    "<str:course_name>/",
    views.course_detail,
    name="course_detail"
),
path(
    "<str:course_name>/roadmap/",
    views.course_roadmap,
    name="course_roadmap"
),
path(
    "<str:course_name>/learn/",
    views.learn_course,
    name="learn_course"
),

path(
    "<str:course_name>/quiz/",
    views.quiz_home,
    name="quiz_home"
),
path(
    "<str:course_name>/quiz/start/",
    views.start_quiz,
    name="start_quiz"
),
path(
    "<str:course_name>/interview/",
    views.interview_home,
    name="interview_home"
),
path(
    "<str:course_name>/interview/<str:level>/",
    views.interview_questions_view,
    name="interview_questions"
),
path(
    "<str:course_name>/resume/",
    views.resume_questions,
    name="resume_questions"
),
path(
    "<str:course_name>/dashboard/",
    views.dashboard,
    name="dashboard"
),
path(
    "<str:course_name>/ats/",
    views.ats_checker,
    name="ats_checker"
),

path(
    "<slug:course_slug>/resume-generator/",
    views.resume_generator,
    name="resume_generator"
),


]
