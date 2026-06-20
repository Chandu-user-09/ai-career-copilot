import PyPDF2
from docx import Document

def extract_text_from_pdf(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

def extract_docx_text(docx_file):

    doc = Document(docx_file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text


def calculate_ats_score(text):

    score = 0

    keywords = [  

        "python",
        "java",
        "sql",
        "django",
        "react",
        "node",
        "mongodb",
        "git",
        "api",
        "project",
        "internship",
        "aws",
        "docker"

    ]

    text = text.lower()

    for keyword in keywords:

        if keyword in text:

            score += 8

    return min(score, 100)