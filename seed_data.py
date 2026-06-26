import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careercopilot.settings')
django.setup()

# Import your actual Resume model from your application
# Replace 'resume_builder' with your actual app name if it's named differently
from resume_builder.models import Resume 

def seed_resumes():
    # Let's create two sample rows tied to your static files layout
    if not Resume.objects.exists():
        Resume.objects.create(
            name="Professional Software Engineer Profile",
            template_name="Modern Minimalist",
            file_name="template1.pdf",  # Must match the file sitting in static/resume_templates/
            created_at=timezone.now()
        )
        Resume.objects.create(
            name="Technical Executive CV",
            template_name="Executive Dark",
            file_name="template2.pdf",
            created_at=timezone.now()
        )
        print("Successfully injected sample resume templates into production!")
    else:
        print("Database already contains data rows. Skipping seeding.")

if __name__ == "__main__":
    seed_resumes()