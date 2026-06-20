import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pdfplumber
from docx import Document


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_pdf_text(pdf_file):
      text = ""

      with pdfplumber.open(pdf_file) as pdf:
          for page in pdf.pages:
              page_text = page.extract_text()

              if page_text:
                  text += page_text + "\n"

      return text


def extract_docx_text(docx_file):
      doc = Document(docx_file)

      text = "\n".join(
          para.text
          for para in doc.paragraphs
      )

      return text
@login_required
def resume_analyzer(request):
    """Render the ATS Resume Analyzer page."""
    return render(request, 'resume/analyzer.html')


@csrf_exempt
@login_required
def analyze_resume(request):
    """
    API endpoint — receives resume text + optional job description,
    calls Claude AI, returns JSON analysis.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    try:
        jd_text = request.POST.get('jdText', '').strip()
        resume_text = request.POST.get('resumeText', '').strip()

        uploaded_file = request.FILES.get('resumeFile')

        if uploaded_file:

            if uploaded_file.name.lower().endswith('.pdf'):
              resume_text = extract_pdf_text(uploaded_file)

            elif uploaded_file.name.lower().endswith('.docx'):
              resume_text = extract_docx_text(uploaded_file)

            elif uploaded_file.name.lower().endswith('.txt'):
              resume_text = uploaded_file.read().decode(
            'utf-8',
            errors='ignore'
        )

        if not resume_text:
          return JsonResponse(
        {'error': 'Resume text is required'},
        status=400
    )

        # Build prompt
        jd_section = f"\n\nJOB DESCRIPTION:\n{jd_text[:2000]}" if jd_text else ""

        prompt = f"""You are an expert ATS Resume Analyzer and Senior Technical Recruiter with 15+ years of experience at top MNCs like Google, Amazon, Microsoft, TCS, Infosys. Analyze this resume comprehensively and return a JSON object ONLY — no markdown, no explanation, no backticks.

RESUME TEXT:
{resume_text[:3500]}{jd_section}

Return this EXACT JSON structure (all numeric fields are integers 0-100):
{{
  "profile": {{
    "name": "string",
    "email": "string or null",
    "phone": "string or null",
    "linkedin": "string or null",
    "github": "string or null",
    "level": "Fresher|Entry-Level|Mid-Level|Experienced|Senior",
    "summary": "2-3 sentence profile summary"
  }},
  "scores": {{
    "overall": 0,
    "keywordMatch": 0,
    "skillsMatch": 0,
    "experienceQuality": 0,
    "education": 0,
    "projectQuality": 0,
    "resumeFormat": 0,
    "readability": 0
  }},
  "recruiterRating": 0,
  "strengthLevel": "Beginner|Intermediate|Advanced|Expert",
  "verdict": "Strong Reject|Reject|Consider|Shortlist|Strong Shortlist",
  "verdictReason": "2-3 sentence recruiter reasoning",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "skills": {{
    "programmingLanguages": [],
    "databases": [],
    "cloudTechnologies": [],
    "dataScience": [],
    "biAnalytics": [],
    "frameworks": [],
    "devops": [],
    "softSkills": []
  }},
  "missingSkills": ["6 missing industry-standard skills"],
  "suggestedSkills": ["6 high-demand skills to add"],
  "projects": [
    {{
      "name": "project name",
      "description": "brief description",
      "techStack": ["tech1", "tech2"],
      "rating": 0,
      "complexity": 0,
      "businessImpact": 0,
      "resumeValue": 0,
      "improvement": "specific improvement suggestion",
      "rewrite": "AI-improved version with action verbs and measurable outcomes"
    }}
  ],
  "experience": [
    {{
      "role": "job title",
      "company": "company name",
      "duration": "duration string",
      "starRewrite": "STAR methodology rewrite with metrics",
      "impact": "quantified impact statement"
    }}
  ],
  "keywordsFound": ["10-15 ATS keywords already present"],
  "keywordsMissing": ["10-15 important missing ATS keywords"],
  "roleMatch": {{
    "dataAnalyst": 0,
    "dataScientist": 0,
    "businessAnalyst": 0,
    "pythonDeveloper": 0,
    "cloudEngineer": 0,
    "mlEngineer": 0,
    "softwareEngineer": 0
  }},
  "improvements": [
    "improvement 1 - most critical",
    "improvement 2",
    "improvement 3",
    "improvement 4",
    "improvement 5",
    "improvement 6",
    "improvement 7",
    "improvement 8",
    "improvement 9",
    "improvement 10",
    "improvement 11",
    "improvement 12",
    "improvement 13",
    "improvement 14",
    "improvement 15"
  ],
  "optimizedSummary": "Full ATS-optimized professional summary with industry keywords",
  "rewrittenExperience": ["bullet 1", "bullet 2", "bullet 3", "bullet 4"],
  "certificationsSuggested": ["cert1", "cert2", "cert3"],
  "scoreAfterImprovements": 0
}}"""

        # Initialize Anthropic client and call API
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        response_text = response.text.strip()
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(response_text)
        
        return JsonResponse({
    'success': True,
    'data': analysis
})

        

    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Failed to parse AI response: {str(e)}'}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@login_required
def upload_resume(request):
    return HttpResponse("Resume Upload Page")

@login_required
def view_resumes(request):
    return HttpResponse("View Resumes Page")


