from django.shortcuts import render
import os
import google.generativeai as genai
import json
import random
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from resume.forms import ResumeForm
from .interview_questions import INTERVIEW_QUESTIONS
from django.http import Http404

from django.http import HttpResponse
from resume.utils import (
    extract_text_from_pdf,
    extract_docx_text,
    calculate_ats_score
)


# A small helper dictionary to map URL slugs to clean titles if needed
COURSE_TITLES = {
    "frontend-developer": "Frontend Developer",
    "backend-java": "Backend (Java)",
    "backend-python": "Backend (Python)",
    "java-full-stack": "Java Full Stack",
    "python-full-stack": "Python Full Stack",
    "ai-ml-engine": "AI & ML Engine",
    "data-analytics": "Data Analytics",
    "data-science": "Data Science",
}
from .models import CourseResource

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def learning_home(request):
    return render(
        request,
        "learning_home.html"
    )


def course_detail(request, course_name):
    context = {
        "course_name": course_name.replace("-", " ").title()
    }
    return render(
        request,
        "course_detail.html",
        context
    )


def course_roadmap(request, course_name):

    roadmaps = {

        "java-full-stack": [
            {
                "title": "Core Java",
                "desc": "Master Java language fundamentals before touching any framework.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "Java Basics",
                        "subs": [
                            "JDK, JRE, JVM setup",
                            "Variables, data types, operators",
                            "Input/output with Scanner",
                            "Type casting and conversions",
                        ]
                    },
                    {
                        "label": "Control Flow",
                        "subs": [
                            "if / else / switch statements",
                            "for, while, do-while loops",
                            "break, continue, return",
                            "Nested loops and patterns",
                        ]
                    },
                    {
                        "label": "Arrays & Strings",
                        "subs": [
                            "1D and 2D arrays",
                            "String methods: length, charAt, substring",
                            "StringBuilder vs String",
                            "String formatting",
                        ]
                    },
                    {
                        "label": "Methods",
                        "subs": [
                            "Defining and calling methods",
                            "Method overloading",
                            "Recursion basics",
                            "Pass by value concept",
                        ]
                    },
                ]
            },
            {
                "title": "OOP Concepts",
                "desc": "Object-Oriented Programming is the backbone of Java development.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Classes & Objects",
                        "subs": [
                            "Defining classes and creating objects",
                            "Constructors and overloading",
                            "this keyword",
                            "Instance vs static members",
                        ]
                    },
                    {
                        "label": "Inheritance",
                        "subs": [
                            "extends keyword",
                            "Method overriding",
                            "super keyword",
                            "Single, multilevel, hierarchical types",
                        ]
                    },
                    {
                        "label": "Polymorphism",
                        "subs": [
                            "Compile-time (overloading)",
                            "Runtime (overriding)",
                            "Upcasting and downcasting",
                            "instanceof operator",
                        ]
                    },
                    {
                        "label": "Abstraction & Encapsulation",
                        "subs": [
                            "Abstract classes and methods",
                            "Interfaces and default methods",
                            "Access modifiers: public, private, protected",
                            "Getters and setters",
                        ]
                    },
                ]
            },
            {
                "title": "Collections Framework",
                "desc": "Java's built-in data structures for managing groups of objects.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "List",
                        "subs": [
                            "ArrayList: add, remove, get, size",
                            "LinkedList operations",
                            "ListIterator",
                            "Sorting with Collections.sort()",
                        ]
                    },
                    {
                        "label": "Set & Map",
                        "subs": [
                            "HashSet and TreeSet",
                            "HashMap: put, get, containsKey",
                            "LinkedHashMap for ordered entries",
                            "Iterating maps with entrySet()",
                        ]
                    },
                    {
                        "label": "Queue & Stack",
                        "subs": [
                            "Stack: push, pop, peek",
                            "Queue with LinkedList",
                            "PriorityQueue",
                            "ArrayDeque",
                        ]
                    },
                ]
            },
            {
                "title": "MySQL & JDBC",
                "desc": "Connect Java applications to relational databases using JDBC.",
                "time": "3 weeks",
                "topics": [
                    {
                        "label": "MySQL Basics",
                        "subs": [
                            "CREATE, DROP, ALTER tables",
                            "INSERT, UPDATE, DELETE, SELECT",
                            "WHERE, ORDER BY, GROUP BY",
                            "JOINs: INNER, LEFT, RIGHT",
                            "Indexes and primary/foreign keys",
                        ]
                    },
                    {
                        "label": "JDBC",
                        "subs": [
                            "DriverManager and Connection",
                            "Statement vs PreparedStatement",
                            "ResultSet iteration",
                            "Handling SQL exceptions",
                            "Closing resources properly",
                        ]
                    },
                ]
            },
            {
                "title": "Servlets & JSP",
                "desc": "Build dynamic server-side web pages with Java Servlets and JSP.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "Servlets",
                        "subs": [
                            "Servlet lifecycle: init, service, destroy",
                            "HttpServletRequest and Response",
                            "doGet and doPost methods",
                            "Session management",
                            "RequestDispatcher: forward and redirect",
                        ]
                    },
                    {
                        "label": "JSP",
                        "subs": [
                            "JSP scriptlets, expressions, declarations",
                            "EL (Expression Language)",
                            "JSTL core tags",
                            "JSP with MVC pattern",
                            "Connecting JSP to MySQL",
                        ]
                    },
                ]
            },
            {
                "title": "Spring Core & Spring Boot",
                "desc": "The most important Java framework for enterprise applications.",
                "time": "5–6 weeks",
                "topics": [
                    {
                        "label": "Spring Core",
                        "subs": [
                            "IoC container and ApplicationContext",
                            "Dependency Injection: constructor & setter",
                            "@Component, @Autowired, @Bean",
                            "Spring configuration with annotations",
                        ]
                    },
                    {
                        "label": "Spring Boot",
                        "subs": [
                            "Spring Initializr project setup",
                            "application.properties configuration",
                            "@SpringBootApplication and auto-config",
                            "Embedded Tomcat server",
                            "Spring Boot DevTools",
                        ]
                    },
                    {
                        "label": "Spring MVC",
                        "subs": [
                            "@Controller and @RestController",
                            "@RequestMapping, @GetMapping, @PostMapping",
                            "@RequestParam and @PathVariable",
                            "@RequestBody and @ResponseBody",
                            "Exception handling with @ControllerAdvice",
                        ]
                    },
                    {
                        "label": "Spring Data JPA",
                        "subs": [
                            "JpaRepository and CrudRepository",
                            "Entity classes with @Entity, @Id",
                            "Derived query methods",
                            "Custom queries with @Query",
                            "Pagination and sorting",
                        ]
                    },
                ]
            },
            {
                "title": "REST APIs",
                "desc": "Build and consume RESTful APIs — standard for modern backend.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "REST Concepts",
                        "subs": [
                            "HTTP methods: GET, POST, PUT, DELETE",
                            "Status codes: 200, 201, 400, 404, 500",
                            "JSON request and response bodies",
                            "Postman for API testing",
                        ]
                    },
                    {
                        "label": "Security & JWT",
                        "subs": [
                            "Spring Security basics",
                            "JWT token: header, payload, signature",
                            "Authentication vs Authorization",
                            "Role-based access control",
                        ]
                    },
                ]
            },
            {
                "title": "Frontend + DevOps",
                "desc": "Complete the stack with HTML/CSS/React and Docker.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "HTML & CSS",
                        "subs": [
                            "Semantic HTML5 tags",
                            "CSS Flexbox and Grid",
                            "Responsive design with media queries",
                            "Bootstrap 5 components",
                        ]
                    },
                    {
                        "label": "JavaScript & React",
                        "subs": [
                            "ES6: arrow functions, destructuring, spread",
                            "DOM manipulation and events",
                            "React components, props, state",
                            "Hooks: useState, useEffect",
                            "Axios for API calls to Spring Boot",
                        ]
                    },
                    {
                        "label": "Git & Docker",
                        "subs": [
                            "git init, add, commit, push, pull",
                            "Branching and merging",
                            "Dockerfile for Java Spring Boot",
                            "docker-compose with MySQL container",
                        ]
                    },
                ]
            },
        ],

        "python-full-stack": [
            {
                "title": "Python Basics",
                "desc": "Build a solid Python foundation before moving to frameworks.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Variables & Types",
                        "subs": [
                            "int, float, str, bool, None",
                            "Type conversion and casting",
                            "f-strings and string methods",
                            "Mutable vs immutable types",
                        ]
                    },
                    {
                        "label": "Control Flow",
                        "subs": [
                            "if / elif / else",
                            "for and while loops",
                            "List, dict, set comprehensions",
                            "break, continue, pass",
                        ]
                    },
                    {
                        "label": "Functions",
                        "subs": [
                            "Defining functions and return values",
                            "*args and **kwargs",
                            "Lambda functions",
                            "Decorators and closures",
                        ]
                    },
                    {
                        "label": "OOP in Python",
                        "subs": [
                            "Classes and __init__",
                            "Inheritance and super()",
                            "Dunder methods __str__, __repr__",
                            "Dataclasses",
                        ]
                    },
                ]
            },
            {
                "title": "NumPy & Pandas",
                "desc": "Essential data manipulation libraries used across Python projects.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "NumPy",
                        "subs": [
                            "ndarray creation and indexing",
                            "Array operations and broadcasting",
                            "Reshaping: reshape, flatten, transpose",
                            "Math functions: sum, mean, std",
                        ]
                    },
                    {
                        "label": "Pandas",
                        "subs": [
                            "Series and DataFrame creation",
                            "read_csv, read_excel, read_sql",
                            "Filtering: loc, iloc, query",
                            "groupby, merge, concat, pivot_table",
                            "Handling missing data: fillna, dropna",
                        ]
                    },
                ]
            },
            {
                "title": "SQL & Databases",
                "desc": "Every Django app needs a database. Master SQL before the ORM.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "SQL Fundamentals",
                        "subs": [
                            "SELECT, WHERE, ORDER BY, LIMIT",
                            "JOINs: INNER, LEFT, RIGHT",
                            "GROUP BY and aggregate functions",
                            "Subqueries and CTEs",
                        ]
                    },
                    {
                        "label": "Django ORM",
                        "subs": [
                            "Model definition and field types",
                            "makemigrations and migrate",
                            "QuerySet: filter, exclude, annotate",
                            "select_related and prefetch_related",
                            "Raw SQL with connection.cursor()",
                        ]
                    },
                ]
            },
            {
                "title": "Django Backend",
                "desc": "Django is the batteries-included Python framework for full applications.",
                "time": "5–6 weeks",
                "topics": [
                    {
                        "label": "Django Basics",
                        "subs": [
                            "Project vs app structure",
                            "settings.py, urls.py, views.py",
                            "Function-based and class-based views",
                            "Django admin panel",
                            "Static and media files",
                        ]
                    },
                    {
                        "label": "Templates",
                        "subs": [
                            "DTL: {{ variables }} and {% tags %}",
                            "Template inheritance with extends",
                            "Filters and custom template tags",
                            "Passing context from views",
                        ]
                    },
                    {
                        "label": "Forms & Auth",
                        "subs": [
                            "Django ModelForm and Form classes",
                            "Form validation and error handling",
                            "Built-in auth: login, logout, register",
                            "Password hashing with PBKDF2",
                            "Session management",
                        ]
                    },
                    {
                        "label": "REST APIs with DRF",
                        "subs": [
                            "Serializers: ModelSerializer",
                            "APIView and ViewSets",
                            "Routers for URL auto-generation",
                            "JWT with SimpleJWT",
                            "Pagination and filtering",
                        ]
                    },
                ]
            },
            {
                "title": "Frontend (HTML, CSS, JS, React)",
                "desc": "Build the UI that your Django APIs will serve.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "HTML & CSS",
                        "subs": [
                            "Semantic HTML5 structure",
                            "CSS Flexbox and Grid layout",
                            "Bootstrap 5 for rapid UI",
                            "Responsive media queries",
                        ]
                    },
                    {
                        "label": "JavaScript",
                        "subs": [
                            "ES6: let/const, arrow functions",
                            "DOM manipulation",
                            "fetch() and async/await",
                            "Event listeners and form handling",
                        ]
                    },
                    {
                        "label": "React",
                        "subs": [
                            "JSX, components, props, state",
                            "Hooks: useState, useEffect",
                            "Axios API calls to Django",
                            "React Router for navigation",
                        ]
                    },
                ]
            },
            {
                "title": "Git & Docker",
                "desc": "Version control and containerization — must-have skills for any dev.",
                "time": "2 weeks",
                "topics": [
                    {
                        "label": "Git & GitHub",
                        "subs": [
                            "git init, add, commit, push",
                            "Branching: feature branches and PRs",
                            "Merge vs rebase",
                            ".gitignore for Python projects",
                        ]
                    },
                    {
                        "label": "Docker",
                        "subs": [
                            "Writing a Dockerfile for Django",
                            "docker build and docker run",
                            "docker-compose with PostgreSQL",
                            "Environment variables in containers",
                            "Pushing images to Docker Hub",
                        ]
                    },
                ]
            },
        ],

        "frontend-developer": [
            {
                "title": "HTML Foundations",
                "desc": "The skeleton of every web page. Master structure before styling.",
                "time": "1–2 weeks",
                "topics": [
                    {
                        "label": "HTML Basics",
                        "subs": [
                            "Document structure: html, head, body",
                            "Headings, paragraphs, links, images",
                            "Lists: ul, ol, li",
                            "Tables: table, tr, th, td",
                        ]
                    },
                    {
                        "label": "Semantic HTML5",
                        "subs": [
                            "header, nav, main, section, article, footer",
                            "Forms: input types, label, select, textarea",
                            "HTML5 attributes: required, placeholder, type",
                            "Accessibility with alt and aria labels",
                        ]
                    },
                ]
            },
            {
                "title": "CSS Styling",
                "desc": "Make your pages look great and respond to any screen size.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "CSS Basics",
                        "subs": [
                            "Selectors: tag, class, id, pseudo",
                            "Box model: margin, padding, border",
                            "Colors, fonts, and backgrounds",
                            "CSS variables (custom properties)",
                        ]
                    },
                    {
                        "label": "Layouts",
                        "subs": [
                            "Flexbox: direction, justify, align",
                            "CSS Grid: columns, rows, areas",
                            "Position: relative, absolute, fixed, sticky",
                            "Responsive with media queries",
                        ]
                    },
                    {
                        "label": "Bootstrap 5",
                        "subs": [
                            "Grid system: container, row, col",
                            "Components: navbar, card, button, modal",
                            "Utility classes for spacing and colors",
                            "Forms and input groups",
                        ]
                    },
                ]
            },
            {
                "title": "JavaScript Core",
                "desc": "Add interactivity and logic to your web pages.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "JS Fundamentals",
                        "subs": [
                            "Variables: var, let, const",
                            "Data types, operators, type coercion",
                            "Functions: declaration, expression, arrow",
                            "Scope, hoisting, and closures",
                        ]
                    },
                    {
                        "label": "DOM Manipulation",
                        "subs": [
                            "querySelector and querySelectorAll",
                            "innerHTML, textContent, classList",
                            "Event listeners: click, submit, keydown",
                            "Creating and removing DOM elements",
                        ]
                    },
                    {
                        "label": "ES6+ Features",
                        "subs": [
                            "Destructuring: arrays and objects",
                            "Spread and rest operators",
                            "Template literals",
                            "Modules: import and export",
                            "Optional chaining and nullish coalescing",
                        ]
                    },
                ]
            },
            {
                "title": "React",
                "desc": "The most in-demand frontend library. Build dynamic UIs with components.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "React Basics",
                        "subs": [
                            "JSX syntax and component structure",
                            "Props: passing and receiving data",
                            "useState hook for local state",
                            "Conditional rendering and lists with keys",
                        ]
                    },
                    {
                        "label": "React Hooks",
                        "subs": [
                            "useEffect for side effects",
                            "useRef for DOM references",
                            "useContext for global state",
                            "Custom hooks pattern",
                        ]
                    },
                    {
                        "label": "React Router",
                        "subs": [
                            "BrowserRouter, Routes, Route",
                            "useNavigate and useParams",
                            "Protected routes with auth guards",
                            "Nested routes and layouts",
                        ]
                    },
                ]
            },
            {
                "title": "Redux & State Management",
                "desc": "Manage complex application state across many components.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "Redux Toolkit",
                        "subs": [
                            "Store, Slice, and Reducer concepts",
                            "createSlice and configureStore",
                            "useSelector and useDispatch hooks",
                            "Async thunks with createAsyncThunk",
                        ]
                    },
                    {
                        "label": "Alternatives",
                        "subs": [
                            "Context API for smaller apps",
                            "Zustand: lightweight state management",
                            "React Query for server state",
                            "When to use Redux vs Context",
                        ]
                    },
                ]
            },
            {
                "title": "API Integration & Projects",
                "desc": "Connect your frontend to real APIs and build portfolio projects.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "API Integration",
                        "subs": [
                            "fetch() and async/await pattern",
                            "Axios for cleaner HTTP calls",
                            "Handling loading, error, success states",
                            "Sending JWT in Authorization header",
                            "CORS issues and how to fix them",
                        ]
                    },
                    {
                        "label": "Git & Projects",
                        "subs": [
                            "Git workflow for frontend projects",
                            "Deploying React apps to Netlify/Vercel",
                            "Build a weather app with API",
                            "Build a task manager with Redux",
                            "Portfolio project with full CRUD",
                        ]
                    },
                ]
            },
        ],

        "backend-developer-java": [
            {
                "title": "Core Java & OOP",
                "desc": "Everything in Java backend starts here. No shortcuts.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "Core Java",
                        "subs": [
                            "Data types, operators, control flow",
                            "Arrays and String manipulation",
                            "Methods and recursion",
                            "Exception handling: try/catch/finally",
                        ]
                    },
                    {
                        "label": "OOP Principles",
                        "subs": [
                            "Encapsulation with private fields",
                            "Inheritance and method overriding",
                            "Polymorphism: compile-time and runtime",
                            "Abstraction with interfaces",
                        ]
                    },
                ]
            },
            {
                "title": "Collections & JDBC",
                "desc": "Manage data in memory and connect to databases from Java.",
                "time": "3 weeks",
                "topics": [
                    {
                        "label": "Collections",
                        "subs": [
                            "ArrayList, LinkedList, HashSet",
                            "HashMap, TreeMap, LinkedHashMap",
                            "Stack, Queue, PriorityQueue",
                            "Sorting with Comparable and Comparator",
                        ]
                    },
                    {
                        "label": "JDBC",
                        "subs": [
                            "Connection, Statement, PreparedStatement",
                            "ResultSet navigation",
                            "Batch updates for performance",
                            "Transactions with commit/rollback",
                            "Connection pooling with HikariCP",
                        ]
                    },
                ]
            },
            {
                "title": "MySQL",
                "desc": "Relational database skills every Java backend developer must have.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "SQL Mastery",
                        "subs": [
                            "DDL: CREATE, ALTER, DROP",
                            "DML: INSERT, UPDATE, DELETE, SELECT",
                            "Joins, subqueries, and views",
                            "Indexes and query optimization",
                            "Stored procedures and triggers",
                        ]
                    },
                ]
            },
            {
                "title": "Servlets & Spring Core",
                "desc": "Understand the foundation before Spring Boot magic hides it.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Servlets",
                        "subs": [
                            "Servlet lifecycle",
                            "HttpServletRequest and Response",
                            "Session and Cookie management",
                            "Filters and Listeners",
                        ]
                    },
                    {
                        "label": "Spring Core",
                        "subs": [
                            "IoC Container and DI",
                            "@Component, @Service, @Repository",
                            "@Autowired and @Bean",
                            "ApplicationContext lifecycle",
                        ]
                    },
                ]
            },
            {
                "title": "Spring Boot & Hibernate",
                "desc": "The most used tech stack in Java backend jobs.",
                "time": "5–6 weeks",
                "topics": [
                    {
                        "label": "Spring Boot",
                        "subs": [
                            "Auto-configuration and starters",
                            "application.properties setup",
                            "Profiles: dev, prod",
                            "Spring Boot Actuator for health checks",
                        ]
                    },
                    {
                        "label": "Hibernate & JPA",
                        "subs": [
                            "@Entity, @Table, @Column",
                            "@OneToMany, @ManyToMany mappings",
                            "HQL and Criteria API",
                            "Lazy vs Eager loading",
                            "Caching: first-level and second-level",
                        ]
                    },
                    {
                        "label": "Spring Security",
                        "subs": [
                            "SecurityFilterChain configuration",
                            "UserDetailsService",
                            "JWT authentication",
                            "Role-based authorization with @PreAuthorize",
                        ]
                    },
                ]
            },
            {
                "title": "REST APIs & Microservices",
                "desc": "Build scalable APIs and understand distributed architectures.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "REST APIs",
                        "subs": [
                            "@RestController and request mappings",
                            "Request/response with @RequestBody",
                            "Global exception handling",
                            "API documentation with Swagger/OpenAPI",
                        ]
                    },
                    {
                        "label": "Microservices",
                        "subs": [
                            "Monolith vs microservices tradeoffs",
                            "Spring Cloud basics",
                            "Eureka service discovery",
                            "API Gateway with Spring Cloud Gateway",
                            "Feign client for inter-service calls",
                        ]
                    },
                    {
                        "label": "Docker",
                        "subs": [
                            "Dockerfile for Spring Boot",
                            "docker-compose with MySQL",
                            "Container networking",
                            "Environment variables for config",
                        ]
                    },
                ]
            },
        ],

        "backend-developer-python": [
            {
                "title": "Python Core",
                "desc": "Solid Python fundamentals are non-negotiable for backend work.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Python Basics",
                        "subs": [
                            "Variables, data types, operators",
                            "Conditionals and loops",
                            "Functions, *args, **kwargs",
                            "List, dict, set comprehensions",
                        ]
                    },
                    {
                        "label": "OOP",
                        "subs": [
                            "Classes, objects, __init__",
                            "Inheritance and super()",
                            "Dunder methods",
                            "Abstract classes and interfaces",
                        ]
                    },
                    {
                        "label": "File Handling",
                        "subs": [
                            "Reading and writing text files",
                            "Working with JSON",
                            "Working with CSV",
                            "pathlib for path management",
                            "Context managers with 'with'",
                        ]
                    },
                ]
            },
            {
                "title": "SQL & Databases",
                "desc": "Every backend app is only as good as its data layer.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "SQL",
                        "subs": [
                            "SELECT, INSERT, UPDATE, DELETE",
                            "JOINs and subqueries",
                            "Indexes and transactions",
                            "PostgreSQL vs MySQL differences",
                        ]
                    },
                ]
            },
            {
                "title": "Django",
                "desc": "The most complete Python web framework — build full apps fast.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "Django Basics",
                        "subs": [
                            "Project and app structure",
                            "Models, Views, Templates (MVT)",
                            "URL routing with urls.py",
                            "Django admin configuration",
                        ]
                    },
                    {
                        "label": "Django ORM",
                        "subs": [
                            "Model field types",
                            "Migrations workflow",
                            "QuerySet API: filter, annotate, order",
                            "select_related vs prefetch_related",
                            "Signals: post_save, pre_delete",
                        ]
                    },
                ]
            },
            {
                "title": "Django REST Framework",
                "desc": "Build professional REST APIs that power mobile and frontend apps.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "DRF Core",
                        "subs": [
                            "Serializers and ModelSerializer",
                            "APIView and GenericAPIView",
                            "ViewSets and Routers",
                            "Permissions: IsAuthenticated, IsAdminUser",
                        ]
                    },
                    {
                        "label": "Authentication",
                        "subs": [
                            "Session auth vs token auth",
                            "JWT with djangorestframework-simplejwt",
                            "Refresh and access tokens",
                            "Custom authentication backends",
                        ]
                    },
                    {
                        "label": "API Development",
                        "subs": [
                            "Pagination: PageNumber and Cursor",
                            "Filtering with django-filter",
                            "Throttling and rate limiting",
                            "API versioning strategies",
                            "Swagger docs with drf-spectacular",
                        ]
                    },
                ]
            },
            {
                "title": "Docker & Deployment",
                "desc": "Package and ship your Python backend reliably to any environment.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "Docker",
                        "subs": [
                            "Dockerfile for Django",
                            "docker-compose with PostgreSQL and Redis",
                            "Multi-stage builds",
                            "Volume mounts for dev workflow",
                        ]
                    },
                    {
                        "label": "Deployment",
                        "subs": [
                            "Gunicorn as WSGI server",
                            "Nginx as reverse proxy",
                            "Environment variables with python-dotenv",
                            "Deploy to Render, Railway, or EC2",
                            "CI/CD with GitHub Actions",
                        ]
                    },
                ]
            },
        ],

        "data-analytics": [
            {
                "title": "Python for Analytics",
                "desc": "Python is the primary language for data analytics.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "Python Basics",
                        "subs": [
                            "Variables, lists, dicts, loops",
                            "Functions and comprehensions",
                            "Reading files: open(), csv module",
                            "Error handling for data pipelines",
                        ]
                    },
                    {
                        "label": "NumPy",
                        "subs": [
                            "ndarray creation and slicing",
                            "Array math and broadcasting",
                            "Statistical functions: mean, median, std",
                            "Reshaping and stacking arrays",
                        ]
                    },
                ]
            },
            {
                "title": "Pandas",
                "desc": "Pandas is the Swiss Army knife of data manipulation in Python.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "DataFrame Basics",
                        "subs": [
                            "Creating DataFrames from CSV, Excel, SQL",
                            "head(), tail(), info(), describe()",
                            "Selecting: loc, iloc, query",
                            "Filtering with conditions",
                        ]
                    },
                    {
                        "label": "Data Transformation",
                        "subs": [
                            "groupby() and aggregate functions",
                            "merge() and concat() for combining data",
                            "pivot_table for summaries",
                            "apply() and lambda for custom logic",
                        ]
                    },
                    {
                        "label": "Data Cleaning",
                        "subs": [
                            "Handling missing values: fillna, dropna",
                            "Removing duplicates with drop_duplicates",
                            "Fixing data types with astype()",
                            "String cleaning with str accessor",
                            "Outlier detection and removal",
                        ]
                    },
                ]
            },
            {
                "title": "Excel for Analytics",
                "desc": "Excel remains essential for business analytics and reporting.",
                "time": "1–2 weeks",
                "topics": [
                    {
                        "label": "Excel Skills",
                        "subs": [
                            "VLOOKUP and XLOOKUP",
                            "Pivot tables and pivot charts",
                            "Conditional formatting",
                            "Excel formulas: IF, SUMIF, COUNTIF",
                            "Data validation and named ranges",
                        ]
                    },
                ]
            },
            {
                "title": "SQL for Analytics",
                "desc": "Querying databases is the most essential skill for any data analyst.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "SQL Deep Dive",
                        "subs": [
                            "SELECT with aliases and expressions",
                            "JOINs: INNER, LEFT, RIGHT, FULL OUTER",
                            "GROUP BY with HAVING clause",
                            "Window functions: ROW_NUMBER, RANK, LAG",
                            "CTEs and subqueries for readability",
                        ]
                    },
                ]
            },
            {
                "title": "Data Visualization",
                "desc": "Turn raw data into stories that decision-makers can act on.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Python Charts",
                        "subs": [
                            "Matplotlib: line, bar, scatter, histogram",
                            "Seaborn: heatmaps, pairplots, boxplots",
                            "Plotly for interactive charts",
                            "Choosing the right chart type",
                        ]
                    },
                    {
                        "label": "Power BI",
                        "subs": [
                            "Importing data from CSV, SQL, Excel",
                            "Data modeling and relationships",
                            "DAX basics: CALCULATE, SUMX, FILTER",
                            "Building dashboards and reports",
                            "Publishing to Power BI Service",
                        ]
                    },
                    {
                        "label": "Tableau",
                        "subs": [
                            "Connecting to data sources",
                            "Dimensions vs measures",
                            "Building bar, line, and map charts",
                            "Calculated fields and table calculations",
                            "Tableau Public for portfolio projects",
                        ]
                    },
                ]
            },
            {
                "title": "Projects & Portfolio",
                "desc": "Apply everything through end-to-end analytics projects.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Projects",
                        "subs": [
                            "Sales analysis dashboard with Power BI",
                            "Customer churn analysis with Python + Pandas",
                            "SQL analytics on e-commerce database",
                            "Tableau public dashboard for portfolio",
                            "End-to-end: collect → clean → analyze → present",
                        ]
                    },
                ]
            },
        ],

        "data-science": [
            {
                "title": "Python & Data Libraries",
                "desc": "Build your Python data science toolkit from the ground up.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Python Core",
                        "subs": [
                            "Data types, functions, OOP basics",
                            "File I/O and working with JSON/CSV",
                            "Virtual environments and pip",
                            "Jupyter Notebooks workflow",
                        ]
                    },
                    {
                        "label": "NumPy & Pandas",
                        "subs": [
                            "Array operations and broadcasting",
                            "DataFrame manipulation and cleaning",
                            "Merging, grouping, and aggregating data",
                            "Time series with DatetimeIndex",
                        ]
                    },
                ]
            },
            {
                "title": "Statistics",
                "desc": "Statistics is the language of data science. You cannot skip it.",
                "time": "2–3 weeks",
                "topics": [
                    {
                        "label": "Descriptive Stats",
                        "subs": [
                            "Mean, median, mode, variance, std dev",
                            "Percentiles and IQR",
                            "Distributions: normal, binomial, Poisson",
                            "Correlation and covariance",
                        ]
                    },
                    {
                        "label": "Inferential Stats",
                        "subs": [
                            "Hypothesis testing: null vs alternative",
                            "p-value and significance level",
                            "t-test, chi-square, ANOVA",
                            "Confidence intervals",
                            "Central Limit Theorem",
                        ]
                    },
                ]
            },
            {
                "title": "Data Visualization",
                "desc": "Communicate insights clearly through EDA and charts.",
                "time": "2 weeks",
                "topics": [
                    {
                        "label": "Visualization",
                        "subs": [
                            "Matplotlib and Seaborn for EDA",
                            "Plotly for interactive exploration",
                            "Histograms, boxplots, scatter, heatmaps",
                            "Correlation matrices",
                            "Pair plots for feature relationships",
                        ]
                    },
                ]
            },
            {
                "title": "Machine Learning",
                "desc": "The core of data science — teaching machines to learn from data.",
                "time": "5–6 weeks",
                "topics": [
                    {
                        "label": "Supervised Learning",
                        "subs": [
                            "Linear regression and cost function",
                            "Logistic regression for classification",
                            "Decision Trees and Random Forest",
                            "SVM: support vectors and kernels",
                            "KNN: distance metrics and k selection",
                        ]
                    },
                    {
                        "label": "Unsupervised Learning",
                        "subs": [
                            "K-Means clustering",
                            "Hierarchical clustering and dendrograms",
                            "PCA for dimensionality reduction",
                            "DBSCAN for density-based clustering",
                        ]
                    },
                    {
                        "label": "Scikit-Learn",
                        "subs": [
                            "train_test_split and cross-validation",
                            "Pipeline for preprocessing + model",
                            "GridSearchCV and RandomizedSearchCV",
                            "Saving models with joblib/pickle",
                        ]
                    },
                ]
            },
            {
                "title": "Feature Engineering & Evaluation",
                "desc": "The difference between a good model and a great one.",
                "time": "3 weeks",
                "topics": [
                    {
                        "label": "Feature Engineering",
                        "subs": [
                            "Handling missing values: imputation",
                            "Encoding: LabelEncoder, OneHotEncoder",
                            "Feature scaling: StandardScaler, MinMaxScaler",
                            "Creating new features from existing ones",
                            "Feature selection: SelectKBest, RFE",
                        ]
                    },
                    {
                        "label": "Model Evaluation",
                        "subs": [
                            "Classification: accuracy, precision, recall, F1",
                            "Confusion matrix interpretation",
                            "Regression: MAE, MSE, RMSE, R²",
                            "ROC curve and AUC score",
                            "Overfitting vs underfitting: bias-variance",
                        ]
                    },
                ]
            },
            {
                "title": "Projects",
                "desc": "Build a data science portfolio that gets you hired.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "Portfolio Projects",
                        "subs": [
                            "House price prediction (regression)",
                            "Titanic survival (classification)",
                            "Customer segmentation (clustering)",
                            "Sentiment analysis (NLP intro)",
                            "End-to-end: EDA → model → evaluation → report",
                        ]
                    },
                ]
            },
        ],

        "ai-ml": [
            {
                "title": "Python & Math Foundations",
                "desc": "AI/ML is math-heavy. Build your Python and math base first.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "Python for AI",
                        "subs": [
                            "NumPy vectorized operations",
                            "Pandas for data pipelines",
                            "Matplotlib for visualization",
                            "Jupyter Notebooks for experiments",
                        ]
                    },
                    {
                        "label": "Math for ML",
                        "subs": [
                            "Linear algebra: vectors, matrices, dot product",
                            "Calculus: derivatives and gradients",
                            "Statistics: distributions, expectation, variance",
                            "Probability: Bayes theorem, conditional prob",
                        ]
                    },
                ]
            },
            {
                "title": "Machine Learning",
                "desc": "Classical ML is the gateway to deep learning and AI.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "Supervised Learning",
                        "subs": [
                            "Linear and logistic regression",
                            "Decision Trees, Random Forest, Gradient Boosting",
                            "SVM and KNN",
                            "Model evaluation: accuracy, F1, ROC-AUC",
                        ]
                    },
                    {
                        "label": "Unsupervised Learning",
                        "subs": [
                            "K-Means and DBSCAN clustering",
                            "PCA for dimensionality reduction",
                            "Anomaly detection",
                            "Association rules: Apriori",
                        ]
                    },
                ]
            },
            {
                "title": "Deep Learning",
                "desc": "Neural networks that power modern AI — image, text, and beyond.",
                "time": "5–6 weeks",
                "topics": [
                    {
                        "label": "Neural Network Basics",
                        "subs": [
                            "Perceptron and activation functions",
                            "Feedforward network architecture",
                            "Backpropagation and gradient descent",
                            "Batch size, epochs, learning rate",
                        ]
                    },
                    {
                        "label": "CNNs",
                        "subs": [
                            "Convolution layers and filters",
                            "Pooling: max and average",
                            "Image classification with CNNs",
                            "Transfer learning: ResNet, VGG, EfficientNet",
                        ]
                    },
                    {
                        "label": "RNNs & LSTMs",
                        "subs": [
                            "RNN and vanishing gradient problem",
                            "LSTM and GRU cells",
                            "Sequence-to-sequence models",
                            "Time series forecasting with LSTM",
                        ]
                    },
                ]
            },
            {
                "title": "TensorFlow",
                "desc": "Industry-standard deep learning framework by Google.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "TensorFlow & Keras",
                        "subs": [
                            "Sequential and Functional API models",
                            "Layers: Dense, Conv2D, LSTM, Dropout",
                            "Compiling: optimizer, loss, metrics",
                            "Callbacks: EarlyStopping, ModelCheckpoint",
                            "Saving and loading models",
                        ]
                    },
                    {
                        "label": "Training Pipeline",
                        "subs": [
                            "tf.data for efficient data loading",
                            "Image augmentation with tf.image",
                            "Custom training loops",
                            "TensorBoard for monitoring",
                            "GPU training with CUDA",
                        ]
                    },
                ]
            },
            {
                "title": "NLP",
                "desc": "Natural Language Processing — teaching machines to understand text.",
                "time": "3–4 weeks",
                "topics": [
                    {
                        "label": "NLP Basics",
                        "subs": [
                            "Tokenization, stemming, lemmatization",
                            "Bag of Words and TF-IDF",
                            "Word embeddings: Word2Vec, GloVe",
                            "Named Entity Recognition (NER)",
                        ]
                    },
                    {
                        "label": "Transformers",
                        "subs": [
                            "Attention mechanism explained",
                            "BERT and its variants",
                            "Hugging Face pipeline API",
                            "Fine-tuning pre-trained models",
                            "Text classification and Q&A with transformers",
                        ]
                    },
                ]
            },
            {
                "title": "LLMs & Projects",
                "desc": "The cutting edge of AI — large language models and building with them.",
                "time": "4–5 weeks",
                "topics": [
                    {
                        "label": "LLMs",
                        "subs": [
                            "GPT architecture overview",
                            "Prompt engineering techniques",
                            "LangChain for LLM apps",
                            "RAG: Retrieval Augmented Generation",
                            "OpenAI and Gemini API integration",
                        ]
                    },
                    {
                        "label": "Projects",
                        "subs": [
                            "Image classifier with TensorFlow",
                            "Sentiment analysis with BERT",
                            "Chatbot with LangChain + Gemini",
                            "Object detection with YOLO",
                            "End-to-end ML pipeline with deployment",
                        ]
                    },
                ]
            },
        ],
    }

    context = {
        "course_name": course_name.replace("-", " ").title(),
        "roadmap_phases": roadmaps.get(course_name, []),
    }

    return render(
        request,
        "roadmap.html",
        context
    )


