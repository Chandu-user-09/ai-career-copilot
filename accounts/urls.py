from django.urls import path
from .views import compiler_ai_explain

from . import views
urlpatterns = [

    path('', views.home),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
    path(
    "compiler/",
    views.compiler,
    name="compiler"
),


    # ... your existing routes
    path("api/compiler-ai-explain/", compiler_ai_explain, name="compiler_ai_explain"),
    
    


]