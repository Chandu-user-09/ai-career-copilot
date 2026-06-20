from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas

import json

from django.http import JsonResponse

import google.generativeai as genai

from .models import ResumeTemplate, UserResume



def resume_builder(request):

    templates = ResumeTemplate.objects.all()

    print("TEMPLATE COUNT =", templates.count())

    if request.method == "POST":

        template_id = request.POST.get("selected_template")

        selected_template = ResumeTemplate.objects.get(id=template_id)

        project_names = request.POST.getlist("project_name[]")
        project_stacks = request.POST.getlist("project_stack[]")
        project_descriptions = request.POST.getlist("project_description[]")

        projects = []

        for i in range(len(project_names)):
            projects.append({
                "name": project_names[i],
                "stack": project_stacks[i],
                "description": project_descriptions[i]
            })

        context = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "linkedin": request.POST.get("linkedin"),
            "github": request.POST.get("github"),
            "location": request.POST.get("location"),
            "summary": request.POST.get("summary"),
            "skills": request.POST.get("skills"),
            "education": request.POST.get("education"),
            "projects": projects,
            "experience": request.POST.get("experience"),
            "certifications": request.POST.get("certifications"),
        }

        if request.user.is_authenticated:

         UserResume.objects.create(

        user=request.user,

        name=request.POST.get(
            "name"
        ),

        template_name=selected_template.name,

        data=context

    )
        print("RESUME SAVED")

        return render(
            request,
            f"resume_templates/{selected_template.template_file}",
            context
        )

    return render(
        request,
        "resume_builder.html",
        {
            "templates": templates
        }
    )


def download_resume(request):
    name = request.GET.get("name", "")
    email = request.GET.get("email", "")
    phone = request.GET.get("phone", "")
    skills = request.GET.get("skills", "")
    education = request.GET.get("education", "")
    projects = request.GET.get("projects", "")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="resume.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 800, name)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 770, f"{email} | {phone}")

    pdf.drawString(100, 720, "Skills:")
    pdf.drawString(100, 700, skills)

    pdf.drawString(100, 650, "Education:")
    pdf.drawString(100, 630, education)

    pdf.drawString(100, 580, "Projects:")
    pdf.drawString(100, 560, projects)

    pdf.save()

    return response

def generate_summary(request):

    if request.method == "POST":

        data = json.loads(
            request.body
        )

        skills = data.get(
            "skills",
            ""
        )

        projects = data.get(
            "projects",
            ""
        )

        experience = data.get(
            "experience",
            ""
        )

        prompt = f"""
Create a professional resume summary.

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Write 4 lines.
Professional and ATS friendly.
"""

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        return JsonResponse({
            "summary":
            response.text
        })
    
from django.contrib.auth.decorators import login_required

@login_required
def my_resumes(request):

    resumes = UserResume.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_resumes.html",
        {
            "resumes": resumes
        }
    )    
from django.shortcuts import get_object_or_404, redirect


@login_required
def view_resume(request, id):

    resume = get_object_or_404(
        UserResume,
        id=id,
        user=request.user
    )

    template = ResumeTemplate.objects.get(
        name=resume.template_name
    )

    return render(
        request,
        f"resume_templates/{template.template_file}",
        resume.data
    )


@login_required
def delete_resume(request, id):

    resume = get_object_or_404(
        UserResume,
        id=id,
        user=request.user
    )

    resume.delete()

    return redirect(
        "my_resumes"
    )