def learn_course(request, course_name):
    materials = CourseResource.objects.filter(course_name=course_name, resource_type="PDF")
    links = CourseResource.objects.filter(course_name=course_name, resource_type="LINK")
    videos = CourseResource.objects.filter(course_name=course_name, resource_type="VIDEO")
    ai_mentors = CourseResource.objects.filter(course_name=course_name, resource_type="AI_MENTOR")
    return render(request, "learn_course.html", {
        "course_name": course_name.replace("-", " ").title(),
        "materials": materials,
        "links": links,
        "videos": videos,
        "ai_mentors": ai_mentors
    })

def quiz_home(request, course_name):
    return render(request, "quiz_home.html", {
        "course_name": course_name.replace("-", " ").title(),
        "course_slug": course_name,
    })




def start_quiz(request, course_name):
    difficulty = request.GET.get("difficulty", "easy")
    num_questions = int(request.GET.get("num_questions", 10))

    all_questions = {

        # ─────────────────────────────────────────────
        # 1. JAVA FULL STACK
        # ─────────────────────────────────────────────
        "java-full-stack": {
            "easy": [
                {"question": "What does JVM stand for?", "options": ["Java Virtual Machine", "Java Variable Method", "Java Verified Module", "Java Vendor Machine"], "answer": "Java Virtual Machine"},
                {"question": "Which keyword is used to create a class in Java?", "options": ["class", "Class", "define", "struct"], "answer": "class"},
                {"question": "What is the default value of an int in Java?", "options": ["0", "null", "1", "-1"], "answer": "0"},
                {"question": "Which method is the entry point of a Java program?", "options": ["main()", "start()", "run()", "init()"], "answer": "main()"},
                {"question": "Which of these is NOT a Java primitive type?", "options": ["String", "int", "boolean", "char"], "answer": "String"},
                {"question": "What does OOP stand for?", "options": ["Object Oriented Programming", "Object Ordered Process", "Open Object Programming", "None"], "answer": "Object Oriented Programming"},
                {"question": "Which symbol is used for single-line comments in Java?", "options": ["//", "#", "/*", "--"], "answer": "//"},
                {"question": "What is the size of an int in Java?", "options": ["4 bytes", "2 bytes", "8 bytes", "1 byte"], "answer": "4 bytes"},
                {"question": "Which class is the parent of all Java classes?", "options": ["Object", "Base", "Super", "Root"], "answer": "Object"},
                {"question": "What is used to print output in Java?", "options": ["System.out.println()", "print()", "echo()", "console.log()"], "answer": "System.out.println()"},
                {"question": "Which keyword prevents a variable from being changed?", "options": ["final", "static", "const", "fixed"], "answer": "final"},
                {"question": "Which loop runs at least once?", "options": ["do-while", "for", "while", "foreach"], "answer": "do-while"},
                {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Transfer Markup Language", "Hyper Tool Making Language", "None"], "answer": "HyperText Markup Language"},
                {"question": "Which SQL command retrieves data?", "options": ["SELECT", "GET", "FETCH", "READ"], "answer": "SELECT"},
                {"question": "What is Spring Boot used for?", "options": ["Building Java applications quickly", "Styling web pages", "Managing databases", "Testing code"], "answer": "Building Java applications quickly"},
                {"question": "Which HTTP method is used to fetch data?", "options": ["GET", "POST", "PUT", "DELETE"], "answer": "GET"},
                {"question": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Creative Style System", "Computer Style Sheets", "None"], "answer": "Cascading Style Sheets"},
                {"question": "What is an API?", "options": ["Application Programming Interface", "Application Process Integration", "Auto Programming Interface", "None"], "answer": "Application Programming Interface"},
                {"question": "Which tag is used to link CSS in HTML?", "options": ["<link>", "<style>", "<css>", "<script>"], "answer": "<link>"},
                {"question": "What does JDK stand for?", "options": ["Java Development Kit", "Java Deploy Kit", "Java Debug Kernel", "None"], "answer": "Java Development Kit"},
                {"question": "Which annotation marks a Spring REST controller?", "options": ["@RestController", "@Controller", "@Bean", "@Service"], "answer": "@RestController"},
                {"question": "What is MySQL?", "options": ["A relational database", "A programming language", "A frontend framework", "An OS"], "answer": "A relational database"},
                {"question": "Which React hook manages state?", "options": ["useState", "useEffect", "useRef", "useContext"], "answer": "useState"},
                {"question": "What does JDBC stand for?", "options": ["Java Database Connectivity", "Java Data Bridge Connector", "Java Direct Base Connection", "None"], "answer": "Java Database Connectivity"},
                {"question": "Which keyword is used for inheritance in Java?", "options": ["extends", "implements", "inherits", "super"], "answer": "extends"},
                {"question": "What is a constructor?", "options": ["A method called when an object is created", "A loop", "A data type", "A class"], "answer": "A method called when an object is created"},
                {"question": "What does REST stand for?", "options": ["Representational State Transfer", "Remote Execution Standard Tool", "Rapid Endpoint Service Transfer", "None"], "answer": "Representational State Transfer"},
                {"question": "Which SQL keyword removes duplicate rows?", "options": ["DISTINCT", "UNIQUE", "REMOVE", "FILTER"], "answer": "DISTINCT"},
                {"question": "What is Git used for?", "options": ["Version control", "Database management", "UI design", "Server hosting"], "answer": "Version control"},
                {"question": "Which company developed Java?", "options": ["Sun Microsystems", "Microsoft", "Apple", "Google"], "answer": "Sun Microsystems"},
            ],
            "medium": [
                {"question": "What is the difference between == and .equals() in Java?", "options": ["== compares references, .equals() compares values", "Both compare values", "== compares values, .equals() compares references", "No difference"], "answer": "== compares references, .equals() compares values"},
                {"question": "What is method overloading?", "options": ["Same method name with different parameters", "Overriding a parent method", "Calling a method multiple times", "None"], "answer": "Same method name with different parameters"},
                {"question": "What is the purpose of the @Autowired annotation?", "options": ["Dependency Injection", "Defining a REST endpoint", "Creating a database table", "None"], "answer": "Dependency Injection"},
                {"question": "Which collection does not allow duplicate values?", "options": ["HashSet", "ArrayList", "LinkedList", "Vector"], "answer": "HashSet"},
                {"question": "What is Spring Data JPA used for?", "options": ["Database operations without SQL", "Building REST APIs", "Frontend rendering", "Authentication"], "answer": "Database operations without SQL"},
                {"question": "What is the default HTTP port?", "options": ["80", "8080", "443", "3000"], "answer": "80"},
                {"question": "What is PreparedStatement in JDBC?", "options": ["A precompiled SQL statement", "A type of loop", "An ORM", "A Spring annotation"], "answer": "A precompiled SQL statement"},
                {"question": "What does @Entity annotation do in Spring?", "options": ["Marks a class as a database table", "Marks a REST controller", "Injects a dependency", "Configures a bean"], "answer": "Marks a class as a database table"},
                {"question": "What is CORS?", "options": ["Cross-Origin Resource Sharing", "Central Object Routing System", "Cross Object REST Service", "None"], "answer": "Cross-Origin Resource Sharing"},
                {"question": "Which HTTP status code means 'Not Found'?", "options": ["404", "200", "500", "301"], "answer": "404"},
                {"question": "What is the use of React's useEffect hook?", "options": ["Handle side effects like API calls", "Manage local state", "Style components", "Route pages"], "answer": "Handle side effects like API calls"},
                {"question": "What is Flexbox used for in CSS?", "options": ["Layout of elements in one direction", "Animations", "Media queries", "Typography"], "answer": "Layout of elements in one direction"},
                {"question": "What does docker-compose do?", "options": ["Manages multi-container apps", "Builds frontend", "Runs SQL queries", "Manages Java packages"], "answer": "Manages multi-container apps"},
                {"question": "What is JSP?", "options": ["Java Server Pages", "JavaScript Processor", "Java Servlet Protocol", "None"], "answer": "Java Server Pages"},
                {"question": "What is the purpose of @RequestMapping?", "options": ["Maps HTTP requests to handler methods", "Maps database columns", "Configures security", "None"], "answer": "Maps HTTP requests to handler methods"},
                {"question": "What is JWT?", "options": ["JSON Web Token", "Java Web Transfer", "JavaScript Web Tool", "None"], "answer": "JSON Web Token"},
                {"question": "Which SQL clause filters grouped results?", "options": ["HAVING", "WHERE", "GROUP", "FILTER"], "answer": "HAVING"},
                {"question": "What is an interface in Java?", "options": ["A contract with abstract methods", "A class with static methods", "A type of loop", "A data structure"], "answer": "A contract with abstract methods"},
                {"question": "What is lazy loading in Hibernate?", "options": ["Loading data only when accessed", "Loading all data at startup", "Caching data", "Deleting data"], "answer": "Loading data only when accessed"},
                {"question": "What does git commit do?", "options": ["Saves changes to local repo", "Pushes code to remote", "Creates a branch", "Merges branches"], "answer": "saves changes to local repo"},
                {"question": "What is Bootstrap used for?", "options": ["Responsive UI design", "Backend development", "Database queries", "Version control"], "answer": "Responsive UI design"},
                {"question": "What is the difference between GET and POST?", "options": ["GET fetches data, POST sends data", "GET deletes data, POST updates", "Both are same", "POST fetches data"], "answer": "GET fetches data, POST sends data"},
                {"question": "What does @PathVariable do in Spring?", "options": ["Extracts value from URL path", "Maps request body", "Configures security", "None"], "answer": "Extracts value from URL path"},
                {"question": "What is polymorphism?", "options": ["One interface, multiple implementations", "Multiple classes, one method", "Inheritance only", "None"], "answer": "One interface, multiple implementations"},
                {"question": "What is Axios used for in React?", "options": ["Making HTTP API calls", "Managing state", "Routing", "Styling"], "answer": "Making HTTP API calls"},
                {"question": "What is a Servlet?", "options": ["A Java class that handles HTTP requests", "A database connector", "A CSS framework", "None"], "answer": "A Java class that handles HTTP requests"},
                {"question": "Which annotation defines a service layer class in Spring?", "options": ["@Service", "@Controller", "@Entity", "@Repository"], "answer": "@Service"},
                {"question": "What is encapsulation?", "options": ["Hiding internal data using access modifiers", "Inheriting from a class", "Overriding methods", "None"], "answer": "Hiding internal data using access modifiers"},
                {"question": "What is the use of INNER JOIN in SQL?", "options": ["Returns matching rows from both tables", "Returns all rows from left table", "Returns all rows", "Deletes duplicates"], "answer": "Returns matching rows from both tables"},
                {"question": "What does useState return in React?", "options": ["A state variable and a setter function", "Only a state variable", "Only a setter", "An object"], "answer": "A state variable and a setter function"},
            ],
            "hard": [
                {"question": "What is the difference between @Controller and @RestController?", "options": ["@RestController adds @ResponseBody automatically", "@Controller is for REST APIs", "Both are identical", "@RestController is deprecated"], "answer": "@RestController adds @ResponseBody automatically"},
                {"question": "What is the N+1 problem in Hibernate?", "options": ["Extra queries fired for each associated entity", "Loading N records at once", "A SQL syntax error", "An indexing problem"], "answer": "Extra queries fired for each associated entity"},
                {"question": "What is Spring Security's SecurityFilterChain?", "options": ["A chain of filters that handle authentication/authorization", "A database connection pool", "A REST endpoint", "A logging utility"], "answer": "A chain of filters that handle authentication/authorization"},
                {"question": "What is the difference between INNER JOIN and LEFT JOIN?", "options": ["LEFT JOIN returns all rows from left table including unmatched", "INNER JOIN returns all rows", "LEFT JOIN is faster", "No difference"], "answer": "LEFT JOIN returns all rows from left table including unmatched"},
                {"question": "What is a memory leak in Java?", "options": ["Objects not garbage collected due to unwanted references", "Running out of RAM", "Stack overflow", "Null pointer exception"], "answer": "Objects not garbage collected due to unwanted references"},
                {"question": "What is the role of DispatcherServlet in Spring MVC?", "options": ["Front controller that routes requests", "Database handler", "Security filter", "View renderer"], "answer": "Front controller that routes requests"},
                {"question": "What is the difference between HashSet and TreeSet?", "options": ["TreeSet maintains sorted order, HashSet does not", "HashSet is sorted", "Both are same", "TreeSet allows duplicates"], "answer": "TreeSet maintains sorted order, HashSet does not"},
                {"question": "What is a transaction in JDBC?", "options": ["A group of SQL operations treated as one unit", "A prepared statement", "A connection object", "None"], "answer": "A group of SQL operations treated as one unit"},
                {"question": "What is the difference between forward() and redirect() in Servlets?", "options": ["forward() stays server-side, redirect() sends new request from client", "Both are same", "redirect() is server-side", "forward() changes URL"], "answer": "forward() stays server-side, redirect() sends new request from client"},
                {"question": "What is Circuit Breaker pattern in Microservices?", "options": ["Stops calls to a failing service temporarily", "Routes traffic between services", "Encrypts data", "Balances load"], "answer": "Stops calls to a failing service temporarily"},
                {"question": "What does @Transactional annotation do in Spring?", "options": ["Manages database transactions automatically", "Maps HTTP requests", "Injects dependencies", "Configures security"], "answer": "Manages database transactions automatically"},
                {"question": "What is virtual DOM in React?", "options": ["A lightweight copy of real DOM for efficient updates", "A server-side renderer", "A database", "A CSS engine"], "answer": "A lightweight copy of real DOM for efficient updates"},
                {"question": "What is connection pooling?", "options": ["Reusing database connections to improve performance", "Pooling HTTP requests", "Caching SQL results", "None"], "answer": "Reusing database connections to improve performance"},
                {"question": "What is the difference between Abstract class and Interface in Java?", "options": ["Abstract class can have method bodies, Interface cannot (pre Java 8)", "Interface can have constructors", "Both are identical", "Abstract class supports multiple inheritance"], "answer": "Abstract class can have method bodies, Interface cannot (pre Java 8)"},
                {"question": "What is Eureka in Spring Cloud?", "options": ["A service discovery server", "A database", "A security tool", "A logging framework"], "answer": "A service discovery server"},
                {"question": "What is the purpose of @PreAuthorize in Spring Security?", "options": ["Checks authorization before method execution", "Authenticates users", "Generates JWT", "None"], "answer": "Checks authorization before method execution"},
                {"question": "What is second-level caching in Hibernate?", "options": ["Cache shared across sessions", "Cache per session", "Query result cache", "None"], "answer": "Cache shared across sessions"},
                {"question": "What is CSRF and how does Spring prevent it?", "options": ["Cross-Site Request Forgery, prevented by CSRF tokens", "Code injection, prevented by encoding", "SQL injection, prevented by parameterized queries", "None"], "answer": "Cross-Site Request Forgery, prevented by CSRF tokens"},
                {"question": "What is idempotency in REST APIs?", "options": ["Same request gives same result regardless of how many times called", "Request is cached", "Request is encrypted", "None"], "answer": "Same request gives same result regardless of how many times called"},
                {"question": "What is Feign Client in Spring Cloud?", "options": ["A declarative HTTP client for calling other microservices", "A security library", "An ORM", "A testing tool"], "answer": "A declarative HTTP client for calling other microservices"},
                {"question": "What is the difference between @RequestParam and @PathVariable?", "options": ["@RequestParam reads query params, @PathVariable reads URL segments", "Both are same", "@PathVariable reads query params", "None"], "answer": "@RequestParam reads query params, @PathVariable reads URL segments"},
                {"question": "How does React's reconciliation algorithm work?", "options": ["Diffs virtual DOM trees and updates only changed nodes", "Re-renders entire DOM on every change", "Uses server-side rendering", "None"], "answer": "Diffs virtual DOM trees and updates only changed nodes"},
                {"question": "What is Docker layer caching?", "options": ["Reuses unchanged layers from previous builds to speed up builds", "Caches database queries", "Stores environment variables", "None"], "answer": "Reuses unchanged layers from previous builds to speed up builds"},
                {"question": "What is the difference between optimistic and pessimistic locking?", "options": ["Optimistic assumes no conflict, pessimistic locks record immediately", "Both lock records the same way", "Optimistic is slower", "None"], "answer": "Optimistic assumes no conflict, pessimistic locks record immediately"},
                {"question": "What is API Gateway pattern?", "options": ["Single entry point for all microservice requests", "A database proxy", "A frontend framework", "None"], "answer": "Single entry point for all microservice requests"},
                {"question": "What is the use of @ControllerAdvice?", "options": ["Global exception handling across all controllers", "Configures security", "Maps endpoints", "None"], "answer": "Global exception handling across all controllers"},
                {"question": "What is HQL?", "options": ["Hibernate Query Language, works with entity objects", "HTML Query Language", "HTTP Query Language", "None"], "answer": "Hibernate Query Language, works with entity objects"},
                {"question": "What is the difference between List and Set in Java?", "options": ["List allows duplicates and maintains order, Set does not allow duplicates", "Set allows duplicates", "Both are same", "List has no order"], "answer": "List allows duplicates and maintains order, Set does not allow duplicates"},
                {"question": "What is Spring Boot Actuator?", "options": ["Provides production monitoring endpoints", "Manages security", "Handles database migrations", "None"], "answer": "Provides production monitoring endpoints"},
                {"question": "What is the CAP theorem in distributed systems?", "options": ["A system can guarantee only 2 of: Consistency, Availability, Partition tolerance", "A caching strategy", "A sorting algorithm", "None"], "answer": "A system can guarantee only 2 of: Consistency, Availability, Partition tolerance"},
            ],
        },

        # ─────────────────────────────────────────────
        # 2. PYTHON FULL STACK
        # ─────────────────────────────────────────────
        "python-full-stack": {
            "easy": [
                {"question": "What is Python?", "options": ["A high-level programming language", "A database", "An OS", "A markup language"], "answer": "A high-level programming language"},
                {"question": "Which keyword defines a function in Python?", "options": ["def", "function", "fun", "define"], "answer": "def"},
                {"question": "What is Django?", "options": ["A Python web framework", "A database", "A JS library", "A CSS tool"], "answer": "A Python web framework"},
                {"question": "Which file contains URL patterns in Django?", "options": ["urls.py", "views.py", "models.py", "settings.py"], "answer": "urls.py"},
                {"question": "What does pip do?", "options": ["Installs Python packages", "Runs Python scripts", "Manages databases", "Compiles code"], "answer": "Installs Python packages"},
                {"question": "What is a list in Python?", "options": ["An ordered mutable collection", "An ordered immutable collection", "An unordered collection", "A key-value store"], "answer": "An ordered mutable collection"},
                {"question": "What is the extension of Python files?", "options": [".py", ".python", ".pt", ".pyc"], "answer": ".py"},
                {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Transfer Markup Language", "None", "Hyper Tool Making Language"], "answer": "HyperText Markup Language"},
                {"question": "Which method reads CSV files in Pandas?", "options": ["read_csv()", "load_csv()", "open_csv()", "get_csv()"], "answer": "read_csv()"},
                {"question": "What is React?", "options": ["A JavaScript library for building UIs", "A Python framework", "A database", "A CSS tool"], "answer": "A JavaScript library for building UIs"},
                {"question": "Which SQL command adds new records?", "options": ["INSERT", "ADD", "CREATE", "PUT"], "answer": "INSERT"},
                {"question": "What is a virtual environment in Python?", "options": ["An isolated Python environment for a project", "A cloud server", "A database", "A testing tool"], "answer": "An isolated Python environment for a project"},
                {"question": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Creative Style Sheets", "None", "Computer Style Sheets"], "answer": "Cascading Style Sheets"},
                {"question": "What is Git?", "options": ["A version control system", "A database", "A web server", "A framework"], "answer": "A version control system"},
                {"question": "What is a tuple in Python?", "options": ["An ordered immutable collection", "A mutable list", "A dictionary", "A set"], "answer": "An ordered immutable collection"},
                {"question": "What is Docker?", "options": ["A containerization platform", "A database", "A frontend library", "A CI tool"], "answer": "A containerization platform"},
                {"question": "What does GET mean in HTTP?", "options": ["Fetch/retrieve data", "Send data", "Delete data", "Update data"], "answer": "Fetch/retrieve data"},
                {"question": "What is a dictionary in Python?", "options": ["A key-value data structure", "An ordered list", "A set", "A tuple"], "answer": "A key-value data structure"},
                {"question": "Which Django file defines data models?", "options": ["models.py", "views.py", "urls.py", "forms.py"], "answer": "models.py"},
                {"question": "What is NumPy used for?", "options": ["Numerical computing with arrays", "Building web apps", "Managing databases", "Styling HTML"], "answer": "Numerical computing with arrays"},
                {"question": "What is an f-string in Python?", "options": ["A formatted string literal", "A file string", "A function string", "None"], "answer": "A formatted string literal"},
                {"question": "What is useState in React?", "options": ["A hook to manage component state", "A CSS utility", "A routing tool", "None"], "answer": "A hook to manage component state"},
                {"question": "What does DRF stand for?", "options": ["Django REST Framework", "Django Resource Files", "Dynamic REST Format", "None"], "answer": "Django REST Framework"},
                {"question": "Which command creates a new Django project?", "options": ["django-admin startproject", "django startproject", "python start", "None"], "answer": "django-admin startproject"},
                {"question": "What is Flexbox?", "options": ["A CSS layout model", "A Python library", "A React hook", "A database query"], "answer": "A CSS layout model"},
                {"question": "What does async/await do in JavaScript?", "options": ["Handles asynchronous operations", "Loops through arrays", "Styles elements", "Routes pages"], "answer": "Handles asynchronous operations"},
                {"question": "What is PostgreSQL?", "options": ["An open-source relational database", "A Python framework", "A frontend tool", "None"], "answer": "An open-source relational database"},
                {"question": "What is Bootstrap?", "options": ["A CSS framework for responsive design", "A Python library", "A database", "A JS framework"], "answer": "A CSS framework for responsive design"},
                {"question": "Which keyword is used for class inheritance in Python?", "options": ["class Child(Parent):", "inherits", "extends", "super"], "answer": "class Child(Parent):"},
                {"question": "What is an ORM?", "options": ["Object Relational Mapper", "Open REST Module", "Object Routing Method", "None"], "answer": "Object Relational Mapper"},
            ],
            "medium": [
                {"question": "What is the difference between Django's filter() and get()?", "options": ["filter() returns QuerySet, get() returns single object", "Both return QuerySets", "get() returns a list", "No difference"], "answer": "filter() returns QuerySet, get() returns single object"},
                {"question": "What is a Django migration?", "options": ["A file that tracks database schema changes", "A URL redirect", "A template tag", "A security setting"], "answer": "A file that tracks database schema changes"},
                {"question": "What is *args in Python?", "options": ["Passes variable number of positional arguments", "A pointer", "A list argument", "None"], "answer": "Passes variable number of positional arguments"},
                {"question": "What is a decorator in Python?", "options": ["A function that wraps another function", "A class method", "A CSS property", "None"], "answer": "A function that wraps another function"},
                {"question": "What is JWT used for?", "options": ["Stateless authentication", "Database queries", "CSS styling", "None"], "answer": "Stateless authentication"},
                {"question": "What is select_related() in Django ORM?", "options": ["Reduces queries by joining related objects with SQL JOIN", "Filters querysets", "Orders results", "None"], "answer": "Reduces queries by joining related objects with SQL JOIN"},
                {"question": "What is Pandas groupby() used for?", "options": ["Grouping data and applying aggregate functions", "Filtering rows", "Renaming columns", "None"], "answer": "Grouping data and applying aggregate functions"},
                {"question": "What is React Router used for?", "options": ["Client-side navigation between pages", "State management", "API calls", "None"], "answer": "Client-side navigation between pages"},
                {"question": "What is a Dockerfile?", "options": ["A script to build a Docker image", "A Python config file", "A Django settings file", "None"], "answer": "A script to build a Docker image"},
                {"question": "What is Axios?", "options": ["A promise-based HTTP client for JavaScript", "A Python HTTP library", "A database driver", "None"], "answer": "A promise-based HTTP client for JavaScript"},
                {"question": "What does CSRF protection do in Django?", "options": ["Prevents cross-site request forgery attacks", "Encrypts passwords", "Manages sessions", "None"], "answer": "Prevents cross-site request forgery attacks"},
                {"question": "What is a ModelSerializer in DRF?", "options": ["Converts Django models to JSON automatically", "A database model", "A URL configuration", "None"], "answer": "Converts Django models to JSON automatically"},
                {"question": "What is the use of __str__ in Python?", "options": ["Returns a human-readable string representation of an object", "Converts to integer", "Compares objects", "None"], "answer": "Returns a human-readable string representation of an object"},
                {"question": "What is Redux used for?", "options": ["Global state management in React apps", "Routing", "API calls", "Styling"], "answer": "Global state management in React apps"},
                {"question": "What is the difference between list and tuple?", "options": ["List is mutable, tuple is immutable", "Tuple is mutable", "Both are mutable", "No difference"], "answer": "List is mutable, tuple is immutable"},
                {"question": "What is a ViewSet in DRF?", "options": ["A class combining multiple views for a model", "A URL configuration", "A serializer", "None"], "answer": "A class combining multiple views for a model"},
                {"question": "What does git push do?", "options": ["Uploads local commits to remote repo", "Saves changes locally", "Creates a branch", "Merges branches"], "answer": "Uploads local commits to remote repo"},
                {"question": "What is Gunicorn?", "options": ["A Python WSGI HTTP server", "A database", "A CSS framework", "None"], "answer": "A Python WSGI HTTP server"},
                {"question": "What is a lambda function in Python?", "options": ["An anonymous single-expression function", "A class method", "A recursive function", "None"], "answer": "An anonymous single-expression function"},
                {"question": "What is the use of useEffect in React?", "options": ["Run side effects after component renders", "Manage state", "Route pages", "Style components"], "answer": "Run side effects after component renders"},
                {"question": "What is Django admin?", "options": ["An auto-generated backend interface to manage models", "A frontend tool", "A REST API", "None"], "answer": "An auto-generated backend interface to manage models"},
                {"question": "What is docker-compose used for?", "options": ["Running multi-container Docker applications", "Writing Dockerfiles", "Building images only", "None"], "answer": "Running multi-container Docker applications"},
                {"question": "What does fillna() do in Pandas?", "options": ["Fills missing values", "Removes rows", "Renames columns", "None"], "answer": "Fills missing values"},
                {"question": "What is a foreign key in SQL?", "options": ["A field that references a primary key in another table", "A unique key", "A composite key", "None"], "answer": "A field that references a primary key in another table"},
                {"question": "What is the purpose of CSS Grid?", "options": ["Two-dimensional layout of rows and columns", "One-dimensional layout", "Animations", "Fonts"], "answer": "Two-dimensional layout of rows and columns"},
                {"question": "What is NumPy broadcasting?", "options": ["Operations on arrays of different shapes", "Sending data over network", "Printing arrays", "None"], "answer": "Operations on arrays of different shapes"},
                {"question": "What is a class-based view in Django?", "options": ["A view written as a Python class with methods per HTTP verb", "A function-based view", "A template", "None"], "answer": "A view written as a Python class with methods per HTTP verb"},
                {"question": "What is pagination in DRF?", "options": ["Splitting large querysets into pages", "Filtering data", "Sorting data", "None"], "answer": "Splitting large querysets into pages"},
                {"question": "What is Webpack?", "options": ["A JavaScript module bundler", "A Python tool", "A database", "A framework"], "answer": "A JavaScript module bundler"},
                {"question": "What does reverse() do in Django?", "options": ["Returns URL from view name", "Reverses a list", "Redirects to home", "None"], "answer": "Returns URL from view name"},
            ],
            "hard": [
                {"question": "What is the GIL in Python?", "options": ["Global Interpreter Lock that allows only one thread to execute at a time", "A garbage collection mechanism", "A module loader", "None"], "answer": "Global Interpreter Lock that allows only one thread to execute at a time"},
                {"question": "What is prefetch_related() vs select_related() in Django?", "options": ["prefetch_related does separate queries for M2M/reverse FK, select_related does SQL JOINs", "Both do the same SQL JOIN", "prefetch_related uses JOINs", "No difference"], "answer": "prefetch_related does separate queries for M2M/reverse FK, select_related does SQL JOINs"},
                {"question": "What is a Python generator?", "options": ["A function that yields values lazily", "A class that generates objects", "A type of list", "None"], "answer": "A function that yields values lazily"},
                {"question": "What is the difference between authentication and authorization?", "options": ["Authentication verifies identity, authorization checks permissions", "Both are the same", "Authorization verifies identity", "None"], "answer": "Authentication verifies identity, authorization checks permissions"},
                {"question": "How does Django's ORM prevent SQL injection?", "options": ["By using parameterized queries internally", "By escaping all HTML", "By using HTTPS", "None"], "answer": "By using parameterized queries internally"},
                {"question": "What is a metaclass in Python?", "options": ["A class that defines the behavior of other classes", "A base class", "A decorator", "None"], "answer": "A class that defines the behavior of other classes"},
                {"question": "What is database indexing?", "options": ["A data structure that speeds up query lookups", "A backup mechanism", "A caching strategy", "None"], "answer": "A data structure that speeds up query lookups"},
                {"question": "What is the React Context API used for?", "options": ["Passing data through component tree without props", "Managing HTTP calls", "Routing", "None"], "answer": "Passing data through component tree without props"},
                {"question": "What is WSGI?", "options": ["Web Server Gateway Interface — Python standard for web servers and apps", "A Django utility", "A database adapter", "None"], "answer": "Web Server Gateway Interface — Python standard for web servers and apps"},
                {"question": "What is the N+1 query problem in Django ORM?", "options": ["Firing one extra query per related object instead of a JOIN", "A pagination issue", "A cache miss", "None"], "answer": "Firing one extra query per related object instead of a JOIN"},
                {"question": "What is a Python context manager?", "options": ["An object that manages setup and teardown using 'with' statement", "A thread manager", "A memory manager", "None"], "answer": "An object that manages setup and teardown using 'with' statement"},
                {"question": "What is rate limiting in APIs?", "options": ["Restricting the number of requests a client can make in a time period", "Limiting API response size", "Caching responses", "None"], "answer": "Restricting the number of requests a client can make in a time period"},
                {"question": "What are signals in Django?", "options": ["Hooks that fire on model events like save or delete", "HTTP signals", "Error events", "None"], "answer": "Hooks that fire on model events like save or delete"},
                {"question": "What is CI/CD?", "options": ["Continuous Integration and Continuous Deployment", "Code Integration and Code Deployment", "None", "Central Index Continuous Delivery"], "answer": "Continuous Integration and Continuous Deployment"},
                {"question": "What is memoization?", "options": ["Caching function results to avoid redundant computation", "A memory type", "A sorting algorithm", "None"], "answer": "Caching function results to avoid redundant computation"},
                {"question": "What is the difference between process and thread?", "options": ["Process has its own memory space, threads share memory", "Threads have own memory", "Both are identical", "None"], "answer": "Process has its own memory space, threads share memory"},
                {"question": "What is a race condition?", "options": ["When two threads access shared data simultaneously causing unpredictable results", "A performance benchmark", "A deadlock", "None"], "answer": "When two threads access shared data simultaneously causing unpredictable results"},
                {"question": "What is OAuth2?", "options": ["An authorization framework for delegated access", "A database protocol", "An encryption standard", "None"], "answer": "An authorization framework for delegated access"},
                {"question": "What is horizontal vs vertical scaling?", "options": ["Horizontal adds more servers, vertical upgrades existing server", "Vertical adds servers", "Both add servers", "None"], "answer": "Horizontal adds more servers, vertical upgrades existing server"},
                {"question": "What is a deadlock?", "options": ["Two processes blocking each other waiting for resources", "A memory leak", "An infinite loop", "None"], "answer": "Two processes blocking each other waiting for resources"},
                {"question": "What does ACID stand for in databases?", "options": ["Atomicity, Consistency, Isolation, Durability", "Availability, Consistency, Integrity, Durability", "None", "Atomicity, Concurrency, Isolation, Delivery"], "answer": "Atomicity, Consistency, Isolation, Durability"},
                {"question": "What is a reverse proxy?", "options": ["A server that forwards client requests to backend servers", "A caching server only", "A database proxy", "None"], "answer": "A server that forwards client requests to backend servers"},
                {"question": "What is server-side rendering vs client-side rendering?", "options": ["SSR renders HTML on server, CSR renders in browser", "CSR renders on server", "Both are identical", "None"], "answer": "SSR renders HTML on server, CSR renders in browser"},
                {"question": "What are environment variables?", "options": ["Configuration values stored outside source code", "Python variables", "Database columns", "None"], "answer": "Configuration values stored outside source code"},
                {"question": "What is a webhook?", "options": ["HTTP callback triggered by an event", "A web scraper", "A REST endpoint", "None"], "answer": "HTTP callback triggered by an event"},
                {"question": "What is the purpose of Nginx?", "options": ["A web server and reverse proxy", "A database", "A Python WSGI server", "None"], "answer": "A web server and reverse proxy"},
                {"question": "What is lazy evaluation in Python?", "options": ["Delaying computation until result is needed", "A slow algorithm", "A caching strategy", "None"], "answer": "Delaying computation until result is needed"},
                {"question": "What is a microservice architecture?", "options": ["App broken into small independent services communicating via APIs", "A monolithic app", "A database architecture", "None"], "answer": "App broken into small independent services communicating via APIs"},
                {"question": "What is the purpose of .gitignore?", "options": ["Specifies files Git should not track", "Ignores Git errors", "Resets the repo", "None"], "answer": "Specifies files Git should not track"},
                {"question": "What is connection pooling in databases?", "options": ["Reusing existing DB connections to improve performance", "Creating multiple databases", "Caching queries", "None"], "answer": "Reusing existing DB connections to improve performance"},
            ],
        },

        # ─────────────────────────────────────────────
        # 3. FRONTEND DEVELOPER
        # ─────────────────────────────────────────────
        "frontend-developer": {
            "easy": [
                {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Transfer Markup Language", "Hyper Tool Making Language", "None"], "answer": "HyperText Markup Language"},
                {"question": "Which tag creates a hyperlink?", "options": ["<a>", "<link>", "<href>", "<nav>"], "answer": "<a>"},
                {"question": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Creative Style Sheets", "Computer Style Sheets", "None"], "answer": "Cascading Style Sheets"},
                {"question": "Which CSS property changes text color?", "options": ["color", "text-color", "font-color", "foreground"], "answer": "color"},
                {"question": "What is JavaScript?", "options": ["A programming language for web interactivity", "A markup language", "A styling language", "A database"], "answer": "A programming language for web interactivity"},
                {"question": "Which HTML tag defines a paragraph?", "options": ["<p>", "<para>", "<text>", "<div>"], "answer": "<p>"},
                {"question": "What is React?", "options": ["A JavaScript library for building UIs", "A CSS framework", "A backend language", "A database"], "answer": "A JavaScript library for building UIs"},
                {"question": "Which CSS property controls element visibility?", "options": ["display", "visibility", "opacity", "show"], "answer": "display"},
                {"question": "What is the DOM?", "options": ["Document Object Model", "Data Object Model", "Document Oriented Module", "None"], "answer": "Document Object Model"},
                {"question": "Which HTML tag creates an unordered list?", "options": ["<ul>", "<ol>", "<list>", "<li>"], "answer": "<ul>"},
                {"question": "What does 'responsive design' mean?", "options": ["Design that adapts to different screen sizes", "Fast loading design", "Design with animations", "None"], "answer": "Design that adapts to different screen sizes"},
                {"question": "What is Bootstrap?", "options": ["A CSS framework for responsive design", "A JavaScript engine", "A backend framework", "None"], "answer": "A CSS framework for responsive design"},
                {"question": "Which property sets element background?", "options": ["background-color", "bg-color", "back-color", "fill"], "answer": "background-color"},
                {"question": "What is useState in React?", "options": ["A hook to manage component state", "A routing tool", "A CSS module", "None"], "answer": "A hook to manage component state"},
                {"question": "Which tag makes text bold in HTML?", "options": ["<strong>", "<bold>", "<b>", "<em>"], "answer": "<strong>"},
                {"question": "What does flexbox help with?", "options": ["Laying out elements in one direction", "Animations", "Forms", "None"], "answer": "Laying out elements in one direction"},
                {"question": "What is an event listener?", "options": ["A function that runs when an event occurs", "A CSS selector", "An HTML attribute", "None"], "answer": "A function that runs when an event occurs"},
                {"question": "Which method selects an element by ID in JS?", "options": ["getElementById()", "querySelector()", "getElement()", "selectById()"], "answer": "getElementById()"},
                {"question": "What is a media query?", "options": ["CSS rule applied at specific screen sizes", "A SQL query", "A JavaScript function", "None"], "answer": "CSS rule applied at specific screen sizes"},
                {"question": "What does 'alt' attribute do in an image tag?", "options": ["Provides alternative text if image fails to load", "Sets image size", "Links the image", "None"], "answer": "Provides alternative text if image fails to load"},
                {"question": "What is Git?", "options": ["A version control system", "A framework", "A database", "None"], "answer": "A version control system"},
                {"question": "Which HTML element is used for navigation?", "options": ["<nav>", "<menu>", "<header>", "<section>"], "answer": "<nav>"},
                {"question": "What is JSX?", "options": ["JavaScript XML used in React", "A CSS extension", "A data format", "None"], "answer": "JavaScript XML used in React"},
                {"question": "What does 'margin' do in CSS?", "options": ["Creates space outside an element", "Creates space inside an element", "Sets border", "None"], "answer": "Creates space outside an element"},
                {"question": "What is a component in React?", "options": ["A reusable piece of UI", "A CSS class", "A database record", "None"], "answer": "A reusable piece of UI"},
                {"question": "What is localStorage?", "options": ["Browser storage for key-value pairs", "A server database", "A CSS module", "None"], "answer": "Browser storage for key-value pairs"},
                {"question": "What does 'let' do in JavaScript?", "options": ["Declares a block-scoped variable", "Declares a constant", "Defines a function", "None"], "answer": "Declares a block-scoped variable"},
                {"question": "What is Axios?", "options": ["A JavaScript HTTP client", "A React hook", "A CSS framework", "None"], "answer": "A JavaScript HTTP client"},
                {"question": "What is the box model in CSS?", "options": ["content, padding, border, margin", "width, height, color", "display, flex, grid", "None"], "answer": "content, padding, border, margin"},
                {"question": "What is a props in React?", "options": ["Data passed from parent to child component", "A state variable", "A lifecycle method", "None"], "answer": "Data passed from parent to child component"},
            ],
            "medium": [
                {"question": "What is the difference between == and === in JavaScript?", "options": ["=== checks type and value, == checks value only", "Both check type and value", "== checks type", "No difference"], "answer": "=== checks type and value, == checks value only"},
                {"question": "What is event bubbling?", "options": ["Event propagates from child to parent", "Event propagates from parent to child", "Event is cancelled", "None"], "answer": "Event propagates from child to parent"},
                {"question": "What is a closure in JavaScript?", "options": ["A function with access to outer function's variables", "A class method", "A loop", "None"], "answer": "A function with access to outer function's variables"},
                {"question": "What is the purpose of useEffect?", "options": ["Handle side effects after render", "Manage state", "Route pages", "None"], "answer": "Handle side effects after render"},
                {"question": "What is CSS specificity?", "options": ["Rules determining which CSS style applies when multiple match", "CSS animation speed", "CSS file size", "None"], "answer": "Rules determining which CSS style applies when multiple match"},
                {"question": "What is a promise in JavaScript?", "options": ["An object representing future async operation", "A function type", "A loop", "None"], "answer": "An object representing future async operation"},
                {"question": "What is Redux used for?", "options": ["Centralized state management", "API calls", "Routing", "Styling"], "answer": "Centralized state management"},
                {"question": "What is the virtual DOM?", "options": ["A lightweight copy of real DOM", "A server-side DOM", "A CSS construct", "None"], "answer": "A lightweight copy of real DOM"},
                {"question": "What is React Router?", "options": ["Client-side routing for React apps", "A state manager", "An HTTP client", "None"], "answer": "Client-side routing for React apps"},
                {"question": "What is destructuring in JavaScript?", "options": ["Extracting values from arrays/objects into variables", "Deleting properties", "Cloning objects", "None"], "answer": "Extracting values from arrays/objects into variables"},
                {"question": "What is the spread operator?", "options": ["Expands iterable elements", "Merges classes", "Loops arrays", "None"], "answer": "Expands iterable elements"},
                {"question": "What is the difference between padding and margin?", "options": ["Padding is inside element, margin is outside", "Margin is inside", "Both are outside", "No difference"], "answer": "Padding is inside element, margin is outside"},
                {"question": "What is async/await in JavaScript?", "options": ["Syntactic sugar over promises for async code", "A loop type", "A class method", "None"], "answer": "Syntactic sugar over promises for async code"},
                {"question": "What is CSS Grid?", "options": ["A two-dimensional layout system", "A one-dimensional layout", "An animation tool", "None"], "answer": "A two-dimensional layout system"},
                {"question": "What is a higher-order component in React?", "options": ["A function that takes a component and returns a new component", "A parent class", "A Redux reducer", "None"], "answer": "A function that takes a component and returns a new component"},
                {"question": "What is the purpose of key prop in React lists?", "options": ["Helps React identify changed/added/removed items", "Styles list items", "Routes items", "None"], "answer": "Helps React identify changed/added/removed items"},
                {"question": "What is hoisting in JavaScript?", "options": ["Variable and function declarations moved to top of scope", "Event bubbling", "Async behavior", "None"], "answer": "Variable and function declarations moved to top of scope"},
                {"question": "What is Webpack?", "options": ["A module bundler for JavaScript", "A CSS preprocessor", "A testing tool", "None"], "answer": "A module bundler for JavaScript"},
                {"question": "What is lazy loading?", "options": ["Loading resources only when needed", "Slow loading", "Caching content", "None"], "answer": "Loading resources only when needed"},
                {"question": "What is a RESTful API?", "options": ["An API following REST principles using HTTP methods", "A frontend framework", "A database", "None"], "answer": "An API following REST principles using HTTP methods"},
                {"question": "What is the use of useRef?", "options": ["Access DOM elements directly without re-render", "Manage state", "Fetch data", "None"], "answer": "Access DOM elements directly without re-render"},
                {"question": "What is SASS?", "options": ["A CSS preprocessor with variables and nesting", "A JavaScript library", "A backend language", "None"], "answer": "A CSS preprocessor with variables and nesting"},
                {"question": "What is prop drilling?", "options": ["Passing props through multiple nested components", "A Redux pattern", "A lifecycle method", "None"], "answer": "Passing props through multiple nested components"},
                {"question": "What does position: absolute do?", "options": ["Positions element relative to nearest positioned ancestor", "Fixes element to viewport", "Positions relative to itself", "None"], "answer": "Positions element relative to nearest positioned ancestor"},
                {"question": "What is a Single Page Application?", "options": ["App that loads once and updates dynamically without full reload", "A one-page website", "A mobile app", "None"], "answer": "App that loads once and updates dynamically without full reload"},
                {"question": "What is the Context API?", "options": ["React's built-in global state solution", "A routing library", "An HTTP tool", "None"], "answer": "React's built-in global state solution"},
                {"question": "What is TypeScript?", "options": ["A typed superset of JavaScript", "A CSS framework", "A backend language", "None"], "answer": "A typed superset of JavaScript"},
                {"question": "What is code splitting?", "options": ["Splitting bundle into smaller chunks loaded on demand", "Splitting CSS files", "Dividing components", "None"], "answer": "Splitting bundle into smaller chunks loaded on demand"},
                {"question": "What is semantic HTML?", "options": ["HTML tags that convey meaning about content", "HTML with CSS", "Minified HTML", "None"], "answer": "HTML tags that convey meaning about content"},
                {"question": "What is memoization in React?", "options": ["Caching component output to avoid unnecessary re-renders", "State management", "Routing", "None"], "answer": "Caching component output to avoid unnecessary re-renders"},
            ],
            "hard": [
                {"question": "What is the difference between useMemo and useCallback?", "options": ["useMemo caches a value, useCallback caches a function", "Both cache functions", "useCallback caches values", "No difference"], "answer": "useMemo caches a value, useCallback caches a function"},
                {"question": "What causes infinite loop in useEffect?", "options": ["Missing or wrong dependency array causing re-render loop", "Too many components", "Wrong JSX syntax", "None"], "answer": "Missing or wrong dependency array causing re-render loop"},
                {"question": "What is the Flux architecture?", "options": ["Unidirectional data flow pattern used by Redux", "A CSS pattern", "A routing strategy", "None"], "answer": "Unidirectional data flow pattern used by Redux"},
                {"question": "What is tree shaking?", "options": ["Removing unused code during bundling", "Sorting DOM elements", "A React pattern", "None"], "answer": "Removing unused code during bundling"},
                {"question": "What is server-side rendering in Next.js?", "options": ["HTML generated on server per request", "HTML built at compile time", "HTML rendered in browser", "None"], "answer": "HTML generated on server per request"},
                {"question": "What is the difference between controlled and uncontrolled components?", "options": ["Controlled uses React state, uncontrolled uses DOM refs", "Both use state", "Uncontrolled uses state", "None"], "answer": "Controlled uses React state, uncontrolled uses DOM refs"},
                {"question": "What is a service worker?", "options": ["A script that runs in background enabling offline/push notifications", "A backend service", "A React hook", "None"], "answer": "A script that runs in background enabling offline/push notifications"},
                {"question": "What is the Critical Rendering Path?", "options": ["Steps browser takes to render HTML/CSS/JS to pixels", "A routing algorithm", "A bundle optimization", "None"], "answer": "Steps browser takes to render HTML/CSS/JS to pixels"},
                {"question": "What is event delegation?", "options": ["Attaching one listener to parent to handle child events", "Passing events between components", "Cancelling events", "None"], "answer": "Attaching one listener to parent to handle child events"},
                {"question": "What is a Web Worker?", "options": ["Runs JavaScript in background thread", "A service worker", "A CSS worker", "None"], "answer": "Runs JavaScript in background thread"},
                {"question": "What is the difference between SSR and SSG?", "options": ["SSR renders per request, SSG renders at build time", "Both render at build time", "SSG renders per request", "None"], "answer": "SSR renders per request, SSG renders at build time"},
                {"question": "What is XSS?", "options": ["Cross-Site Scripting — injecting malicious scripts via user input", "Cross-Site Request Forgery", "XML Style Sheets", "None"], "answer": "Cross-Site Scripting — injecting malicious scripts via user input"},
                {"question": "What is the purpose of React.memo?", "options": ["Prevents re-render if props haven't changed", "Caches API calls", "Manages global state", "None"], "answer": "Prevents re-render if props haven't changed"},
                {"question": "What is hydration in React?", "options": ["Attaching React event handlers to server-rendered HTML", "Loading CSS", "Fetching initial data", "None"], "answer": "Attaching React event handlers to server-rendered HTML"},
                {"question": "What is the purpose of Babel?", "options": ["Transpiles modern JS to older browser-compatible JS", "Bundles modules", "Minifies CSS", "None"], "answer": "Transpiles modern JS to older browser-compatible JS"},
                {"question": "What is a pure function?", "options": ["A function with no side effects that always returns same output for same input", "A static method", "An async function", "None"], "answer": "A function with no side effects that always returns same output for same input"},
                {"question": "What is the Intersection Observer API?", "options": ["Detects when element enters/exits viewport", "Manages DOM events", "A React hook", "None"], "answer": "Detects when element enters/exits viewport"},
                {"question": "What is code splitting in React?", "options": ["Dynamically loading parts of app using React.lazy and Suspense", "Splitting CSS files", "Dividing components", "None"], "answer": "Dynamically loading parts of app using React.lazy and Suspense"},
                {"question": "What is a compound component pattern?", "options": ["Components that share state implicitly through context", "A HOC pattern", "A reducer pattern", "None"], "answer": "Components that share state implicitly through context"},
                {"question": "What is the difference between localStorage and sessionStorage?", "options": ["localStorage persists across tabs/sessions, sessionStorage is tab-specific", "Both are same", "sessionStorage persists", "None"], "answer": "localStorage persists across tabs/sessions, sessionStorage is tab-specific"},
                {"question": "What is Content Security Policy?", "options": ["HTTP header that prevents XSS by controlling resource loading", "A CSS rule", "An HTML attribute", "None"], "answer": "HTTP header that prevents XSS by controlling resource loading"},
                {"question": "What is the render props pattern?", "options": ["Sharing code using a prop whose value is a function", "A CSS technique", "A Redux pattern", "None"], "answer": "Sharing code using a prop whose value is a function"},
                {"question": "What is HTTP/2 vs HTTP/1.1?", "options": ["HTTP/2 supports multiplexing, header compression, and server push", "HTTP/1.1 is faster", "Both are identical", "None"], "answer": "HTTP/2 supports multiplexing, header compression, and server push"},
                {"question": "What is progressive web app?", "options": ["A web app with app-like features including offline support", "A fast website", "A mobile-only app", "None"], "answer": "A web app with app-like features including offline support"},
                {"question": "What is the purpose of shouldComponentUpdate?", "options": ["Controls whether component should re-render", "Mounts component", "Handles errors", "None"], "answer": "Controls whether component should re-render"},
                {"question": "What is the difference between createRoot and render in React 18?", "options": ["createRoot enables concurrent features, render is legacy", "Both are the same", "render enables concurrent mode", "None"], "answer": "createRoot enables concurrent features, render is legacy"},
                {"question": "What is CSS containment?", "options": ["Isolates a subtree from the rest of the page for performance", "A layout property", "A specificity rule", "None"], "answer": "Isolates a subtree from the rest of the page for performance"},
                {"question": "What is the purpose of requestAnimationFrame?", "options": ["Schedules animation callback before next repaint", "Delays function execution", "Fetches resources", "None"], "answer": "Schedules animation callback before next repaint"},
                {"question": "What is module federation in Webpack?", "options": ["Sharing code between separately deployed apps at runtime", "Code splitting", "Tree shaking", "None"], "answer": "Sharing code between separately deployed apps at runtime"},
                {"question": "What is stale closure in React?", "options": ["A closure capturing outdated state/props value", "A memory leak", "An infinite loop", "None"], "answer": "A closure capturing outdated state/props value"},
            ],
        },

        # ─────────────────────────────────────────────
        # 4. BACKEND DEVELOPER - JAVA
        # ─────────────────────────────────────────────
        "backend-developer-java": {
            "easy": [
                {"question": "What does JVM stand for?", "options": ["Java Virtual Machine", "Java Variable Method", "Java Vendor Module", "None"], "answer": "Java Virtual Machine"},
                {"question": "What is Spring Boot?", "options": ["A Java framework for rapid application development", "A database", "A frontend library", "None"], "answer": "A Java framework for rapid application development"},
                {"question": "What is a REST API?", "options": ["An API using HTTP methods to communicate", "A database connection", "A UI framework", "None"], "answer": "An API using HTTP methods to communicate"},
                {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Sequential Query Language", "Standard Query Language", "None"], "answer": "Structured Query Language"},
                {"question": "Which HTTP method creates a resource?", "options": ["POST", "GET", "DELETE", "PATCH"], "answer": "POST"},
                {"question": "What is Maven?", "options": ["A Java build and dependency management tool", "A database", "An IDE", "None"], "answer": "A Java build and dependency management tool"},
                {"question": "What is a Servlet?", "options": ["A Java class handling HTTP requests", "A database connector", "A framework", "None"], "answer": "A Java class handling HTTP requests"},
                {"question": "What is Hibernate?", "options": ["A Java ORM framework", "A database", "A build tool", "None"], "answer": "A Java ORM framework"},
                {"question": "What is the purpose of @GetMapping?", "options": ["Maps GET HTTP requests to a method", "Maps POST requests", "Configures security", "None"], "answer": "Maps GET HTTP requests to a method"},
                {"question": "What is a primary key in SQL?", "options": ["A unique identifier for a table row", "A foreign key", "An index", "None"], "answer": "A unique identifier for a table row"},
                {"question": "What does Git do?", "options": ["Version control for source code", "Manages databases", "Runs servers", "None"], "answer": "Version control for source code"},
                {"question": "What is Docker?", "options": ["A platform to run apps in containers", "A Java framework", "A database", "None"], "answer": "A platform to run apps in containers"},
                {"question": "What is JSON?", "options": ["JavaScript Object Notation — a data format", "Java Serialized Object Node", "A database", "None"], "answer": "JavaScript Object Notation — a data format"},
                {"question": "What is @Entity in Spring?", "options": ["Marks a class as a JPA database entity", "Marks a REST controller", "Defines a service", "None"], "answer": "Marks a class as a JPA database entity"},
                {"question": "What is the purpose of application.properties?", "options": ["Configure Spring Boot application settings", "Define models", "Write SQL queries", "None"], "answer": "Configure Spring Boot application settings"},
                {"question": "What is encapsulation?", "options": ["Hiding data with access modifiers", "Inheriting from a class", "Overriding methods", "None"], "answer": "Hiding data with access modifiers"},
                {"question": "What is a HashMap?", "options": ["A key-value collection in Java", "A sorted list", "A SQL table", "None"], "answer": "A key-value collection in Java"},
                {"question": "Which annotation marks a Spring service class?", "options": ["@Service", "@Controller", "@Repository", "@Bean"], "answer": "@Service"},
                {"question": "What does SELECT * FROM users do?", "options": ["Returns all rows from users table", "Deletes all users", "Updates users", "None"], "answer": "Returns all rows from users table"},
                {"question": "What is an interface in Java?", "options": ["A contract of abstract methods", "A class type", "A loop", "None"], "answer": "A contract of abstract methods"},
                {"question": "What is a foreign key?", "options": ["A field referencing primary key of another table", "A unique constraint", "An index", "None"], "answer": "A field referencing primary key of another table"},
                {"question": "What is Spring Security used for?", "options": ["Authentication and authorization", "Database access", "Frontend rendering", "None"], "answer": "Authentication and authorization"},
                {"question": "What is Postman?", "options": ["A tool to test REST APIs", "A database client", "A build tool", "None"], "answer": "A tool to test REST APIs"},
                {"question": "What does @Repository annotation do?", "options": ["Marks a DAO class for database operations", "Marks a controller", "Defines a service", "None"], "answer": "Marks a DAO class for database operations"},
                {"question": "What is method overriding?", "options": ["Redefining a parent class method in child class", "Same method different parameters", "Calling a method twice", "None"], "answer": "Redefining a parent class method in child class"},
                {"question": "What is the use of @Id in JPA?", "options": ["Marks a field as the primary key", "Marks a foreign key", "Marks an index", "None"], "answer": "Marks a field as the primary key"},
                {"question": "What is HikariCP?", "options": ["A JDBC connection pool library", "A build tool", "A security library", "None"], "answer": "A JDBC connection pool library"},
                {"question": "What is the purpose of @Autowired?", "options": ["Injects a Spring bean automatically", "Defines a REST endpoint", "Maps a URL", "None"], "answer": "Injects a Spring bean automatically"},
                {"question": "What is an ArrayList?", "options": ["A resizable array-based list in Java", "A fixed array", "A key-value map", "None"], "answer": "A resizable array-based list in Java"},
                {"question": "What is JWT used for?", "options": ["Stateless token-based authentication", "Database encryption", "Frontend routing", "None"], "answer": "Stateless token-based authentication"},
            ],
            "medium": [
                {"question": "What is the difference between @Component, @Service, and @Repository?", "options": ["They serve same purpose but indicate different layers: general, service, DAO", "They are completely different", "@Service is for REST", "None"], "answer": "They serve same purpose but indicate different layers: general, service, DAO"},
                {"question": "What is Spring IoC container?", "options": ["Manages creation and injection of Spring beans", "A security module", "A database pool", "None"], "answer": "Manages creation and injection of Spring beans"},
                {"question": "What is the difference between INNER JOIN and LEFT JOIN?", "options": ["LEFT JOIN returns all left rows, INNER JOIN returns only matches", "INNER JOIN returns all rows", "Both are same", "None"], "answer": "LEFT JOIN returns all left rows, INNER JOIN returns only matches"},
                {"question": "What is a PreparedStatement advantage over Statement?", "options": ["Prevents SQL injection and is precompiled for performance", "It is easier to write", "It supports NoSQL", "None"], "answer": "Prevents SQL injection and is precompiled for performance"},
                {"question": "What is the role of DispatcherServlet?", "options": ["Front controller routing requests to handlers in Spring MVC", "A database handler", "A security filter", "None"], "answer": "Front controller routing requests to handlers in Spring MVC"},
                {"question": "What is Spring Data JPA?", "options": ["Abstraction over JPA reducing boilerplate database code", "A database itself", "A REST tool", "None"], "answer": "Abstraction over JPA reducing boilerplate database code"},
                {"question": "What is Eager loading in Hibernate?", "options": ["Loading associated entities immediately with parent", "Loading only when accessed", "Caching entities", "None"], "answer": "Loading associated entities immediately with parent"},
                {"question": "What is @Transactional in Spring?", "options": ["Wraps method in a database transaction", "Maps a URL", "Injects beans", "None"], "answer": "Wraps method in a database transaction"},
                {"question": "What is the use of @RequestBody?", "options": ["Converts HTTP request body JSON to Java object", "Maps URL path", "Reads query params", "None"], "answer": "Converts HTTP request body JSON to Java object"},
                {"question": "What is the difference between HashMap and TreeMap?", "options": ["TreeMap sorts keys, HashMap does not", "HashMap sorts keys", "Both sort keys", "None"], "answer": "TreeMap sorts keys, HashMap does not"},
                {"question": "What is JWT token structure?", "options": ["Header.Payload.Signature", "Key.Value.Signature", "ID.Data.Hash", "None"], "answer": "Header.Payload.Signature"},
                {"question": "What is @OneToMany in JPA?", "options": ["Maps a one-to-many relationship between entities", "A SQL JOIN", "A caching annotation", "None"], "answer": "Maps a one-to-many relationship between entities"},
                {"question": "What is the use of ResponseEntity in Spring?", "options": ["Returns HTTP response with status code and body", "Maps requests", "Configures security", "None"], "answer": "Returns HTTP response with status code and body"},
                {"question": "What is a Comparator in Java?", "options": ["An interface to define custom sorting logic", "A type of loop", "A data structure", "None"], "answer": "An interface to define custom sorting logic"},
                {"question": "What is connection pooling?", "options": ["Reusing pre-established database connections", "Pooling HTTP requests", "Caching query results", "None"], "answer": "Reusing pre-established database connections"},
                {"question": "What is the purpose of global exception handling in Spring?", "options": ["Handle exceptions across all controllers consistently", "Log requests", "Manage sessions", "None"], "answer": "Handle exceptions across all controllers consistently"},
                {"question": "What is a microservice?", "options": ["A small independent deployable service", "A database table", "A frontend component", "None"], "answer": "A small independent deployable service"},
                {"question": "What is Spring Boot Actuator?", "options": ["Provides health and monitoring endpoints", "Manages security", "Handles migrations", "None"], "answer": "Provides health and monitoring endpoints"},
                {"question": "What is CORS?", "options": ["Cross-Origin Resource Sharing", "Central Object Resource System", "None", "Cross Object Routing Service"], "answer": "Cross-Origin Resource Sharing"},
                {"question": "What does @PathVariable do?", "options": ["Extracts variable from URL path segment", "Reads request body", "Maps query params", "None"], "answer": "Extracts variable from URL path segment"},
                {"question": "What is an index in SQL?", "options": ["A data structure that speeds up queries on a column", "A row number", "A foreign key", "None"], "answer": "A data structure that speeds up queries on a column"},
                {"question": "What is Feign Client?", "options": ["A declarative HTTP client for calling other services", "A database client", "A security tool", "None"], "answer": "A declarative HTTP client for calling other services"},
                {"question": "What is the purpose of HAVING clause in SQL?", "options": ["Filters grouped results", "Filters individual rows", "Orders results", "None"], "answer": "Filters grouped results"},
                {"question": "What is a checked exception in Java?", "options": ["An exception that must be declared or caught at compile time", "A runtime error", "An unchecked error", "None"], "answer": "An exception that must be declared or caught at compile time"},
                {"question": "What is HQL?", "options": ["Hibernate Query Language using entity names instead of table names", "An HTTP query language", "A SQL variant", "None"], "answer": "Hibernate Query Language using entity names instead of table names"},
                {"question": "What is the difference between @Controller and @RestController?", "options": ["@RestController adds @ResponseBody to all methods automatically", "Both are identical", "@Controller is for REST", "None"], "answer": "@RestController adds @ResponseBody to all methods automatically"},
                {"question": "What is role-based access control?", "options": ["Granting permissions based on user roles", "Encrypting data by role", "Caching by role", "None"], "answer": "Granting permissions based on user roles"},
                {"question": "What is Swagger/OpenAPI?", "options": ["A tool to document and test REST APIs", "A security framework", "A database tool", "None"], "answer": "A tool to document and test REST APIs"},
                {"question": "What is the purpose of @Column annotation in JPA?", "options": ["Customizes the database column mapping for a field", "Marks a primary key", "Maps a relationship", "None"], "answer": "Customizes the database column mapping for a field"},
                {"question": "What is a thread in Java?", "options": ["A lightweight unit of execution within a process", "A type of loop", "A collection", "None"], "answer": "A lightweight unit of execution within a process"},
            ],
            "hard": [
                {"question": "What is the N+1 problem and how do you fix it?", "options": ["Extra queries per association — fix with JOIN FETCH or @EntityGraph", "A pagination issue — fix with LIMIT", "A caching miss — fix with Redis", "None"], "answer": "Extra queries per association — fix with JOIN FETCH or @EntityGraph"},
                {"question": "What is the difference between optimistic and pessimistic locking in JPA?", "options": ["Optimistic uses versioning, pessimistic locks the row in DB", "Both lock the row", "Optimistic is slower", "None"], "answer": "Optimistic uses versioning, pessimistic locks the row in DB"},
                {"question": "What is the Saga pattern in microservices?", "options": ["Managing distributed transactions through a series of local transactions", "A service discovery pattern", "A caching strategy", "None"], "answer": "Managing distributed transactions through a series of local transactions"},
                {"question": "What is the difference between first-level and second-level cache in Hibernate?", "options": ["First-level is per session, second-level is shared across sessions", "Both are per session", "Second-level is per session", "None"], "answer": "First-level is per session, second-level is shared across sessions"},
                {"question": "What is an ExecutorService in Java?", "options": ["A thread pool for managing async tasks", "A database connection pool", "A scheduled task runner", "None"], "answer": "A thread pool for managing async tasks"},
                {"question": "What is Spring Cloud Config?", "options": ["Centralized configuration management for microservices", "A service discovery tool", "An API gateway", "None"], "answer": "Centralized configuration management for microservices"},
                {"question": "What is CQRS pattern?", "options": ["Separating command (write) and query (read) responsibilities", "A caching pattern", "A security pattern", "None"], "answer": "Separating command (write) and query (read) responsibilities"},
                {"question": "What is the difference between HashMap and ConcurrentHashMap?", "options": ["ConcurrentHashMap is thread-safe, HashMap is not", "HashMap is thread-safe", "Both are thread-safe", "None"], "answer": "ConcurrentHashMap is thread-safe, HashMap is not"},
                {"question": "What is database sharding?", "options": ["Splitting a large database horizontally across multiple servers", "Splitting a database vertically", "Creating database replicas", "None"], "answer": "Splitting a large database horizontally across multiple servers"},
                {"question": "What is a CompletableFuture in Java?", "options": ["Represents async computation that can be chained and combined", "A scheduled task", "A blocking operation", "None"], "answer": "Represents async computation that can be chained and combined"},
                {"question": "What is event sourcing?", "options": ["Storing state changes as a sequence of events", "Publishing events between services", "A caching strategy", "None"], "answer": "Storing state changes as a sequence of events"},
                {"question": "What is a circuit breaker in Resilience4j?", "options": ["Stops calls to a failing service and falls back after threshold", "A rate limiter", "A retry mechanism", "None"], "answer": "Stops calls to a failing service and falls back after threshold"},
                {"question": "What is the difference between JPA and Hibernate?", "options": ["JPA is a specification, Hibernate is an implementation of JPA", "Both are specifications", "Hibernate is the specification", "None"], "answer": "JPA is a specification, Hibernate is an implementation of JPA"},
                {"question": "What is a deadlock in Java multithreading?", "options": ["Two threads waiting on each other's locks indefinitely", "A memory overflow", "A stack overflow", "None"], "answer": "Two threads waiting on each other's locks indefinitely"},
                {"question": "What is Spring WebFlux?", "options": ["A reactive non-blocking web framework for Spring", "A traditional MVC framework", "A security module", "None"], "answer": "A reactive non-blocking web framework for Spring"},
                {"question": "What is eventual consistency?", "options": ["System will become consistent over time without requiring immediate agreement", "Immediate consistency across all nodes", "A caching strategy", "None"], "answer": "System will become consistent over time without requiring immediate agreement"},
                {"question": "What is the use of @Version in JPA?", "options": ["Enables optimistic locking by tracking entity version", "Marks entity version number for display", "Creates a versioned table", "None"], "answer": "Enables optimistic locking by tracking entity version"},
                {"question": "What is a bulkhead pattern?", "options": ["Isolating failures in one service from affecting others", "A circuit breaker", "A retry pattern", "None"], "answer": "Isolating failures in one service from affecting others"},
                {"question": "What is the CAP theorem?", "options": ["Can only guarantee 2 of: Consistency, Availability, Partition Tolerance", "A caching algorithm", "A SQL rule", "None"], "answer": "Can only guarantee 2 of: Consistency, Availability, Partition Tolerance"},
                {"question": "What is an API Gateway pattern?", "options": ["Single entry point handling routing, auth, rate limiting for microservices", "A service registry", "A config server", "None"], "answer": "Single entry point handling routing, auth, rate limiting for microservices"},
                {"question": "What is the difference between synchronous and asynchronous communication?", "options": ["Sync waits for response, async does not block and uses callbacks/events", "Async waits for response", "Both are identical", "None"], "answer": "Sync waits for response, async does not block and uses callbacks/events"},
                {"question": "What is Kafka used for?", "options": ["Distributed event streaming and message brokering", "A database", "An API gateway", "None"], "answer": "Distributed event streaming and message brokering"},
                {"question": "What is the purpose of @PreAuthorize in Spring Security?", "options": ["Evaluates authorization expression before method runs", "Authenticates user", "Logs requests", "None"], "answer": "Evaluates authorization expression before method runs"},
                {"question": "What is a read replica?", "options": ["A copy of database for handling read queries to reduce load", "A backup database", "A sharded database", "None"], "answer": "A copy of database for handling read queries to reduce load"},
                {"question": "What is idempotency and why is it important in REST?", "options": ["Same request multiple times gives same result — ensures safe retries", "Fast response time", "Request caching", "None"], "answer": "Same request multiple times gives same result — ensures safe retries"},
                {"question": "What is Spring Batch?", "options": ["A framework for processing large volumes of data in batch jobs", "A message queue", "A security module", "None"], "answer": "A framework for processing large volumes of data in batch jobs"},
                {"question": "What is a projection in Spring Data JPA?", "options": ["Selecting only specific fields from entity instead of full object", "A SQL JOIN", "A caching strategy", "None"], "answer": "Selecting only specific fields from entity instead of full object"},
                {"question": "What is the difference between @Eager and lazy fetch in JPA?", "options": ["EAGER loads immediately, LAZY loads on access", "LAZY loads immediately", "Both load immediately", "None"], "answer": "EAGER loads immediately, LAZY loads on access"},
                {"question": "What is service mesh?", "options": ["Infrastructure layer handling service-to-service communication", "A API gateway", "A database cluster", "None"], "answer": "Infrastructure layer handling service-to-service communication"},
                {"question": "What is a distributed transaction?", "options": ["A transaction spanning multiple services or databases", "A local database transaction", "A cached transaction", "None"], "answer": "A transaction spanning multiple services or databases"},
            ],
        },

        # ─────────────────────────────────────────────
        # 5. BACKEND DEVELOPER - PYTHON
        # ─────────────────────────────────────────────
        "backend-developer-python": {
            "easy": [
                {"question": "What is Python?", "options": ["A high-level programming language", "A database", "An OS", "A framework"], "answer": "A high-level programming language"},
                {"question": "What is Django?", "options": ["A Python web framework", "A database", "A JS library", "A CSS tool"], "answer": "A Python web framework"},
                {"question": "What does ORM stand for?", "options": ["Object Relational Mapper", "Open REST Module", "Object Routing Method", "None"], "answer": "Object Relational Mapper"},
                {"question": "Which file defines URL patterns in Django?", "options": ["urls.py", "views.py", "models.py", "settings.py"], "answer": "urls.py"},
                {"question": "What does pip install do?", "options": ["Installs Python packages", "Runs scripts", "Manages databases", "None"], "answer": "Installs Python packages"},
                {"question": "What is DRF?", "options": ["Django REST Framework", "Django Resource Files", "None", "Dynamic REST Format"], "answer": "Django REST Framework"},
                {"question": "What is a virtual environment?", "options": ["Isolated Python environment per project", "A cloud server", "A database", "None"], "answer": "Isolated Python environment per project"},
                {"question": "Which HTTP method deletes a resource?", "options": ["DELETE", "GET", "POST", "PATCH"], "answer": "DELETE"},
                {"question": "What is PostgreSQL?", "options": ["An open-source relational database", "A Python framework", "A frontend tool", "None"], "answer": "An open-source relational database"},
                {"question": "What does CRUD stand for?", "options": ["Create, Read, Update, Delete", "Connect, Run, Update, Deploy", "None", "Create, Retrieve, Undo, Delete"], "answer": "Create, Read, Update, Delete"},
                {"question": "What is Git?", "options": ["A version control system", "A database", "A web server", "None"], "answer": "A version control system"},
                {"question": "What is Docker?", "options": ["A containerization platform", "A Python library", "A database", "None"], "answer": "A containerization platform"},
                {"question": "What does def do in Python?", "options": ["Defines a function", "Defines a class", "Imports a module", "None"], "answer": "Defines a function"},
                {"question": "What is JSON?", "options": ["A data interchange format", "A database", "A Python module", "None"], "answer": "A data interchange format"},
                {"question": "Which command creates a Django project?", "options": ["django-admin startproject", "django start", "python new project", "None"], "answer": "django-admin startproject"},
                {"question": "What is a decorator in Python?", "options": ["A function that wraps another function", "A class attribute", "A CSS class", "None"], "answer": "A function that wraps another function"},
                {"question": "What is a list comprehension?", "options": ["A concise way to create a list using a loop", "A list method", "A tuple", "None"], "answer": "A concise way to create a list using a loop"},
                {"question": "What is an API endpoint?", "options": ["A specific URL that handles a request", "A database table", "A Python function", "None"], "answer": "A specific URL that handles a request"},
                {"question": "What does makemigrations do in Django?", "options": ["Creates migration files from model changes", "Applies migrations", "Deletes models", "None"], "answer": "Creates migration files from model changes"},
                {"question": "What is Gunicorn?", "options": ["A Python WSGI HTTP server", "A database", "A CSS framework", "None"], "answer": "A Python WSGI HTTP server"},
                {"question": "What is JWT?", "options": ["JSON Web Token for authentication", "JavaScript Web Tool", "None", "Java Web Transfer"], "answer": "JSON Web Token for authentication"},
                {"question": "Which Django file holds app settings?", "options": ["settings.py", "models.py", "views.py", "urls.py"], "answer": "settings.py"},
                {"question": "What is Nginx?", "options": ["A web server and reverse proxy", "A database", "A Python WSGI server", "None"], "answer": "A web server and reverse proxy"},
                {"question": "What is a query set in Django?", "options": ["A collection of database objects from a model", "A SQL string", "A form", "None"], "answer": "A collection of database objects from a model"},
                {"question": "What does filter() do in Django ORM?", "options": ["Returns QuerySet matching conditions", "Returns single object", "Deletes records", "None"], "answer": "Returns QuerySet matching conditions"},
                {"question": "What is a Python dictionary?", "options": ["A key-value data structure", "An ordered list", "A set", "None"], "answer": "A key-value data structure"},
                {"question": "What is the purpose of __init__.py?", "options": ["Makes a directory a Python package", "Initializes a database", "Configures settings", "None"], "answer": "Makes a directory a Python package"},
                {"question": "What is a ModelSerializer in DRF?", "options": ["Serializes model instances to JSON", "A database model", "A URL config", "None"], "answer": "Serializes model instances to JSON"},
                {"question": "What is the use of try/except in Python?", "options": ["Handle exceptions gracefully", "Loop over items", "Define classes", "None"], "answer": "Handle exceptions gracefully"},
                {"question": "What is a Dockerfile?", "options": ["Script to build a Docker image", "A Python config", "A Django settings file", "None"], "answer": "Script to build a Docker image"},
            ],
            "medium": [
                {"question": "What is the GIL in Python?", "options": ["Global Interpreter Lock allowing one thread at a time", "A garbage collector", "A module loader", "None"], "answer": "Global Interpreter Lock allowing one thread at a time"},
                {"question": "What is the difference between filter() and get() in Django?", "options": ["filter() returns QuerySet, get() returns single object or raises error", "Both return lists", "get() returns QuerySet", "None"], "answer": "filter() returns QuerySet, get() returns single object or raises error"},
                {"question": "What is select_related() used for?", "options": ["Reduces queries by doing SQL JOIN for ForeignKey relations", "Filters related objects", "Orders results", "None"], "answer": "Reduces queries by doing SQL JOIN for ForeignKey relations"},
                {"question": "What is a Python generator?", "options": ["A function that yields values lazily", "A class for generating data", "A type of list", "None"], "answer": "A function that yields values lazily"},
                {"question": "What is authentication vs authorization?", "options": ["Auth verifies who you are, authorization what you can do", "Both verify identity", "Authorization verifies identity", "None"], "answer": "Auth verifies who you are, authorization what you can do"},
                {"question": "What is CSRF protection in Django?", "options": ["Prevents cross-site request forgery with tokens", "Encrypts passwords", "Manages sessions", "None"], "answer": "Prevents cross-site request forgery with tokens"},
                {"question": "What is a ViewSet in DRF?", "options": ["Combines CRUD operations for a model into one class", "A URL config", "A serializer", "None"], "answer": "Combines CRUD operations for a model into one class"},
                {"question": "What is a Python context manager?", "options": ["Manages resource setup/teardown with 'with' statement", "A thread manager", "A memory tool", "None"], "answer": "Manages resource setup/teardown with 'with' statement"},
                {"question": "What is signals in Django?", "options": ["Hooks firing on model events like save/delete", "HTTP signals", "Error events", "None"], "answer": "Hooks firing on model events like save/delete"},
                {"question": "What is the purpose of @staticmethod?", "options": ["Defines a method that doesn't need self or cls", "A class factory method", "A property", "None"], "answer": "Defines a method that doesn't need self or cls"},
                {"question": "What is Celery?", "options": ["A distributed task queue for Python", "A database", "A web framework", "None"], "answer": "A distributed task queue for Python"},
                {"question": "What is prefetch_related() vs select_related()?", "options": ["prefetch_related handles M2M/reverse FK with separate queries, select_related uses JOINs", "Both use JOINs", "select_related uses separate queries", "None"], "answer": "prefetch_related handles M2M/reverse FK with separate queries, select_related uses JOINs"},
                {"question": "What is a custom manager in Django?", "options": ["A class extending objects to add custom QuerySet methods", "A migration tool", "A form handler", "None"], "answer": "A class extending objects to add custom QuerySet methods"},
                {"question": "What is rate limiting?", "options": ["Restricting number of API requests per time window", "Caching responses", "Compressing data", "None"], "answer": "Restricting number of API requests per time window"},
                {"question": "What is a migration in Django?", "options": ["File tracking schema changes to apply to database", "A URL redirect", "A template", "None"], "answer": "File tracking schema changes to apply to database"},
                {"question": "What is docker-compose used for?", "options": ["Running multi-container applications", "Building images only", "Writing Dockerfiles", "None"], "answer": "Running multi-container applications"},
                {"question": "What is WSGI?", "options": ["Web Server Gateway Interface — standard for Python web servers", "A Django utility", "A database adapter", "None"], "answer": "Web Server Gateway Interface — standard for Python web servers"},
                {"question": "What is __str__ used for in Django models?", "options": ["Returns human-readable string for the model object", "Converts to integer", "Compares objects", "None"], "answer": "Returns human-readable string for the model object"},
                {"question": "What is pagination in DRF?", "options": ["Splitting large querysets into pages", "Filtering data", "Sorting data", "None"], "answer": "Splitting large querysets into pages"},
                {"question": "What is a lambda function?", "options": ["An anonymous single-expression function", "A class method", "A recursive function", "None"], "answer": "An anonymous single-expression function"},
                {"question": "What is the purpose of reverse() in Django?", "options": ["Returns URL from named URL pattern", "Reverses a list", "Redirects to home", "None"], "answer": "Returns URL from named URL pattern"},
                {"question": "What is a foreign key in Django models?", "options": ["A ForeignKey field linking to another model", "A unique constraint", "An index", "None"], "answer": "A ForeignKey field linking to another model"},
                {"question": "What is the use of annotate() in Django ORM?", "options": ["Adds computed values to each queryset object", "Filters results", "Orders results", "None"], "answer": "Adds computed values to each queryset object"},
                {"question": "What is Swagger?", "options": ["A tool to document and test REST APIs", "A security framework", "A database tool", "None"], "answer": "A tool to document and test REST APIs"},
                {"question": "What is the difference between list and tuple in Python?", "options": ["List is mutable, tuple is immutable", "Tuple is mutable", "Both are mutable", "None"], "answer": "List is mutable, tuple is immutable"},
                {"question": "What is an environment variable?", "options": ["Configuration stored outside source code", "A Python variable", "A database column", "None"], "answer": "Configuration stored outside source code"},
                {"question": "What is the purpose of @property in Python?", "options": ["Defines a method accessible as an attribute", "Defines a static method", "Defines a class method", "None"], "answer": "Defines a method accessible as an attribute"},
                {"question": "What is a webhook?", "options": ["HTTP callback triggered when an event occurs", "A web scraper", "A REST endpoint", "None"], "answer": "HTTP callback triggered when an event occurs"},
                {"question": "What is connection pooling?", "options": ["Reusing existing DB connections to improve performance", "Creating multiple databases", "Caching queries", "None"], "answer": "Reusing existing DB connections to improve performance"},
                {"question": "What is GitHub Actions?", "options": ["A CI/CD tool for automating workflows", "A code editor", "A project manager", "None"], "answer": "A CI/CD tool for automating workflows"},
            ],
            "hard": [
                {"question": "What is the N+1 query problem in Django ORM?", "options": ["Firing one query per related object instead of a single JOIN", "A pagination bug", "A cache miss", "None"], "answer": "Firing one query per related object instead of a single JOIN"},
                {"question": "What is a Python metaclass?", "options": ["A class that defines the behavior of other classes", "A base class", "A decorator", "None"], "answer": "A class that defines the behavior of other classes"},
                {"question": "What is the difference between ACID and BASE?", "options": ["ACID is strict consistency for relational DBs, BASE is eventual consistency for NoSQL", "ACID is for NoSQL", "Both are same", "None"], "answer": "ACID is strict consistency for relational DBs, BASE is eventual consistency for NoSQL"},
                {"question": "What is asyncio in Python?", "options": ["Library for writing single-threaded concurrent code using coroutines", "A multithreading tool", "A database driver", "None"], "answer": "Library for writing single-threaded concurrent code using coroutines"},
                {"question": "What is a race condition?", "options": ["Two threads accessing shared data simultaneously causing unpredictable results", "A performance benchmark", "A deadlock", "None"], "answer": "Two threads accessing shared data simultaneously causing unpredictable results"},
                {"question": "What is event sourcing?", "options": ["Storing state changes as a sequence of immutable events", "Publishing events", "A caching strategy", "None"], "answer": "Storing state changes as a sequence of immutable events"},
                {"question": "What is Redis used for in a Python backend?", "options": ["Caching, session storage, and message brokering", "A relational database", "A frontend tool", "None"], "answer": "Caching, session storage, and message brokering"},
                {"question": "What is the difference between horizontal and vertical scaling?", "options": ["Horizontal adds servers, vertical upgrades existing server resources", "Vertical adds servers", "Both add servers", "None"], "answer": "Horizontal adds servers, vertical upgrades existing server resources"},
                {"question": "What is CQRS?", "options": ["Command Query Responsibility Segregation — separating read and write models", "A caching pattern", "A security pattern", "None"], "answer": "Command Query Responsibility Segregation — separating read and write models"},
                {"question": "What is OAuth2?", "options": ["An authorization framework for delegated access", "An authentication protocol", "An encryption standard", "None"], "answer": "An authorization framework for delegated access"},
                {"question": "What is database sharding?", "options": ["Splitting database horizontally across multiple servers by key", "Replicating databases", "Indexing tables", "None"], "answer": "Splitting database horizontally across multiple servers by key"},
                {"question": "What is a deadlock?", "options": ["Two processes blocking each other waiting for resources indefinitely", "A memory leak", "An infinite loop", "None"], "answer": "Two processes blocking each other waiting for resources indefinitely"},
                {"question": "What is eventual consistency?", "options": ["System becomes consistent over time without immediate agreement", "Immediate consistency", "A caching strategy", "None"], "answer": "System becomes consistent over time without immediate agreement"},
                {"question": "What is the purpose of database indexing?", "options": ["Speeds up query lookups at cost of write performance", "Speeds up writes", "Compresses data", "None"], "answer": "Speeds up query lookups at cost of write performance"},
                {"question": "What is a message queue?", "options": ["An async communication buffer between services", "A database", "A cache", "None"], "answer": "An async communication buffer between services"},
                {"question": "What is the Strangler Fig pattern?", "options": ["Gradually replacing a monolith by building new features as microservices", "A deployment strategy", "A caching pattern", "None"], "answer": "Gradually replacing a monolith by building new features as microservices"},
                {"question": "What is content negotiation in REST?", "options": ["Client and server agreeing on response format via Accept headers", "Rate limiting", "URL versioning", "None"], "answer": "Client and server agreeing on response format via Accept headers"},
                {"question": "What is a distributed lock?", "options": ["A lock shared across multiple servers to prevent concurrent access", "A thread lock", "A database constraint", "None"], "answer": "A lock shared across multiple servers to prevent concurrent access"},
                {"question": "What is the Circuit Breaker pattern?", "options": ["Stops requests to a failing service and allows recovery time", "A retry pattern", "A rate limiter", "None"], "answer": "Stops requests to a failing service and allows recovery time"},
                {"question": "What is gRPC?", "options": ["A high-performance RPC framework using Protocol Buffers", "A REST variant", "A GraphQL tool", "None"], "answer": "A high-performance RPC framework using Protocol Buffers"},
                {"question": "What is lazy evaluation in Python?", "options": ["Delaying computation until result is actually needed", "A slow algorithm", "A caching strategy", "None"], "answer": "Delaying computation until result is actually needed"},
                {"question": "What is a read replica in databases?", "options": ["A copy of primary DB serving read-only queries to reduce load", "A backup DB", "A sharded DB", "None"], "answer": "A copy of primary DB serving read-only queries to reduce load"},
                {"question": "What is CAP theorem?", "options": ["Cannot guarantee all 3 of Consistency, Availability, Partition Tolerance", "A caching algorithm", "A SQL rule", "None"], "answer": "Cannot guarantee all 3 of Consistency, Availability, Partition Tolerance"},
                {"question": "What is memoization?", "options": ["Caching function results to avoid redundant computation", "A sorting technique", "A memory type", "None"], "answer": "Caching function results to avoid redundant computation"},
                {"question": "What is a service mesh?", "options": ["Infrastructure layer managing service-to-service communication", "An API gateway", "A database cluster", "None"], "answer": "Infrastructure layer managing service-to-service communication"},
                {"question": "What is idempotency in REST APIs?", "options": ["Same request multiple times produces same result", "Fast response time", "Request caching", "None"], "answer": "Same request multiple times produces same result"},
                {"question": "What is the Outbox pattern?", "options": ["Publishing events reliably by writing to a DB outbox table first", "A message queue", "A cache strategy", "None"], "answer": "Publishing events reliably by writing to a DB outbox table first"},
                {"question": "What is blue-green deployment?", "options": ["Two identical environments switching traffic for zero-downtime deploys", "A canary release", "A rollback strategy", "None"], "answer": "Two identical environments switching traffic for zero-downtime deploys"},
                {"question": "What is a JWT refresh token?", "options": ["A long-lived token used to obtain new short-lived access tokens", "A permanent access token", "An API key", "None"], "answer": "A long-lived token used to obtain new short-lived access tokens"},
                {"question": "What is GraphQL?", "options": ["A query language for APIs allowing clients to request exact data needed", "A REST variant", "A database query language", "None"], "answer": "A query language for APIs allowing clients to request exact data needed"},
            ],
        },

        # ─────────────────────────────────────────────
        # 6. DATA ANALYTICS
        # ─────────────────────────────────────────────
        "data-analytics": {
            "easy": [
                {"question": "What is data analytics?", "options": ["Analyzing data to extract insights", "Building mobile apps", "Designing websites", "None"], "answer": "Analyzing data to extract insights"},
                {"question": "What does CSV stand for?", "options": ["Comma Separated Values", "Comma Sorted Values", "Compressed Standard Values", "None"], "answer": "Comma Separated Values"},
                {"question": "What is Pandas?", "options": ["A Python data manipulation library", "A database", "A web framework", "None"], "answer": "A Python data manipulation library"},
                {"question": "Which Pandas method reads a CSV file?", "options": ["read_csv()", "load_csv()", "open_csv()", "get_csv()"], "answer": "read_csv()"},
                {"question": "What is a DataFrame in Pandas?", "options": ["A 2D tabular data structure", "A list", "A dictionary", "None"], "answer": "A 2D tabular data structure"},
                {"question": "What does SQL SELECT do?", "options": ["Retrieves data from a database", "Deletes data", "Updates data", "Inserts data"], "answer": "Retrieves data from a database"},
                {"question": "What is Power BI?", "options": ["A Microsoft data visualization tool", "A Python library", "A database", "None"], "answer": "A Microsoft data visualization tool"},
                {"question": "What is a pivot table?", "options": ["A table summarizing data with grouping", "A SQL table", "A chart type", "None"], "answer": "A table summarizing data with grouping"},
                {"question": "What is the mean?", "options": ["Average of a dataset", "Middle value", "Most frequent value", "None"], "answer": "Average of a dataset"},
                {"question": "What is a bar chart used for?", "options": ["Comparing categories", "Showing trends over time", "Showing proportions", "None"], "answer": "Comparing categories"},
                {"question": "What does dropna() do in Pandas?", "options": ["Removes rows with missing values", "Fills missing values", "Renames columns", "None"], "answer": "Removes rows with missing values"},
                {"question": "What is Excel VLOOKUP used for?", "options": ["Looking up a value in a table", "Creating charts", "Filtering data", "None"], "answer": "Looking up a value in a table"},
                {"question": "What is a line chart best for?", "options": ["Showing trends over time", "Comparing categories", "Showing parts of whole", "None"], "answer": "Showing trends over time"},
                {"question": "What is NumPy?", "options": ["A Python library for numerical computing", "A database", "A web framework", "None"], "answer": "A Python library for numerical computing"},
                {"question": "What does GROUP BY do in SQL?", "options": ["Groups rows by a column for aggregation", "Filters rows", "Orders results", "None"], "answer": "Groups rows by a column for aggregation"},
                {"question": "What is Tableau used for?", "options": ["Data visualization and dashboards", "Database management", "Python scripting", "None"], "answer": "Data visualization and dashboards"},
                {"question": "What is a null value?", "options": ["A missing or unknown value", "Zero", "An empty string", "None"], "answer": "A missing or unknown value"},
                {"question": "What is the median?", "options": ["The middle value when data is sorted", "The average", "The most frequent value", "None"], "answer": "The middle value when data is sorted"},
                {"question": "What does fillna() do?", "options": ["Fills missing values with a specified value", "Removes nulls", "Renames columns", "None"], "answer": "Fills missing values with a specified value"},
                {"question": "What is a pie chart best for?", "options": ["Showing proportions of a whole", "Trends over time", "Comparing many categories", "None"], "answer": "Showing proportions of a whole"},
                {"question": "What is data cleaning?", "options": ["Fixing errors and inconsistencies in data", "Visualizing data", "Storing data", "None"], "answer": "Fixing errors and inconsistencies in data"},
                {"question": "What is a scatter plot used for?", "options": ["Showing relationship between two variables", "Comparing categories", "Showing parts of whole", "None"], "answer": "Showing relationship between two variables"},
                {"question": "What does COUNT() do in SQL?", "options": ["Counts number of rows", "Sums values", "Averages values", "None"], "answer": "Counts number of rows"},
                {"question": "What is a histogram?", "options": ["A chart showing distribution of numeric data", "A bar chart", "A line chart", "None"], "answer": "A chart showing distribution of numeric data"},
                {"question": "What is DAX in Power BI?", "options": ["Data Analysis Expressions — a formula language", "A data format", "A chart type", "None"], "answer": "Data Analysis Expressions — a formula language"},
                {"question": "What is the mode?", "options": ["The most frequently occurring value", "The average", "The middle value", "None"], "answer": "The most frequently occurring value"},
                {"question": "What does ORDER BY do in SQL?", "options": ["Sorts results by a column", "Groups results", "Filters results", "None"], "answer": "Sorts results by a column"},
                {"question": "What is Matplotlib?", "options": ["A Python plotting library", "A database", "A web framework", "None"], "answer": "A Python plotting library"},
                {"question": "What is data aggregation?", "options": ["Combining data to compute summary statistics", "Splitting data", "Filtering data", "None"], "answer": "Combining data to compute summary statistics"},
                {"question": "What does describe() do in Pandas?", "options": ["Returns summary statistics of a DataFrame", "Describes column types", "Prints first rows", "None"], "answer": "Returns summary statistics of a DataFrame"},
            ],
            "medium": [
                {"question": "What is the difference between merge() and concat() in Pandas?", "options": ["merge() joins on keys like SQL JOIN, concat() stacks DataFrames", "Both join on keys", "concat() uses SQL JOIN", "None"], "answer": "merge() joins on keys like SQL JOIN, concat() stacks DataFrames"},
                {"question": "What is a window function in SQL?", "options": ["Applies calculation over a partition of rows without collapsing them", "A GROUP BY alternative", "A subquery type", "None"], "answer": "Applies calculation over a partition of rows without collapsing them"},
                {"question": "What is the difference between loc and iloc in Pandas?", "options": ["loc uses labels, iloc uses integer positions", "Both use integers", "iloc uses labels", "None"], "answer": "loc uses labels, iloc uses integer positions"},
                {"question": "What is a CTE in SQL?", "options": ["Common Table Expression — a named temporary result set", "A type of JOIN", "A window function", "None"], "answer": "Common Table Expression — a named temporary result set"},
                {"question": "What is Seaborn?", "options": ["A Python statistical visualization library", "A database tool", "A data cleaning library", "None"], "answer": "A Python statistical visualization library"},
                {"question": "What is the difference between INNER JOIN and LEFT JOIN?", "options": ["LEFT JOIN includes all left rows, INNER JOIN only matches", "INNER JOIN includes all rows", "Both are identical", "None"], "answer": "LEFT JOIN includes all left rows, INNER JOIN only matches"},
                {"question": "What is groupby() in Pandas?", "options": ["Groups data and applies aggregate functions", "Filters rows", "Renames columns", "None"], "answer": "Groups data and applies aggregate functions"},
                {"question": "What is a heatmap?", "options": ["A chart showing matrix data with color intensity", "A scatter plot", "A line chart", "None"], "answer": "A chart showing matrix data with color intensity"},
                {"question": "What is data normalization?", "options": ["Scaling data to a common range like 0-1", "Removing duplicates", "Filling nulls", "None"], "answer": "Scaling data to a common range like 0-1"},
                {"question": "What is the HAVING clause used for?", "options": ["Filtering after GROUP BY aggregation", "Filtering individual rows", "Ordering results", "None"], "answer": "Filtering after GROUP BY aggregation"},
                {"question": "What is Plotly?", "options": ["A Python library for interactive charts", "A static chart library", "A database tool", "None"], "answer": "A Python library for interactive charts"},
                {"question": "What is correlation?", "options": ["A measure of linear relationship between two variables", "A measure of variance", "A type of regression", "None"], "answer": "A measure of linear relationship between two variables"},
                {"question": "What is apply() in Pandas?", "options": ["Applies a function along axis of DataFrame", "Filters rows", "Groups data", "None"], "answer": "Applies a function along axis of DataFrame"},
                {"question": "What is a RANK() window function?", "options": ["Assigns rank to rows with gaps for ties", "Assigns row numbers without gaps", "Counts rows", "None"], "answer": "Assigns rank to rows with gaps for ties"},
                {"question": "What does astype() do in Pandas?", "options": ["Converts column to a different data type", "Renames column", "Filters column", "None"], "answer": "Converts column to a different data type"},
                {"question": "What is a KPI?", "options": ["Key Performance Indicator", "Key Process Integration", "None", "Key Product Index"], "answer": "Key Performance Indicator"},
                {"question": "What is the standard deviation?", "options": ["Measure of how spread out data is from the mean", "The average", "The middle value", "None"], "answer": "Measure of how spread out data is from the mean"},
                {"question": "What is the purpose of SUMIF in Excel?", "options": ["Sums values that meet a condition", "Sums all values", "Counts values", "None"], "answer": "Sums values that meet a condition"},
                {"question": "What is a box plot?", "options": ["Shows distribution with quartiles and outliers", "A bar chart", "A scatter plot", "None"], "answer": "Shows distribution with quartiles and outliers"},
                {"question": "What is data wrangling?", "options": ["Transforming raw data into a usable format", "Visualizing data", "Storing data", "None"], "answer": "Transforming raw data into a usable format"},
                {"question": "What is a subquery in SQL?", "options": ["A query nested inside another query", "A type of JOIN", "A window function", "None"], "answer": "A query nested inside another query"},
                {"question": "What is outlier detection?", "options": ["Identifying data points that deviate significantly from others", "Filling missing values", "Sorting data", "None"], "answer": "Identifying data points that deviate significantly from others"},
                {"question": "What is the difference between mean and median?", "options": ["Mean is average, median is middle value — median is robust to outliers", "Both are averages", "Median is the average", "None"], "answer": "Mean is average, median is middle value — median is robust to outliers"},
                {"question": "What is a data warehouse?", "options": ["A centralized repository for structured analytical data", "A transaction database", "A file server", "None"], "answer": "A centralized repository for structured analytical data"},
                {"question": "What is conditional formatting in Excel?", "options": ["Automatically formatting cells based on their values", "A formula type", "A chart feature", "None"], "answer": "Automatically formatting cells based on their values"},
                {"question": "What is data granularity?", "options": ["The level of detail in a dataset", "The size of the dataset", "The number of columns", "None"], "answer": "The level of detail in a dataset"},
                {"question": "What is a calculated field in Power BI?", "options": ["A custom column or measure created with DAX", "A filter", "A chart type", "None"], "answer": "A custom column or measure created with DAX"},
                {"question": "What is an ETL pipeline?", "options": ["Extract, Transform, Load — moving data from source to destination", "A Python library", "A visualization tool", "None"], "answer": "Extract, Transform, Load — moving data from source to destination"},
                {"question": "What is the IQR?", "options": ["Interquartile Range — the range between Q1 and Q3", "Interquartile Ratio", "None", "Index Query Range"], "answer": "Interquartile Range — the range between Q1 and Q3"},
                {"question": "What is pivot_table() in Pandas?", "options": ["Creates a pivot summary table from a DataFrame", "Sorts data", "Filters data", "None"], "answer": "Creates a pivot summary table from a DataFrame"},
            ],
            "hard": [
                {"question": "What is the difference between a data lake and a data warehouse?", "options": ["Data lake stores raw unstructured data, warehouse stores structured analytics data", "Both store structured data", "Warehouse stores raw data", "None"], "answer": "Data lake stores raw unstructured data, warehouse stores structured analytics data"},
                {"question": "What is Simpson's Paradox?", "options": ["A trend in groups reverses when groups are combined", "A visualization error", "A SQL error", "None"], "answer": "A trend in groups reverses when groups are combined"},
                {"question": "What is the difference between correlation and causation?", "options": ["Correlation shows relationship, causation shows one causes the other", "Both mean one causes the other", "Causation shows relationship", "None"], "answer": "Correlation shows relationship, causation shows one causes the other"},
                {"question": "What is a slowly changing dimension?", "options": ["A dimension that changes over time in a data warehouse", "A static table", "A fact table", "None"], "answer": "A dimension that changes over time in a data warehouse"},
                {"question": "What is variance in statistics?", "options": ["The average squared deviation from the mean", "The average deviation", "The range", "None"], "answer": "The average squared deviation from the mean"},
                {"question": "What is a fact table in a star schema?", "options": ["The central table with measurable metrics", "A dimension table", "A lookup table", "None"], "answer": "The central table with measurable metrics"},
                {"question": "What is the difference between RANK() and DENSE_RANK()?", "options": ["RANK() skips numbers for ties, DENSE_RANK() does not", "DENSE_RANK() skips numbers", "Both are identical", "None"], "answer": "RANK() skips numbers for ties, DENSE_RANK() does not"},
                {"question": "What is a cohort analysis?", "options": ["Analyzing behavior of groups sharing a common characteristic over time", "A KPI dashboard", "A SQL technique", "None"], "answer": "Analyzing behavior of groups sharing a common characteristic over time"},
                {"question": "What is data profiling?", "options": ["Examining data quality, structure, and content", "Visualizing data", "Filtering data", "None"], "answer": "Examining data quality, structure, and content"},
                {"question": "What is funnel analysis?", "options": ["Analyzing drop-off at each stage of a user journey", "A KPI calculation", "A SQL window function", "None"], "answer": "Analyzing drop-off at each stage of a user journey"},
                {"question": "What is A/B testing?", "options": ["Comparing two variants to see which performs better statistically", "A data cleaning method", "A visualization technique", "None"], "answer": "Comparing two variants to see which performs better statistically"},
                {"question": "What is Pareto analysis?", "options": ["Finding the 20% of causes responsible for 80% of effects", "A regression method", "A SQL technique", "None"], "answer": "Finding the 20% of causes responsible for 80% of effects"},
                {"question": "What is the p-value in hypothesis testing?", "options": ["Probability of observing results as extreme as data if null hypothesis is true", "The test statistic", "The confidence level", "None"], "answer": "Probability of observing results as extreme as data if null hypothesis is true"},
                {"question": "What is a confidence interval?", "options": ["A range of values likely to contain the true parameter", "A p-value range", "A significance level", "None"], "answer": "A range of values likely to contain the true parameter"},
                {"question": "What is time series decomposition?", "options": ["Splitting time series into trend, seasonality, and residual", "Forecasting future values", "Smoothing data", "None"], "answer": "Splitting time series into trend, seasonality, and residual"},
                {"question": "What is skewness?", "options": ["Asymmetry of data distribution around the mean", "The spread of data", "The average", "None"], "answer": "Asymmetry of data distribution around the mean"},
                {"question": "What is Pearson correlation coefficient?", "options": ["Measures strength and direction of linear relationship between two variables", "Measures variance", "Measures distribution shape", "None"], "answer": "Measures strength and direction of linear relationship between two variables"},
                {"question": "What is a star schema?", "options": ["A data warehouse schema with one fact table and multiple dimension tables", "A relational schema", "A NoSQL schema", "None"], "answer": "A data warehouse schema with one fact table and multiple dimension tables"},
                {"question": "What is data lineage?", "options": ["Tracking data origins, movements, and transformations", "A data format", "An ETL technique", "None"], "answer": "Tracking data origins, movements, and transformations"},
                {"question": "What is OLAP?", "options": ["Online Analytical Processing for complex queries on multidimensional data", "Online Transaction Processing", "A database type", "None"], "answer": "Online Analytical Processing for complex queries on multidimensional data"},
                {"question": "What is Benford's Law?", "options": ["In many real-world datasets, leading digits follow a predictable distribution", "A statistical test", "A SQL rule", "None"], "answer": "In many real-world datasets, leading digits follow a predictable distribution"},
                {"question": "What is multicollinearity?", "options": ["When predictor variables are highly correlated with each other", "When target variable correlates with predictors", "A data cleaning issue", "None"], "answer": "When predictor variables are highly correlated with each other"},
                {"question": "What is a control chart?", "options": ["A statistical tool to monitor process variation over time", "A bar chart", "A KPI dashboard", "None"], "answer": "A statistical tool to monitor process variation over time"},
                {"question": "What is the Central Limit Theorem?", "options": ["Sample means approach normal distribution as sample size increases", "Population is always normal", "A regression theorem", "None"], "answer": "Sample means approach normal distribution as sample size increases"},
                {"question": "What is interpolation?", "options": ["Estimating values between known data points", "Forecasting future values", "Filling nulls with mean", "None"], "answer": "Estimating values between known data points"},
                {"question": "What is data modeling?", "options": ["Designing the structure of a database or data warehouse", "Building ML models", "Visualizing data", "None"], "answer": "Designing the structure of a database or data warehouse"},
                {"question": "What is the Shapiro-Wilk test?", "options": ["Tests if data follows a normal distribution", "Tests correlation", "Tests variance equality", "None"], "answer": "Tests if data follows a normal distribution"},
                {"question": "What is seasonality in time series?", "options": ["Repeating patterns at regular intervals", "Random noise", "A long-term trend", "None"], "answer": "Repeating patterns at regular intervals"},
                {"question": "What is the difference between descriptive and inferential statistics?", "options": ["Descriptive summarizes data, inferential draws conclusions about population from sample", "Both draw conclusions", "Inferential summarizes data", "None"], "answer": "Descriptive summarizes data, inferential draws conclusions about population from sample"},
                {"question": "What is data governance?", "options": ["Policies and standards for managing data quality, security, and access", "A database tool", "An ETL process", "None"], "answer": "Policies and standards for managing data quality, security, and access"},
            ],
        },

        # ─────────────────────────────────────────────
        # 7. DATA SCIENCE
        # ─────────────────────────────────────────────
        "data-science": {
            "easy": [
                {"question": "What is data science?", "options": ["Extracting insights from data using statistics and ML", "Building websites", "Managing databases only", "None"], "answer": "Extracting insights from data using statistics and ML"},
                {"question": "What is machine learning?", "options": ["Teaching machines to learn from data", "Programming logic manually", "A database technique", "None"], "answer": "Teaching machines to learn from data"},
                {"question": "What is Python?", "options": ["A high-level programming language", "A database", "An OS", "None"], "answer": "A high-level programming language"},
                {"question": "What does EDA stand for?", "options": ["Exploratory Data Analysis", "Experimental Data Analytics", "Extract Data Analysis", "None"], "answer": "Exploratory Data Analysis"},
                {"question": "What is a feature in machine learning?", "options": ["An input variable used to make predictions", "The output label", "A model parameter", "None"], "answer": "An input variable used to make predictions"},
                {"question": "What is a label in supervised learning?", "options": ["The target output variable", "An input feature", "A model weight", "None"], "answer": "The target output variable"},
                {"question": "What is Scikit-learn?", "options": ["A Python ML library", "A deep learning framework", "A database", "None"], "answer": "A Python ML library"},
                {"question": "What is overfitting?", "options": ["Model performs well on training data but poorly on new data", "Model performs well on all data", "Model underfits data", "None"], "answer": "Model performs well on training data but poorly on new data"},
                {"question": "What is a training set?", "options": ["Data used to train the model", "Data used to evaluate the model", "Raw unprocessed data", "None"], "answer": "Data used to train the model"},
                {"question": "What is a test set?", "options": ["Data used to evaluate final model performance", "Data used during training", "Cleaned data", "None"], "answer": "Data used to evaluate final model performance"},
                {"question": "What is linear regression?", "options": ["Predicting a continuous output using a linear relationship", "A classification algorithm", "A clustering method", "None"], "answer": "Predicting a continuous output using a linear relationship"},
                {"question": "What is classification in ML?", "options": ["Predicting a category/class label", "Predicting a numeric value", "Grouping data", "None"], "answer": "Predicting a category/class label"},
                {"question": "What is clustering?", "options": ["Grouping data points based on similarity", "Classifying data", "Predicting values", "None"], "answer": "Grouping data points based on similarity"},
                {"question": "What does Pandas read_csv() do?", "options": ["Reads a CSV file into a DataFrame", "Writes CSV files", "Queries SQL", "None"], "answer": "Reads a CSV file into a DataFrame"},
                {"question": "What is accuracy in classification?", "options": ["Percentage of correct predictions", "Sum of true positives", "Recall measure", "None"], "answer": "Percentage of correct predictions"},
                {"question": "What is a confusion matrix?", "options": ["A table showing predicted vs actual classifications", "A correlation matrix", "A feature importance table", "None"], "answer": "A table showing predicted vs actual classifications"},
                {"question": "What is normalization?", "options": ["Scaling features to a common range", "Removing duplicates", "Filling missing values", "None"], "answer": "Scaling features to a common range"},
                {"question": "What is a Jupyter Notebook?", "options": ["An interactive coding environment", "A Python library", "A database tool", "None"], "answer": "An interactive coding environment"},
                {"question": "What is NumPy?", "options": ["A Python numerical computing library", "A web framework", "A database", "None"], "answer": "A Python numerical computing library"},
                {"question": "What is underfitting?", "options": ["Model is too simple and fails to capture patterns", "Model memorizes training data", "Model performs well", "None"], "answer": "Model is too simple and fails to capture patterns"},
                {"question": "What is a decision tree?", "options": ["A model making decisions using branching conditions", "A neural network", "A regression model", "None"], "answer": "A model making decisions using branching conditions"},
                {"question": "What is K-Means used for?", "options": ["Clustering unlabeled data", "Classification", "Regression", "None"], "answer": "Clustering unlabeled data"},
                {"question": "What is cross-validation?", "options": ["Evaluating model by training/testing on multiple data splits", "A single train/test split", "A data cleaning technique", "None"], "answer": "Evaluating model by training/testing on multiple data splits"},
                {"question": "What is a correlation matrix?", "options": ["A table showing pairwise correlations between features", "A confusion matrix", "A feature table", "None"], "answer": "A table showing pairwise correlations between features"},
                {"question": "What is feature scaling?", "options": ["Transforming features to similar ranges", "Selecting important features", "Creating new features", "None"], "answer": "Transforming features to similar ranges"},
                {"question": "What is the mean squared error?", "options": ["Average of squared differences between predictions and actual values", "Average absolute difference", "Root average error", "None"], "answer": "Average of squared differences between predictions and actual values"},
                {"question": "What is a random forest?", "options": ["An ensemble of decision trees", "A single decision tree", "A clustering algorithm", "None"], "answer": "An ensemble of decision trees"},
                {"question": "What is precision in ML?", "options": ["True positives / (True positives + False positives)", "True positives / All positives", "Correct predictions / Total", "None"], "answer": "True positives / (True positives + False positives)"},
                {"question": "What is recall in ML?", "options": ["True positives / (True positives + False negatives)", "True positives / All predictions", "Accuracy measure", "None"], "answer": "True positives / (True positives + False negatives)"},
                {"question": "What is PCA?", "options": ["Principal Component Analysis — reduces dimensions", "A clustering algorithm", "A regression method", "None"], "answer": "Principal Component Analysis — reduces dimensions"},
            ],
            "medium": [
                {"question": "What is the bias-variance tradeoff?", "options": ["High bias = underfitting, high variance = overfitting — balance needed", "High bias is always better", "High variance is always better", "None"], "answer": "High bias = underfitting, high variance = overfitting — balance needed"},
                {"question": "What is the difference between bagging and boosting?", "options": ["Bagging builds models in parallel, boosting builds sequentially correcting errors", "Both build models in parallel", "Boosting builds models in parallel", "None"], "answer": "Bagging builds models in parallel, boosting builds sequentially correcting errors"},
                {"question": "What is feature engineering?", "options": ["Creating new useful features from existing data", "Selecting features", "Scaling features", "None"], "answer": "Creating new useful features from existing data"},
                {"question": "What is the F1 score?", "options": ["Harmonic mean of precision and recall", "Average of precision and recall", "Same as accuracy", "None"], "answer": "Harmonic mean of precision and recall"},
                {"question": "What is GridSearchCV?", "options": ["Exhaustive search over hyperparameter grid with cross-validation", "A single hyperparameter test", "A feature selector", "None"], "answer": "Exhaustive search over hyperparameter grid with cross-validation"},
                {"question": "What is the ROC curve?", "options": ["Plots true positive rate vs false positive rate at various thresholds", "A loss curve", "A precision-recall curve", "None"], "answer": "Plots true positive rate vs false positive rate at various thresholds"},
                {"question": "What is AUC?", "options": ["Area Under the ROC Curve — higher is better", "Average Uncertainty Coefficient", "None", "Actual vs Uncertainty Curve"], "answer": "Area Under the ROC Curve — higher is better"},
                {"question": "What is Label Encoding?", "options": ["Converting categorical values to integers", "One-hot encoding", "Feature scaling", "None"], "answer": "Converting categorical values to integers"},
                {"question": "What is One-Hot Encoding?", "options": ["Converting categorical values to binary columns", "Label encoding", "Normalizing data", "None"], "answer": "Converting categorical values to binary columns"},
                {"question": "What is a hyperparameter?", "options": ["A model configuration set before training", "A trained model weight", "A feature", "None"], "answer": "A model configuration set before training"},
                {"question": "What is gradient descent?", "options": ["An optimization algorithm minimizing loss by updating weights", "A regularization method", "A feature selector", "None"], "answer": "An optimization algorithm minimizing loss by updating weights"},
                {"question": "What is regularization?", "options": ["Penalizing model complexity to prevent overfitting", "Increasing model complexity", "A data cleaning step", "None"], "answer": "Penalizing model complexity to prevent overfitting"},
                {"question": "What is the difference between L1 and L2 regularization?", "options": ["L1 can zero out weights (sparse), L2 shrinks all weights", "L2 zeros out weights", "Both are identical", "None"], "answer": "L1 can zero out weights (sparse), L2 shrinks all weights"},
                {"question": "What is a support vector machine?", "options": ["A classifier finding the optimal hyperplane maximizing margin", "A clustering algorithm", "A regression-only algorithm", "None"], "answer": "A classifier finding the optimal hyperplane maximizing margin"},
                {"question": "What is the elbow method in K-Means?", "options": ["Finding optimal K where inertia decrease slows down", "Selecting random K", "A training method", "None"], "answer": "Finding optimal K where inertia decrease slows down"},
                {"question": "What is imputation?", "options": ["Filling missing values with estimated ones", "Removing missing rows", "Scaling features", "None"], "answer": "Filling missing values with estimated ones"},
                {"question": "What is the train-test split ratio typically used?", "options": ["80% train, 20% test", "50% train, 50% test", "90% test, 10% train", "None"], "answer": "80% train, 20% test"},
                {"question": "What is KNN?", "options": ["K-Nearest Neighbors — classifies based on closest training examples", "K-Means clustering", "A regression algorithm", "None"], "answer": "K-Nearest Neighbors — classifies based on closest training examples"},
                {"question": "What is a learning curve?", "options": ["Plot of training vs validation score as dataset size grows", "A loss curve", "A feature importance plot", "None"], "answer": "Plot of training vs validation score as dataset size grows"},
                {"question": "What is SMOTE?", "options": ["Synthetic Minority Oversampling Technique for imbalanced data", "A clustering method", "A feature selector", "None"], "answer": "Synthetic Minority Oversampling Technique for imbalanced data"},
                {"question": "What is feature importance in Random Forest?", "options": ["Measure of how much each feature contributes to predictions", "The number of features", "Feature correlation", "None"], "answer": "Measure of how much each feature contributes to predictions"},
                {"question": "What is dimensionality reduction?", "options": ["Reducing number of features while retaining information", "Adding more features", "Scaling features", "None"], "answer": "Reducing number of features while retaining information"},
                {"question": "What is the difference between regression and classification?", "options": ["Regression predicts continuous values, classification predicts categories", "Both predict categories", "Classification predicts continuous values", "None"], "answer": "Regression predicts continuous values, classification predicts categories"},
                {"question": "What is a pair plot in Seaborn?", "options": ["Scatter plots for all feature pairs in dataset", "A single scatter plot", "A correlation matrix", "None"], "answer": "Scatter plots for all feature pairs in dataset"},
                {"question": "What is R-squared in regression?", "options": ["Proportion of variance explained by the model", "The model error", "The accuracy score", "None"], "answer": "Proportion of variance explained by the model"},
                {"question": "What is DBSCAN?", "options": ["A density-based clustering algorithm", "A supervised learning algorithm", "A feature selector", "None"], "answer": "A density-based clustering algorithm"},
                {"question": "What is the purpose of StandardScaler?", "options": ["Scales features to have mean 0 and std 1", "Scales to 0-1 range", "Removes outliers", "None"], "answer": "Scales features to have mean 0 and std 1"},
                {"question": "What is ensemble learning?", "options": ["Combining multiple models to improve performance", "Training one very large model", "A feature engineering technique", "None"], "answer": "Combining multiple models to improve performance"},
                {"question": "What is a pipeline in Scikit-learn?", "options": ["Chains preprocessing and model steps together", "A data loading tool", "A visualization tool", "None"], "answer": "Chains preprocessing and model steps together"},
                {"question": "What is class imbalance?", "options": ["When one class has significantly more samples than another", "When features are imbalanced", "When data is not normalized", "None"], "answer": "When one class has significantly more samples than another"},
            ],
            "hard": [
                {"question": "What is the curse of dimensionality?", "options": ["As features increase, data becomes sparse and algorithms degrade", "Too many training samples", "Too many labels", "None"], "answer": "As features increase, data becomes sparse and algorithms degrade"},
                {"question": "What is the difference between generative and discriminative models?", "options": ["Generative models P(X,Y), discriminative models P(Y|X) directly", "Both model P(Y|X)", "Discriminative models P(X,Y)", "None"], "answer": "Generative models P(X,Y), discriminative models P(Y|X) directly"},
                {"question": "What is maximum likelihood estimation?", "options": ["Finding parameters that maximize probability of observed data", "Minimizing loss function", "Maximizing accuracy", "None"], "answer": "Finding parameters that maximize probability of observed data"},
                {"question": "What is the difference between parametric and non-parametric models?", "options": ["Parametric assume a fixed form, non-parametric grow with data", "Non-parametric have fixed parameters", "Both are identical", "None"], "answer": "Parametric assume a fixed form, non-parametric grow with data"},
                {"question": "What is the kernel trick in SVM?", "options": ["Maps data to higher dimensions implicitly for non-linear separation", "A regularization method", "A feature selector", "None"], "answer": "Maps data to higher dimensions implicitly for non-linear separation"},
                {"question": "What is gradient boosting?", "options": ["Sequentially adding models that correct residual errors of previous", "Parallel ensemble method", "A clustering algorithm", "None"], "answer": "Sequentially adding models that correct residual errors of previous"},
                {"question": "What is the difference between MAE and RMSE?", "options": ["RMSE penalizes large errors more due to squaring, MAE treats all errors equally", "MAE penalizes more", "Both are identical", "None"], "answer": "RMSE penalizes large errors more due to squaring, MAE treats all errors equally"},
                {"question": "What is information gain in decision trees?", "options": ["Reduction in entropy after splitting on a feature", "Gain in model accuracy", "Feature importance score", "None"], "answer": "Reduction in entropy after splitting on a feature"},
                {"question": "What is Gini impurity?", "options": ["Probability of incorrectly classifying a randomly chosen element", "A regularization term", "A distance metric", "None"], "answer": "Probability of incorrectly classifying a randomly chosen element"},
                {"question": "What is XGBoost?", "options": ["An optimized gradient boosting library with regularization", "A neural network", "A clustering tool", "None"], "answer": "An optimized gradient boosting library with regularization"},
                {"question": "What is the Bayes theorem?", "options": ["P(A|B) = P(B|A) * P(A) / P(B)", "P(A|B) = P(A) * P(B)", "None", "P(A|B) = P(B) / P(A)"], "answer": "P(A|B) = P(B|A) * P(A) / P(B)"},
                {"question": "What is Monte Carlo simulation?", "options": ["Using random sampling to model probabilistic outcomes", "A regression method", "A neural network technique", "None"], "answer": "Using random sampling to model probabilistic outcomes"},
                {"question": "What is t-SNE?", "options": ["t-Distributed Stochastic Neighbor Embedding — nonlinear dimensionality reduction for visualization", "A clustering algorithm", "A regression method", "None"], "answer": "t-Distributed Stochastic Neighbor Embedding — nonlinear dimensionality reduction for visualization"},
                {"question": "What is a latent variable?", "options": ["A hidden variable not directly observed but inferred from data", "A feature", "A label", "None"], "answer": "A hidden variable not directly observed but inferred from data"},
                {"question": "What is Expectation Maximization?", "options": ["An iterative algorithm estimating parameters with latent variables", "A gradient descent variant", "A clustering distance metric", "None"], "answer": "An iterative algorithm estimating parameters with latent variables"},
                {"question": "What is a ROC-AUC of 0.5?", "options": ["Model performs no better than random guessing", "Perfect model", "Worst possible model", "None"], "answer": "Model performs no better than random guessing"},
                {"question": "What is covariate shift?", "options": ["Training and test data have different feature distributions", "Label distribution shift", "Missing data issue", "None"], "answer": "Training and test data have different feature distributions"},
                {"question": "What is the silhouette score?", "options": ["Measures how similar a point is to its cluster vs other clusters", "Clustering accuracy", "Number of clusters metric", "None"], "answer": "Measures how similar a point is to its cluster vs other clusters"},
                {"question": "What is multicollinearity in regression?", "options": ["High correlation between predictor variables distorting coefficients", "Target variable correlation", "A data imbalance", "None"], "answer": "High correlation between predictor variables distorting coefficients"},
                {"question": "What is an ROC curve used for?", "options": ["Evaluating classifier performance at all classification thresholds", "Regression evaluation", "Clustering evaluation", "None"], "answer": "Evaluating classifier performance at all classification thresholds"},
                {"question": "What is the difference between bagging and random forest?", "options": ["Random forest adds random feature selection at each split", "Both are identical", "Bagging selects random features", "None"], "answer": "Random forest adds random feature selection at each split"},
                {"question": "What is a Gaussian Naive Bayes assumption?", "options": ["Features are conditionally independent and normally distributed", "Features are correlated", "Data must be balanced", "None"], "answer": "Features are conditionally independent and normally distributed"},
                {"question": "What is data augmentation?", "options": ["Artificially expanding training data by transforming existing samples", "Collecting more data", "Removing outliers", "None"], "answer": "Artificially expanding training data by transforming existing samples"},
                {"question": "What is the purpose of early stopping in ML?", "options": ["Stop training when validation loss stops improving to prevent overfitting", "Stop training when accuracy is 100%", "A hyperparameter technique", "None"], "answer": "Stop training when validation loss stops improving to prevent overfitting"},
                {"question": "What is SHAP?", "options": ["SHapley Additive exPlanations — explaining model predictions using game theory", "A feature selector", "A neural network tool", "None"], "answer": "SHapley Additive exPlanations — explaining model predictions using game theory"},
                {"question": "What is the difference between frequentist and Bayesian statistics?", "options": ["Frequentist treats parameters as fixed, Bayesian treats them as distributions", "Both are identical", "Bayesian treats parameters as fixed", "None"], "answer": "Frequentist treats parameters as fixed, Bayesian treats them as distributions"},
                {"question": "What is target leakage?", "options": ["Using information in features that wouldn't be available at prediction time", "Overfitting to test data", "Data duplication", "None"], "answer": "Using information in features that wouldn't be available at prediction time"},
                {"question": "What is a Markov Chain?", "options": ["A sequence where each state depends only on the previous state", "A neural network", "A regression model", "None"], "answer": "A sequence where each state depends only on the previous state"},
                {"question": "What is isotonic regression?", "options": ["A non-parametric regression that fits a monotone function", "A linear regression variant", "A classification method", "None"], "answer": "A non-parametric regression that fits a monotone function"},
                {"question": "What is the purpose of a validation set?", "options": ["Tuning hyperparameters without touching test data", "Training the model", "Final evaluation", "None"], "answer": "Tuning hyperparameters without touching test data"},
            ],
        },

        # ─────────────────────────────────────────────
        # 8. AI / ML
        # ─────────────────────────────────────────────
        "ai-ml": {
            "easy": [
                {"question": "What is Artificial Intelligence?", "options": ["Machines simulating human intelligence", "A programming language", "A database", "None"], "answer": "Machines simulating human intelligence"},
                {"question": "What is machine learning?", "options": ["Systems that learn from data", "Manual programming of rules", "A database technique", "None"], "answer": "Systems that learn from data"},
                {"question": "What is deep learning?", "options": ["ML using multi-layer neural networks", "Traditional ML", "A database method", "None"], "answer": "ML using multi-layer neural networks"},
                {"question": "What is a neural network?", "options": ["A system of layers inspired by human brain", "A decision tree", "A SQL database", "None"], "answer": "A system of layers inspired by human brain"},
                {"question": "What is TensorFlow?", "options": ["A deep learning framework by Google", "A Python web framework", "A database", "None"], "answer": "A deep learning framework by Google"},
                {"question": "What is PyTorch?", "options": ["A deep learning framework by Meta", "A Python HTTP library", "A CSS framework", "None"], "answer": "A deep learning framework by Meta"},
                {"question": "What is NLP?", "options": ["Natural Language Processing", "Neural Learning Protocol", "None", "Normalized Language Processing"], "answer": "Natural Language Processing"},
                {"question": "What is a CNN?", "options": ["Convolutional Neural Network for image processing", "A clustering algorithm", "A regression model", "None"], "answer": "Convolutional Neural Network for image processing"},
                {"question": "What is an RNN?", "options": ["Recurrent Neural Network for sequential data", "A regression network", "A random neural network", "None"], "answer": "Recurrent Neural Network for sequential data"},
                {"question": "What is a GPT model?", "options": ["Generative Pretrained Transformer — a language model", "A clustering tool", "A visualization library", "None"], "answer": "Generative Pretrained Transformer — a language model"},
                {"question": "What is supervised learning?", "options": ["Learning from labeled data", "Learning from unlabeled data", "Learning by rewards", "None"], "answer": "Learning from labeled data"},
                {"question": "What is unsupervised learning?", "options": ["Learning from unlabeled data to find patterns", "Learning from labeled data", "Learning by reinforcement", "None"], "answer": "Learning from unlabeled data to find patterns"},
                {"question": "What is reinforcement learning?", "options": ["Learning by receiving rewards and penalties", "Supervised learning", "Clustering", "None"], "answer": "Learning by receiving rewards and penalties"},
                {"question": "What is a training epoch?", "options": ["One full pass through the training dataset", "One batch update", "One layer pass", "None"], "answer": "One full pass through the training dataset"},
                {"question": "What is a loss function?", "options": ["Measures how far predictions are from actual values", "A scoring function", "A feature selector", "None"], "answer": "Measures how far predictions are from actual values"},
                {"question": "What is backpropagation?", "options": ["Algorithm computing gradients to update weights", "A forward pass", "A clustering method", "None"], "answer": "Algorithm computing gradients to update weights"},
                {"question": "What is an activation function?", "options": ["Introduces non-linearity in neural networks", "A loss function", "A data loader", "None"], "answer": "Introduces non-linearity in neural networks"},
                {"question": "What is ReLU?", "options": ["Rectified Linear Unit — activation function outputting max(0,x)", "A loss function", "A layer type", "None"], "answer": "Rectified Linear Unit — activation function outputting max(0,x)"},
                {"question": "What is a dataset split?", "options": ["Dividing data into train, validation, test sets", "Splitting a CSV file", "Dividing features", "None"], "answer": "Dividing data into train, validation, test sets"},
                {"question": "What is transfer learning?", "options": ["Reusing a pretrained model on a new task", "Training from scratch", "A data augmentation method", "None"], "answer": "Reusing a pretrained model on a new task"},
                {"question": "What is BERT?", "options": ["Bidirectional Encoder Representations from Transformers", "A CNN model", "A reinforcement algorithm", "None"], "answer": "Bidirectional Encoder Representations from Transformers"},
                {"question": "What is tokenization in NLP?", "options": ["Splitting text into tokens (words/subwords)", "Encoding images", "A data format", "None"], "answer": "Splitting text into tokens (words/subwords)"},
                {"question": "What is Hugging Face?", "options": ["A platform for pre-trained NLP models", "A Python library for ML", "A database tool", "None"], "answer": "A platform for pre-trained NLP models"},
                {"question": "What is overfitting?", "options": ["Model memorizes training data and fails on new data", "Model performs well on all data", "Model underfits", "None"], "answer": "Model memorizes training data and fails on new data"},
                {"question": "What is a batch in deep learning?", "options": ["A subset of training data processed together", "All training data", "One training sample", "None"], "answer": "A subset of training data processed together"},
                {"question": "What is dropout in neural networks?", "options": ["Randomly disabling neurons during training to prevent overfitting", "A layer type", "A loss function", "None"], "answer": "Randomly disabling neurons during training to prevent overfitting"},
                {"question": "What is LangChain?", "options": ["A framework for building LLM applications", "A deep learning library", "A database ORM", "None"], "answer": "A framework for building LLM applications"},
                {"question": "What is a word embedding?", "options": ["A vector representation of a word", "A tokenization method", "A loss function", "None"], "answer": "A vector representation of a word"},
                {"question": "What is YOLO?", "options": ["You Only Look Once — a real-time object detection model", "A text generation model", "A clustering algorithm", "None"], "answer": "You Only Look Once — a real-time object detection model"},
                {"question": "What is a GAN?", "options": ["Generative Adversarial Network — generator vs discriminator", "A clustering method", "A regression network", "None"], "answer": "Generative Adversarial Network — generator vs discriminator"},
            ],
            "medium": [
                {"question": "What is the vanishing gradient problem?", "options": ["Gradients become too small in deep networks stopping learning", "Gradients become too large", "A data preprocessing issue", "None"], "answer": "Gradients become too small in deep networks stopping learning"},
                {"question": "What is the difference between CNN and RNN?", "options": ["CNN processes spatial data, RNN processes sequential data", "RNN processes images", "Both process sequential data", "None"], "answer": "CNN processes spatial data, RNN processes sequential data"},
                {"question": "What is LSTM?", "options": ["Long Short-Term Memory — an RNN that handles long-term dependencies", "A CNN variant", "A transformer model", "None"], "answer": "Long Short-Term Memory — an RNN that handles long-term dependencies"},
                {"question": "What is the attention mechanism?", "options": ["Allows model to focus on relevant parts of input sequence", "A regularization method", "A feature selector", "None"], "answer": "Allows model to focus on relevant parts of input sequence"},
                {"question": "What is the Transformer architecture?", "options": ["A model using self-attention for sequence tasks", "A CNN architecture", "An RNN variant", "None"], "answer": "A model using self-attention for sequence tasks"},
                {"question": "What is fine-tuning?", "options": ["Updating a pretrained model's weights on new task data", "Training from scratch", "Feature engineering", "None"], "answer": "Updating a pretrained model's weights on new task data"},
                {"question": "What is the purpose of batch normalization?", "options": ["Normalizes activations to stabilize and speed up training", "Adds dropout", "Reduces overfitting via regularization", "None"], "answer": "Normalizes activations to stabilize and speed up training"},
                {"question": "What is Adam optimizer?", "options": ["An adaptive learning rate optimizer combining momentum and RMSprop", "A basic gradient descent", "A regularization method", "None"], "answer": "An adaptive learning rate optimizer combining momentum and RMSprop"},
                {"question": "What is RAG?", "options": ["Retrieval Augmented Generation — combining retrieval with LLM generation", "Random Augmented Generation", "A CNN technique", "None"], "answer": "Retrieval Augmented Generation — combining retrieval with LLM generation"},
                {"question": "What is prompt engineering?", "options": ["Designing prompts to get better outputs from LLMs", "Training LLMs", "A data preprocessing step", "None"], "answer": "Designing prompts to get better outputs from LLMs"},
                {"question": "What is data augmentation in CV?", "options": ["Expanding training images via rotations, flips, crops", "Adding more data manually", "Cleaning image data", "None"], "answer": "Expanding training images via rotations, flips, crops"},
                {"question": "What is TF-IDF?", "options": ["Term Frequency-Inverse Document Frequency — text feature extraction", "A deep learning method", "A SQL function", "None"], "answer": "Term Frequency-Inverse Document Frequency — text feature extraction"},
                {"question": "What is Word2Vec?", "options": ["A model learning word embeddings from text", "A tokenizer", "A classification model", "None"], "answer": "A model learning word embeddings from text"},
                {"question": "What is the difference between semantic and syntactic analysis in NLP?", "options": ["Semantic is about meaning, syntactic is about structure/grammar", "Both are about grammar", "Syntactic is about meaning", "None"], "answer": "Semantic is about meaning, syntactic is about structure/grammar"},
                {"question": "What is a learning rate?", "options": ["Controls step size in gradient descent updates", "Controls training duration", "Controls batch size", "None"], "answer": "Controls step size in gradient descent updates"},
                {"question": "What is the difference between model accuracy and loss?", "options": ["Accuracy measures correctness, loss measures prediction error magnitude", "Both measure the same thing", "Loss measures correctness", "None"], "answer": "Accuracy measures correctness, loss measures prediction error magnitude"},
                {"question": "What is max pooling in CNNs?", "options": ["Takes maximum value in each pooling window", "Averages values in window", "A convolution operation", "None"], "answer": "Takes maximum value in each pooling window"},
                {"question": "What is Named Entity Recognition?", "options": ["Identifying entities like names, dates, locations in text", "A text classification task", "A text generation task", "None"], "answer": "Identifying entities like names, dates, locations in text"},
                {"question": "What is semantic search?", "options": ["Searching based on meaning/context rather than keywords", "Keyword-based search", "A database search", "None"], "answer": "Searching based on meaning/context rather than keywords"},
                {"question": "What is ResNet?", "options": ["A deep CNN using residual connections to solve vanishing gradients", "An RNN", "A transformer model", "None"], "answer": "A deep CNN using residual connections to solve vanishing gradients"},
                {"question": "What is an autoencoder?", "options": ["A neural network learning compressed representation of input", "A generative model", "A classification model", "None"], "answer": "A neural network learning compressed representation of input"},
                {"question": "What is the purpose of the embedding layer?", "options": ["Converts categorical tokens to dense vector representations", "A pooling layer", "A normalization layer", "None"], "answer": "Converts categorical tokens to dense vector representations"},
                {"question": "What is multi-head attention?", "options": ["Running multiple attention operations in parallel", "A single attention operation", "A CNN variant", "None"], "answer": "Running multiple attention operations in parallel"},
                {"question": "What is positional encoding in Transformers?", "options": ["Adds sequence position information since attention has no order", "A regularization method", "A tokenization method", "None"], "answer": "Adds sequence position information since attention has no order"},
                {"question": "What is text summarization?", "options": ["Generating a shorter version of a text", "Classifying text", "Translating text", "None"], "answer": "Generating a shorter version of a text"},
                {"question": "What is a vector database?", "options": ["A database storing and searching embedding vectors", "A SQL database", "A graph database", "None"], "answer": "A database storing and searching embedding vectors"},
                {"question": "What is the purpose of a softmax function?", "options": ["Converts logits to probabilities summing to 1", "A regression output", "A hidden layer activation", "None"], "answer": "Converts logits to probabilities summing to 1"},
                {"question": "What is RLHF?", "options": ["Reinforcement Learning from Human Feedback — aligning LLMs", "Recursive Learning for Human Feedback", "A CNN training technique", "None"], "answer": "Reinforcement Learning from Human Feedback — aligning LLMs"},
                {"question": "What is temperature in LLMs?", "options": ["Controls randomness of model outputs", "A training hyperparameter", "A tokenization setting", "None"], "answer": "Controls randomness of model outputs"},
                {"question": "What is a foundation model?", "options": ["A large pretrained model adaptable to many tasks", "A small task-specific model", "A database model", "None"], "answer": "A large pretrained model adaptable to many tasks"},
            ],
            "hard": [
                {"question": "What is the difference between self-attention and cross-attention?", "options": ["Self-attention attends within same sequence, cross-attention between two sequences", "Both attend within same sequence", "Cross-attention is within same sequence", "None"], "answer": "Self-attention attends within same sequence, cross-attention between two sequences"},
                {"question": "What is the exploding gradient problem?", "options": ["Gradients grow exponentially making training unstable", "Gradients become zero", "A data preprocessing issue", "None"], "answer": "Gradients grow exponentially making training unstable"},
                {"question": "What is quantization in LLMs?", "options": ["Reducing model weights from FP32 to INT8/INT4 to reduce memory", "Increasing model precision", "A training technique", "None"], "answer": "Reducing model weights from FP32 to INT8/INT4 to reduce memory"},
                {"question": "What is the difference between GPT and BERT?", "options": ["GPT is autoregressive (left-to-right), BERT is bidirectional", "Both are autoregressive", "BERT is autoregressive", "None"], "answer": "GPT is autoregressive (left-to-right), BERT is bidirectional"},
                {"question": "What is mixture of experts (MoE)?", "options": ["A model architecture routing inputs to specialized expert sub-networks", "Combining multiple training datasets", "An ensemble method", "None"], "answer": "A model architecture routing inputs to specialized expert sub-networks"},
                {"question": "What is LoRA?", "options": ["Low-Rank Adaptation — efficient LLM fine-tuning by adding small rank matrices", "A large model architecture", "A regularization method", "None"], "answer": "Low-Rank Adaptation — efficient LLM fine-tuning by adding small rank matrices"},
                {"question": "What is knowledge distillation?", "options": ["Training a small student model to mimic a large teacher model", "Compressing data", "Quantizing models", "None"], "answer": "Training a small student model to mimic a large teacher model"},
                {"question": "What is hallucination in LLMs?", "options": ["Model generating plausible but factually incorrect information", "Model refusing to answer", "Model repeating context", "None"], "answer": "Model generating plausible but factually incorrect information"},
                {"question": "What is grounding in LLMs?", "options": ["Connecting model outputs to verifiable external knowledge", "Training on large datasets", "A tokenization method", "None"], "answer": "Connecting model outputs to verifiable external knowledge"},
                {"question": "What is the difference between zero-shot and few-shot learning?", "options": ["Zero-shot uses no examples, few-shot uses a few examples in prompt", "Both use training examples", "Few-shot uses no examples", "None"], "answer": "Zero-shot uses no examples, few-shot uses a few examples in prompt"},
                {"question": "What is a diffusion model?", "options": ["A generative model learning to reverse a noise process", "A CNN variant", "A clustering model", "None"], "answer": "A generative model learning to reverse a noise process"},
                {"question": "What is chain-of-thought prompting?", "options": ["Encouraging model to reason step-by-step before answering", "A multi-turn dialogue", "A retrieval technique", "None"], "answer": "Encouraging model to reason step-by-step before answering"},
                {"question": "What is the purpose of residual connections?", "options": ["Allow gradients to flow directly through skip connections avoiding vanishing gradients", "Add regularization", "Reduce parameters", "None"], "answer": "Allow gradients to flow directly through skip connections avoiding vanishing gradients"},
                {"question": "What is a sparse transformer?", "options": ["A transformer using sparse attention patterns to scale to longer sequences", "A small transformer", "A compressed transformer", "None"], "answer": "A transformer using sparse attention patterns to scale to longer sequences"},
                {"question": "What is contrastive learning?", "options": ["Learning representations by pulling similar samples close and pushing dissimilar apart", "Supervised classification", "A GAN technique", "None"], "answer": "Learning representations by pulling similar samples close and pushing dissimilar apart"},
                {"question": "What is the context window in LLMs?", "options": ["Maximum number of tokens the model can process at once", "The training data size", "The number of parameters", "None"], "answer": "Maximum number of tokens the model can process at once"},
                {"question": "What is model distillation vs pruning?", "options": ["Distillation trains smaller model from teacher, pruning removes weights from model", "Both remove weights", "Pruning trains smaller model", "None"], "answer": "Distillation trains smaller model from teacher, pruning removes weights from model"},
                {"question": "What is CLIP?", "options": ["Contrastive Language-Image Pretraining — aligning text and image embeddings", "A text-only model", "A CNN architecture", "None"], "answer": "Contrastive Language-Image Pretraining — aligning text and image embeddings"},
                {"question": "What is a reward model in RLHF?", "options": ["A model trained to predict human preference scores", "The main language model", "A discriminator", "None"], "answer": "A model trained to predict human preference scores"},
                {"question": "What is catastrophic forgetting?", "options": ["Model forgets previously learned tasks when trained on new ones", "Model overfits new data", "A data issue", "None"], "answer": "Model forgets previously learned tasks when trained on new ones"},
                {"question": "What is model parallelism?", "options": ["Splitting model layers across multiple GPUs", "Splitting data across GPUs", "Training multiple models", "None"], "answer": "Splitting model layers across multiple GPUs"},
                {"question": "What is an agentic AI system?", "options": ["An AI that autonomously plans and executes multi-step tasks", "A rule-based system", "A chatbot", "None"], "answer": "An AI that autonomously plans and executes multi-step tasks"},
                {"question": "What is positional encoding in Transformers?", "options": ["Injects token position information since attention is order-invariant", "A regularization layer", "A tokenization step", "None"], "answer": "Injects token position information since attention is order-invariant"},
                {"question": "What is beam search?", "options": ["Decoding strategy keeping top-k candidate sequences at each step", "A greedy decoder", "A sampling method", "None"], "answer": "Decoding strategy keeping top-k candidate sequences at each step"},
                {"question": "What is the difference between data parallelism and model parallelism?", "options": ["Data parallelism splits data, model parallelism splits model across devices", "Both split data", "Model parallelism splits data", "None"], "answer": "Data parallelism splits data, model parallelism splits model across devices"},
                {"question": "What is instruction tuning?", "options": ["Fine-tuning LLMs on instruction-following datasets", "Pretraining from scratch", "A prompting technique", "None"], "answer": "Fine-tuning LLMs on instruction-following datasets"},
                {"question": "What is a token in LLMs?", "options": ["A subword unit the model processes", "A full word", "A character", "None"], "answer": "A subword unit the model processes"},
                {"question": "What is the scaling law in AI?", "options": ["Model performance predictably improves with more data, compute, and parameters", "More data always causes overfitting", "Smaller models are better", "None"], "answer": "Model performance predictably improves with more data, compute, and parameters"},
                {"question": "What is tool use in LLMs?", "options": ["LLM calling external functions or APIs to complete tasks", "A training technique", "A tokenization method", "None"], "answer": "LLM calling external functions or APIs to complete tasks"},
                {"question": "What is a multimodal model?", "options": ["A model processing multiple input types like text, image, and audio", "A text-only model", "A vision-only model", "None"], "answer": "A model processing multiple input types like text, image, and audio"},
            ],
        },
    }

    if request.method == "POST":
        selected = request.session.get("quiz_questions", [])
        total = len(selected)
        correct = 0
        for i, q in enumerate(selected, start=1):
            if request.POST.get(f"question{i}") == q["answer"]:
                correct += 1
        wrong = total - correct
        score = int((correct / total) * 100) if total > 0 else 0
        rank = "Excellent 🏆" if score >= 90 else "Good 👍" if score >= 70 else "Average 📘" if score >= 50 else "Needs Improvement 💪"
        return render(request, "quiz_result.html", {
            "correct": correct, "wrong": wrong, "score": score,
            "rank": rank, "course_name": course_name,
             "course_slug": course_name,
            "difficulty": request.session.get("quiz_difficulty", difficulty).title(),
            "total": total,
        })

    course_questions = all_questions.get(course_name, {})
    level_questions = course_questions.get(difficulty, [])
    selected = random.sample(level_questions, min(num_questions, len(level_questions)))

    request.session["quiz_questions"] = selected
    request.session["quiz_difficulty"] = difficulty

    return render(request, "quiz_questions.html", {
        "questions": selected,
        "course_name": course_name.replace("-", " ").title(),
        "course_slug": course_name,

        "difficulty": difficulty.title(),
        "num_questions": num_questions,
    })


def interview_home(request, course_name):

    course_title = course_name.replace(
        "-",
        " "
    ).title()

    return render(
        request,
        "interview_home.html",
        {
            "course_name": course_title,
            "course_slug": course_name
        }
    )

def interview_questions_view(request, course_name, level):

    level = level.lower()

    if level not in ["easy", "medium", "hard"]:
        raise Http404("Invalid level")

    questions = (
        INTERVIEW_QUESTIONS
        .get(course_name, {})
        .get(level, [])
    )

    course_title = course_name.replace(
        "-",
        " "
    ).title()

    return render(
        request,
        "interview_questions.html",
        {
            "questions": questions,
            "level": level.title(),
            "course_name": course_title
        }
    )

def resume_questions(request, course_name):
    questions = [
        "What is JVM?", "Explain OOP concepts.", "What is Spring Boot?",
        "How does React Virtual DOM work?", "Explain REST API.",
        "Explain your project architecture.", "Why did you choose MySQL?",
        "What challenges did you face in your project?"
    ]
    return render(request, "resume_questions.html", {
        "course_name": course_name.replace("-", " ").title(),
        "questions": questions
    })


def dashboard(request, course_name):
    return render(request, "dashboard.html", {
        "course_name": course_name.replace("-", " ").title(),
        "roadmap_progress": 70,
        "easy_score": 90,
        "medium_score": 80,
        "hard_score": 60,
        "interview_questions": 25,
        "resume_questions": 10,
        "status": "Advanced Learner"
    })


def ats_checker(request, course_name):
    ats_score = None
    missing_skills = []
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            from django.contrib.auth.models import User
            resume.user = User.objects.first()
            resume.save()
            text = extract_text_from_pdf(resume.resume_file.path)
            ats_score = calculate_ats_score(text)
            skills = ["python", "java", "sql", "django", "react", "node", "mongodb", "git", "api", "project", "internship", "aws", "docker"]
            for skill in skills:
                if skill not in text.lower():
                    missing_skills.append(skill.upper())
    else:
        form = ResumeForm()
    return render(request, "ats_checker.html", {
        "course_name": course_name.replace("-", " ").title(),
        "form": form,
        "ats_score": ats_score,
        "missing_skills": missing_skills
    })


def ai_mentor(request):
    answer = ""
    if request.method == "POST":
        question = request.POST.get("question")
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"""
You are AI Mentor for AI Career Copilot.

First understand the user's question.

Rules:

1. If the question is mathematical, solve it directly.
   Example:
   Question: 12/2
   Answer: 12 ÷ 2 = 6

2. If the question is programming related, answer using:

📌 Definition
⭐ Key Points
💡 Example
🎯 Interview Tip

3. If the question is an interview question,
   give a professional interview answer.

4. If the question is a resume question,
   give resume guidance.

5. Use simple English.

6. Avoid unnecessary information.

7. Keep answers concise and useful.

Question:
{question}
"""
            response = model.generate_content(prompt)  # ✅ fixed indentation
            answer = response.text
        except Exception as e:
            answer = "AI Mentor is temporarily unavailable.\n\n" + str(e)
    return render(request, "ai_mentor.html", {"answer": answer})

from django.shortcuts import render



@login_required
def resume_generator(request, course_slug):

    generated_resume = ""

    if request.method == "POST":

        uploaded_file = request.FILES.get(
            "resume_file"
        )

        text = ""

        if uploaded_file:

            if uploaded_file.name.endswith(".pdf"):

                text = extract_text_from_pdf(
                    uploaded_file
                )

            elif uploaded_file.name.endswith(".docx"):

                text = extract_docx_text(
                    uploaded_file
                )

        if text:

            try:

                course_name = course_slug.replace(
                    "-",
                    " "
                ).title()

                prompt = f"""
You are an ATS Resume Expert.

Create a professional ATS-optimized resume for:

{course_name}

Resume Content:

{text[:6000]}

Rules:

1. Improve formatting.
2. Rewrite summary professionally.
3. Improve project descriptions.
4. Improve skills section.
5. Improve experience section.
6. Add ATS keywords.
7. Return plain text only.
"""

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    prompt
                )

                generated_resume = response.text

            except Exception as e:

                generated_resume = str(e)

    return render(
        request,
        "resume_generator.html",
        {
            "course_slug": course_slug,
            "course_name": course_slug.replace(
                "-",
                " "
            ).title(),
            "generated_resume": generated_resume
        }
    )

print(INTERVIEW_QUESTIONS.keys())