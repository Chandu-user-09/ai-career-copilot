from django.shortcuts import render

def interview_home(request):

    return render(
        request,
        'interview_home.html'
    )

def java_questions(request):

    questions = [

        "Tell me about yourself",

        "What is OOP?",

        "Difference between JDK and JRE",

        "What is JVM?",

        "What are Collections?",

        "Difference between ArrayList and LinkedList",

        "What is Exception Handling?",

        "What is Spring Boot?",

        "What is REST API?",

        "Explain Dependency Injection"

    ]

    return render(
        request,
        'java_questions.html',
        {'questions': questions}
    )