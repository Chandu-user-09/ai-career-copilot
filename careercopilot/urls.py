from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'resume/',
        include('resume.urls')
    ),
    path(
    'learning/',
    include('learning.urls')
),
    path(
    'interview/',
    include('interview.urls')
),
path(
    'doubts/',
    include('doubts.urls')
),
path(
    'resume-builder/',
    include('resume_builder.urls')
),

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )