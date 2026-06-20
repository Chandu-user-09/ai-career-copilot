from django.shortcuts import render


def doubt_solver(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get("question")

        if "spring boot" in question.lower():

            answer = """
            Spring Boot is a Java framework used
            to build web applications and REST APIs quickly.
            """

        elif "react" in question.lower():

            answer = """
            React is a JavaScript library used
            to build user interfaces.
            """

        else:

            answer = """
            Sorry, I don't know this answer yet.
            """

    return render(
        request,
        "doubt_solver.html",
        {"answer": answer}
    )