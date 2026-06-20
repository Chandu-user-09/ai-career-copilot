from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.doubt_solver,
        name='doubt_solver'
    ),

]