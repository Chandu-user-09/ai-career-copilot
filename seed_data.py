import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careercopilot.settings')
django.setup()

from django.apps import apps

def seed_resumes():
    try:
        # Automatically lookup the models inside your resume_builder app
        app_config = apps.get_app_config('resume_builder')
        model_names = list(app_config.models.keys())
        print(f"Found models in resume_builder: {model_names}")
        
        if not model_names:
            print("No models found in resume_builder app!")
            return
            
        # Dynamically grab the first available model class in that app
        ResumeModel = app_config.get_model(model_names[0])
        
        if not ResumeModel.objects.exists():
            # Build an attribute dictionary based on what fields exist
            sample_data = {
                "name": "Professional Software Engineer Profile",
                "template_name": "Modern Minimalist",
                "file_name": "template1.pdf",
                "created_at": timezone.now()
            }
            
            # Filter out keys that don't match your exact model fields to prevent crashes
            model_fields = [f.name for f in ResumeModel._meta.get_fields()]
            final_data = {k: v for k, v in sample_data.items() if k in model_fields}
            
            # Create the record!
            ResumeModel.objects.create(**final_data)
            print(f"Successfully injected a record into {ResumeModel.__name__}!")
        else:
            print("Database already has data rows. Skipping.")
            
    except Exception as e:
        print(f"Seeding bypassed or skipped due to: {e}")

if __name__ == "__main__":
    seed_resumes()