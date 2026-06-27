from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json

import google.generativeai as genai

from .models import ResumeTemplate, UserResume


def resume_builder(request):
    templates = ResumeTemplate.objects.all()

    if request.method == "POST":
        template_id = request.POST.get("selected_template")
        selected_template = ResumeTemplate.objects.get(id=template_id)

        # Section visibility toggles
        show_summary        = request.POST.get("show_summary") == "on" or request.POST.get("show_summary") == "true" or request.POST.get("show_summary") is not None
        show_skills         = request.POST.get("show_skills") is not None
        show_education      = request.POST.get("show_education") is not None
        show_projects       = request.POST.get("show_projects") is not None
        show_experience     = request.POST.get("show_experience") is not None
        show_certifications = request.POST.get("show_certifications") is not None
        show_achievements   = request.POST.get("show_achievements") is not None
        show_languages      = request.POST.get("show_languages") is not None

        # ATS checkbox
        ats_optimized = request.POST.get("ats_optimized") is not None

        # Gather dynamic project arrays
        project_names        = request.POST.getlist("project_name[]")
        project_stacks       = request.POST.getlist("project_stack[]")
        project_descriptions = request.POST.getlist("project_description[]")

        projects = []
        for i in range(len(project_names)):
            if project_names[i].strip(): # Only pack if name isn't empty
                projects.append({
                    "name":        project_names[i],
                    "stack":       project_stacks[i] if i < len(project_stacks) else "",
                    "description": project_descriptions[i] if i < len(project_descriptions) else "",
                })

        # Process skills block cleanly into individual loop elements
        raw_skills = request.POST.get("skills", "")
        skills_list = [s.strip() for s in raw_skills.split(",") if s.strip()]

        # Generate character initials safely
        name = request.POST.get("name", "")
        initials = "".join(word[0] for word in name.split() if word)[:2].upper()

        context = {
            "resume_title":        request.POST.get("resume_title") or "Professional Resume",
            "name":                name,
            "initials":            initials,
            "email":               request.POST.get("email"),
            "phone":               request.POST.get("phone"),
            "linkedin":            request.POST.get("linkedin"),
            "github":              request.POST.get("github"),
            "location":            request.POST.get("location"),
            "summary":             request.POST.get("summary"),
            "skills":              skills_list,
            "education":           request.POST.get("education"),
            "projects":            projects,
            "experience":          request.POST.get("experience"),
            "certifications":      request.POST.get("certifications"),
            "achievements":        request.POST.get("achievements"),
            "languages":           request.POST.get("languages"),
            "show_summary":        show_summary,
            "show_skills":         show_skills,
            "show_education":      show_education,
            "show_projects":       show_projects,
            "show_experience":     show_experience,
            "show_certifications": show_certifications,
            "show_achievements":   show_achievements,
            "show_languages":      show_languages,
            "ats_optimized":       ats_optimized,
        }

        # Persist to database if authenticated
        if request.user.is_authenticated:
            UserResume.objects.create(
                user=request.user,
                name=name,
                template_name=selected_template.name,
                data=context,
            )

        return render(
            request,
            f"resume_templates/{selected_template.template_file}",
            context,
        )

    # GET request execution loop
    return render(request, "resume_builder.html", {"templates": templates})


def generate_summary(request):
    if request.method == "POST":
        data       = json.loads(request.body)
        skills     = data.get("skills", "")
        projects   = data.get("projects", "")
        experience = data.get("experience", "")

        prompt = f"""
Create a professional resume summary.

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Write exactly 4 lines.
Keep it crisp, professional, and ATS friendly. Do not output anything other than the summary text.
"""
        model    = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return JsonResponse({"summary": response.text.strip()})


@login_required
def my_resumes(request):
    resumes = UserResume.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_resumes.html", {"resumes": resumes})


@login_required
def view_resume(request, id):
    resume   = get_object_or_404(UserResume, id=id, user=request.user)
    template = ResumeTemplate.objects.get(name=resume.template_name)
    return render(
        request,
        f"resume_templates/{template.template_file}",
        resume.data,
    )


@login_required
def delete_resume(request, id):
    resume = get_object_or_404(UserResume, id=id, user=request.user)
    resume.delete()
    return redirect("my_resumes")