import json
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import google.generativeai as genai
from dotenv import load_dotenv

from .forms import RegisterForm
from learning.models import CourseResource

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")
            return redirect('/login/')
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect('/')


def dashboard(request):
    total_resources = CourseResource.objects.count()

    context = {
        "total_resources": total_resources,
        "total_courses": 8
    }

    return render(request, "dashboard.html", context)


def home(request):
    total_resources = CourseResource.objects.count()

    context = {
        "total_resources": total_resources,
        "total_courses": 8
    }

    return render(request, "home.html", context)


def compiler(request):
    return render(request, "compiler.html")


@csrf_exempt
def compiler_ai_explain(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get("code", "")
        lang = data.get("lang", "python")

        prompt = f"""You are an expert code assistant in CodeForge Pro IDE.
Analyze this {lang} code and respond in HTML format (compact, no outer tags):

<b>📋 What it does:</b> 1-2 sentences<br><br>
<b>⚠️ Issues found:</b> list bugs/errors or say None<br><br>
<b>💡 Suggestions:</b> 2-3 improvements<br><br>
<b>🔧 Quick fix:</b> if errors exist, show fixed snippet in <code> tags

Code:
```{lang}
{code}
```"""

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        answer = response.text

        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse(
            {"answer": "AI Assistant is temporarily unavailable.\n\n" + str(e)},
            status=500
        )