"""
ChronoSkill — Skill Graph Definitions, Free Learning Vault & Path Planning Engine.
Defines expanded canonical skill taxonomy, alias normalization maps,
prerequisite DAG, free beginner-friendly resources, and topological path generation logic
across 12 tech disciplines.
"""

from __future__ import annotations
from typing import Any
import pandas as pd


# ---------------------------------------------------------------------------
# 12 Target Disciplines — Benchmark Compensation in Indian Rupees (INR / LPA)
# ---------------------------------------------------------------------------

ROLE_INR_BENCHMARKS: dict[str, dict[str, str]] = {
    "Data Analyst": {
        "range": "₹6.5 - ₹14.0 LPA",
        "entry": "₹5.0 - ₹8.0 LPA",
        "senior": "₹12.0 - ₹18.0 LPA",
        "hourly": "₹1,200 - ₹2,500/hr"
    },
    "Data Scientist": {
        "range": "₹12.0 - ₹26.0 LPA",
        "entry": "₹8.0 - ₹14.0 LPA",
        "senior": "₹20.0 - ₹38.0 LPA",
        "hourly": "₹2,500 - ₹5,000/hr"
    },
    "ML Engineer": {
        "range": "₹15.0 - ₹32.0 LPA",
        "entry": "₹10.0 - ₹16.0 LPA",
        "senior": "₹25.0 - ₹45.0 LPA",
        "hourly": "₹3,000 - ₹6,500/hr"
    },
    "AI / GenAI Engineer": {
        "range": "₹18.0 - ₹38.0 LPA",
        "entry": "₹12.0 - ₹18.0 LPA",
        "senior": "₹28.0 - ₹55.0 LPA",
        "hourly": "₹3,500 - ₹7,500/hr"
    },
    "Data Engineer": {
        "range": "₹10.0 - ₹24.0 LPA",
        "entry": "₹7.0 - ₹12.0 LPA",
        "senior": "₹18.0 - ₹35.0 LPA",
        "hourly": "₹2,000 - ₹4,500/hr"
    },
    "Backend Developer": {
        "range": "₹8.0 - ₹22.0 LPA",
        "entry": "₹6.0 - ₹10.0 LPA",
        "senior": "₹16.0 - ₹32.0 LPA",
        "hourly": "₹1,800 - ₹3,800/hr"
    },
    "Frontend Developer": {
        "range": "₹7.0 - ₹20.0 LPA",
        "entry": "₹5.0 - ₹9.0 LPA",
        "senior": "₹14.0 - ₹28.0 LPA",
        "hourly": "₹1,500 - ₹3,500/hr"
    },
    "Full-Stack Developer": {
        "range": "₹9.0 - ₹24.0 LPA",
        "entry": "₹6.0 - ₹11.0 LPA",
        "senior": "₹16.0 - ₹34.0 LPA",
        "hourly": "₹2,000 - ₹4,200/hr"
    },
    "DevOps Engineer": {
        "range": "₹10.0 - ₹25.0 LPA",
        "entry": "₹7.0 - ₹12.0 LPA",
        "senior": "₹18.0 - ₹36.0 LPA",
        "hourly": "₹2,200 - ₹4,800/hr"
    },
    "Cloud Architect": {
        "range": "₹20.0 - ₹45.0 LPA",
        "entry": "₹14.0 - ₹20.0 LPA",
        "senior": "₹32.0 - ₹60.0 LPA",
        "hourly": "₹4,000 - ₹9,000/hr"
    },
    "Site Reliability Engineer (SRE)": {
        "range": "₹12.0 - ₹28.0 LPA",
        "entry": "₹8.0 - ₹14.0 LPA",
        "senior": "₹20.0 - ₹40.0 LPA",
        "hourly": "₹2,500 - ₹5,500/hr"
    },
    "Cybersecurity Analyst": {
        "range": "₹8.5 - ₹22.0 LPA",
        "entry": "₹6.0 - ₹10.0 LPA",
        "senior": "₹15.0 - ₹30.0 LPA",
        "hourly": "₹2,000 - ₹4,500/hr"
    }
}


# ---------------------------------------------------------------------------
# Free Curated Learning Resources per Role (World-Class & Free)
# ---------------------------------------------------------------------------

ROLE_FREE_RESOURCES: dict[str, list[dict[str, str]]] = {
    "Data Analyst": [
        {"title": "Google Data Analytics Certificate (Free Audit)", "provider": "Coursera / Google", "type": "Interactive Course", "url": "https://www.coursera.org/professional-certificates/google-data-analytics", "why": "The industry gold standard for beginners to learn spreadsheets, SQL, Tableau, and R."},
        {"title": "Data Analysis with Python Certification", "provider": "freeCodeCamp", "type": "Hands-on Interactive Lab", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "why": "Completely free, project-based curriculum covering NumPy, Pandas, Matplotlib, and SeaBorn."},
        {"title": "Kaggle Learn: SQL & Pandas Micro-Courses", "provider": "Kaggle (Google)", "type": "Bite-Sized Interactive Notebooks", "url": "https://www.kaggle.com/learn", "why": "Practice SQL queries and data manipulation directly in your browser with zero setup."},
        {"title": "Alex The Analyst Bootcamp", "provider": "YouTube", "type": "Complete Video Playlist", "url": "https://www.youtube.com/@AlexTheAnalyst", "why": "Extremely popular practical guide covering portfolio projects, resume building, and interview prep."}
    ],
    "Data Scientist": [
        {"title": "Harvard CS50: Intro to AI with Python", "provider": "Harvard University / edX", "type": "University Course (Free Audit)", "url": "https://cs50.harvard.edu/ai/", "why": "Teaches fundamental search algorithms, probability, optimization, and neural networks from scratch."},
        {"title": "Practical Deep Learning for Coders", "provider": "fast.ai", "type": "Hands-on Video Course & Book", "url": "https://course.fast.ai/", "why": "Top-down approach designed to train world-class machine learning models from Day 1."},
        {"title": "Intro to Machine Learning & Intermediate ML", "provider": "Kaggle Learn", "type": "Interactive Practice", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "why": "Build your first Random Forest and XGBoost models on real competition data in minutes."},
        {"title": "StatQuest with Josh Starmer", "provider": "YouTube", "type": "Visual Concept Masterclasses", "url": "https://www.youtube.com/@statquest", "why": "Breaks down complex mathematical formulas into intuitive step-by-step visual illustrations."}
    ],
    "ML Engineer": [
        {"title": "Stanford CS229: Machine Learning by Andrew Ng", "provider": "Stanford University / YouTube", "type": "Full Lecture Series", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU", "why": "The definitive mathematical and theoretical foundation of machine learning."},
        {"title": "Made With ML by Goku Mohandas", "provider": "Made With ML", "type": "End-to-End MLOps Course", "url": "https://madewithml.com/", "why": "Teaches taking ML from prototype to production: data versioning, MLflow, CI/CD, and serving."},
        {"title": "DeepLearning.AI Short Courses", "provider": "DeepLearning.AI", "type": "Hands-on Jupyter Labs", "url": "https://www.deeplearning.ai/short-courses/", "why": "Official free courses on LangChain, Hugging Face, vector databases, and LLM applications."},
        {"title": "Full Stack Deep Learning", "provider": "FSDL", "type": "Production ML Bootcamp", "url": "https://fullstackdeeplearning.com/", "why": "Industry-grade training on deploying models, GPUs, Docker, monitoring, and prompt pipelines."}
    ],
    "AI / GenAI Engineer": [
        {"title": "Generative AI with Large Language Models", "provider": "DeepLearning.AI / AWS", "type": "Free Course Audit", "url": "https://www.coursera.org/learn/generative-ai-with-llms", "why": "Official comprehensive guide to Transformer architectures, LoRA fine-tuning, RLHF, and deployment."},
        {"title": "Andrej Karpathy's Neural Networks: Zero to Hero", "provider": "YouTube", "type": "Engineering Masterclass", "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "why": "Build micrograd, makemore, and a complete GPT model from raw code with ex-Tesla AI Director Andrej Karpathy."},
        {"title": "LangChain & Vector Databases for LLMs", "provider": "DeepLearning.AI", "type": "Interactive Jupyter Labs", "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/", "why": "The industry blueprint for building RAG applications, vector memory, and autonomous AI agents."},
        {"title": "Hugging Face Open-Source NLP & LLM Course", "provider": "Hugging Face", "type": "Hands-on Python Guide", "url": "https://huggingface.co/learn/nlp-course", "why": "Master using thousands of pre-trained models, tokenizers, and datasets for free."}
    ],
    "Data Engineer": [
        {"title": "Data Engineering Zoomcamp (DataTalks.Club)", "provider": "DataTalksClub (GitHub)", "type": "Open-Source Free Bootcamp", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "why": "The world's most famous free data engineering bootcamp: Docker, SQL, Airflow, Spark, BigQuery, dbt, and Kafka."},
        {"title": "dbt Fundamentals Certification Course", "provider": "dbt Labs", "type": "Interactive Certification", "url": "https://courses.getdbt.com/courses/fundamentals", "why": "Learn modern data transformation, automated data testing, and documentation."},
        {"title": "Apache Spark Official Programming Guides", "provider": "Apache.org", "type": "Documentation & Labs", "url": "https://spark.apache.org/docs/latest/api/python/", "why": "The official guide for distributed big data processing and PySpark pipelines."},
        {"title": "Kafka: The Definitive Guide (Free eBook)", "provider": "Confluent", "type": "Free Book Download", "url": "https://www.confluent.io/resources/kafka-the-definitive-guide/", "why": "Everything you need to master real-time data streaming and event-driven architectures."}
    ],
    "Backend Developer": [
        {"title": "The Odin Project: Foundations & Node.js Path", "provider": "The Odin Project", "type": "Comprehensive Free Curriculum", "url": "https://www.theodinproject.com/", "why": "Zero-to-hire open-source curriculum focusing on building authentic GitHub portfolio projects."},
        {"title": "Backend Development and APIs Certification", "provider": "freeCodeCamp", "type": "Interactive Coding Environment", "url": "https://www.freecodecamp.org/learn/back-end-development-and-apis/", "why": "Build real microservices, REST endpoints, MongoDB databases, and authentication layers."},
        {"title": "ByteByteGo System Design Primer", "provider": "Alex Xu / ByteByteGo", "type": "Articles & Architecture Diagrams", "url": "https://bytebytego.com/", "why": "Learn how high-traffic systems like YouTube, WhatsApp, and Netflix handle millions of requests."},
        {"title": "FastAPI Official Interactive Tutorial", "provider": "FastAPI.tiangolo.com", "type": "Documentation & Hands-on Guide", "url": "https://fastapi.tiangolo.com/tutorial/", "why": "One of the best-written software documentation sites in existence, packed with copy-pasteable examples."}
    ],
    "Frontend Developer": [
        {"title": "Full Stack Open (React & Modern Web)", "provider": "University of Helsinki", "type": "University-Accredited Course", "url": "https://fullstackopen.com/en/", "why": "World-renowned deep dive into React, Redux, Node.js, GraphQL, and TypeScript."},
        {"title": "The Odin Project: Intermediate & Advanced HTML/CSS", "provider": "The Odin Project", "type": "Project-Driven Track", "url": "https://www.theodinproject.com/paths/full-stack-javascript", "why": "Teaches proper layout, accessibility, responsive design, and CSS Grid from first principles."},
        {"title": "MDN Web Docs (Mozilla Developer Network)", "provider": "Mozilla", "type": "Official Reference & Interactive Tutorials", "url": "https://developer.mozilla.org/en-US/docs/Learn", "why": "The definitive, authoritative reference manual for every web developer on Earth."},
        {"title": "JavaScript30 by Wes Bos", "provider": "Wes Bos", "type": "30 Day Vanilla JS Challenge", "url": "https://javascript30.com/", "why": "Build 30 vanilla JS projects in 30 days without frameworks, libraries, or compilers."}
    ],
    "Full-Stack Developer": [
        {"title": "Full Stack Open: Helsinki University", "provider": "University of Helsinki", "type": "Complete Engineering Course", "url": "https://fullstackopen.com/en/", "why": "Widely considered the best single free full-stack curriculum available online."},
        {"title": "CS50W: Web Programming with Python and JavaScript", "provider": "Harvard University / edX", "type": "University Masterclass (Free)", "url": "https://cs50.harvard.edu/web/", "why": "Covers database design, scalability, security, Django backends, and React/JS frontends."},
        {"title": "freeCodeCamp 3,000-Hour Full Stack Curriculum", "provider": "freeCodeCamp", "type": "Verified Certification Track", "url": "https://www.freecodecamp.org/", "why": "Earn certified credentials by submitting verified full-stack applications."},
        {"title": "The Odin Project Full-Stack JS Path", "provider": "The Odin Project", "type": "Self-Paced Web Engineering", "url": "https://www.theodinproject.com/paths/full-stack-javascript", "why": "Master everything from Git commands to deploying full-stack Postgres-backed Node apps."}
    ],
    "DevOps Engineer": [
        {"title": "TechWorld with Nana: DevOps Bootcamp", "provider": "YouTube / TechWorld with Nana", "type": "Visual Video Bootcamp", "url": "https://www.youtube.com/@TechWorldwithNana", "why": "The clearest beginner visual explanation of Docker, Kubernetes, CI/CD, and Terraform anywhere."},
        {"title": "OverTheWire: Bandit (Linux Terminal Wargame)", "provider": "OverTheWire", "type": "Gamified Terminal SSH Challenge", "url": "https://overthewire.org/wargames/bandit/", "why": "Learn Linux commands, file permissions, SSH, and scripting by solving 34 progressively harder levels."},
        {"title": "Kubernetes Official Interactive Tutorials", "provider": "Kubernetes.io", "type": "In-Browser Terminal Simulations", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "why": "Launch Pods, deploy containers, and inspect services right inside your browser without installing anything."},
        {"title": "GitHub Actions Official Quickstart", "provider": "GitHub Docs", "type": "CI/CD Practical Guide", "url": "https://docs.github.com/en/actions/quickstart", "why": "Automate your builds, tests, and cloud deployments for free on GitHub."}
    ],
    "Cloud Architect": [
        {"title": "AWS Certified Solutions Architect Associate Prep", "provider": "freeCodeCamp", "type": "14-Hour Full Masterclass", "url": "https://www.youtube.com/watch?v=Ia-UEYYR44s", "why": "The premier comprehensive preparation course for designing resilient, secure, and cost-effective cloud architectures."},
        {"title": "Google Cloud Architecture Framework", "provider": "Google Cloud", "type": "Architecture Blueprint Library", "url": "https://cloud.google.com/architecture/framework", "why": "Explore real production architecture diagrams for multi-region databases, disaster recovery, and networking."},
        {"title": "HashiCorp Learn Terraform Tutorials", "provider": "HashiCorp", "type": "Hands-on Interactive Lab", "url": "https://developer.hashicorp.com/terraform/tutorials", "why": "Master automated Infrastructure as Code across AWS, Azure, and Google Cloud."},
        {"title": "AWS Well-Architected Labs", "provider": "Amazon Web Services", "type": "Free Hands-on Workshops", "url": "https://www.wellarchitectedlabs.com/", "why": "Hands-on labs on operational excellence, security, reliability, performance, and cost optimization."}
    ],
    "Site Reliability Engineer (SRE)": [
        {"title": "Google's Site Reliability Engineering Books (Free)", "provider": "Google SRE Team", "type": "Free Official Books", "url": "https://sre.google/books/", "why": "The foundational texts that created the modern discipline of SRE, written by Google engineers."},
        {"title": "Prometheus & Grafana Masterclass", "provider": "TechWorld with Nana", "type": "Video Course", "url": "https://www.youtube.com/watch?v=9TYX7HKtr3I", "why": "Learn metrics collection, alerting, SLOs, SLIs, error budgets, and live cluster health monitoring."},
        {"title": "OverTheWire: Bandit (Terminal Skills)", "provider": "OverTheWire", "type": "Gamified Linux Shell Game", "url": "https://overthewire.org/wargames/bandit/", "why": "Build lightning-fast terminal troubleshooting and debugging muscle memory."},
        {"title": "Introduction to SRE and Incident Management", "provider": "Coursera (Free Audit)", "type": "Foundational Course", "url": "https://www.coursera.org/learn/site-reliability-engineering-slos", "why": "Learn to calculate Service Level Objectives, error budgets, and incident post-mortems."}
    ],
    "Cybersecurity Analyst": [
        {"title": "PortSwigger Web Security Academy", "provider": "PortSwigger (Creators of Burp Suite)", "type": "Free Interactive Attack Labs", "url": "https://portswigger.net/web-security", "why": "The undisputed gold standard for hands-on learning of SQL Injection, XSS, CSRF, and authentication bypass."},
        {"title": "TryHackMe: Pre-Security & Complete Beginner Path", "provider": "TryHackMe", "type": "Gamified Virtual Lab Rooms", "url": "https://tryhackme.com/", "why": "Interactive browser-based virtual machines walking through networking, Linux, and penetration testing."},
        {"title": "OverTheWire Wargames: Natas (Web Security)", "provider": "OverTheWire", "type": "Browser Exploitation Challenges", "url": "https://overthewire.org/wargames/natas/", "why": "Learn web application vulnerabilities hands-on by cracking server passwords step by step."},
        {"title": "Professor Messer's CompTIA Security+ Course", "provider": "Professor Messer / YouTube", "type": "Complete Certification Training", "url": "https://www.professormesser.com/", "why": "Comprehensive video training covering threats, attacks, vulnerabilities, cryptography, and network defense."}
    ]
}


# ---------------------------------------------------------------------------
# Canonical Taxonomy & Prerequisite DAG
# ---------------------------------------------------------------------------

SKILLS_GRAPH: dict[str, dict[str, Any]] = {
    # --- Languages & Foundations ---
    "Python": {
        "category": "Languages", "prerequisites": [], "difficulty": "Beginner", "estimated_weeks": 3,
        "description": "Core syntax, data types, loops, functions, OOP, and file handling.",
        "plain_english": "The most beginner-friendly programming language in the world. Used for writing scripts, analyzing data, and building AI.",
        "why_this_skill": "Without Python, tools like Pandas, Scikit-Learn, and PyTorch cannot be understood or run.",
        "topics_checklist": [
            "Variables, conditionals (if/else), and loops (for/while)",
            "Data structures: Lists, dictionaries, tuples, sets",
            "Functions, parameter passing, and return values",
            "Reading/writing files and error handling with try/except"
        ],
        "milestone": "CLI utility or automation script using modern Pythonic patterns.",
        "beginner_project": "Build an Automated Expense Tracker that reads numbers from a text file and prints categorized totals.",
        "free_resources": [
            {"title": "Python for Beginners (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=eWRfhZUzrAc", "provider": "YouTube"},
            {"title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/", "provider": "Python.org"},
            {"title": "Kaggle Python Micro-Course", "url": "https://www.kaggle.com/learn/python", "provider": "Kaggle"}
        ]
    },
    "HTML & CSS": {
        "category": "Frontend", "prerequisites": [], "difficulty": "Beginner", "estimated_weeks": 2,
        "description": "Semantic markup, modern layout models (Flexbox, CSS Grid), responsive design.",
        "plain_english": "HTML provides the skeleton of websites (text, buttons, images), and CSS styles them (colors, fonts, layouts).",
        "why_this_skill": "Every website or web application on the internet is fundamentally rendered as HTML and CSS.",
        "topics_checklist": [
            "Semantic HTML tags (header, nav, main, section, footer)",
            "CSS box model (margin, padding, border, content)",
            "Flexbox layout (justify-content, align-items, flex-direction)",
            "CSS Grid and responsive mobile media queries (@media)"
        ],
        "milestone": "Fully responsive editorial landing page without frameworks.",
        "beginner_project": "Create a clean personal portfolio landing page that looks great on both phone and laptop.",
        "free_resources": [
            {"title": "Responsive Web Design Certification", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "provider": "freeCodeCamp"},
            {"title": "MDN Learn HTML & CSS", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "provider": "MDN"}
        ]
    },
    "JavaScript": {
        "category": "Languages", "prerequisites": ["HTML & CSS"], "difficulty": "Beginner", "estimated_weeks": 3,
        "description": "ECMAScript modern standards, closures, DOM manipulation, asynchronous event loop.",
        "plain_english": "The programming language that runs inside web browsers. It makes static pages interactive (clicks, popups, data fetching).",
        "why_this_skill": "Browsers only run JavaScript. You cannot build modern web applications or use React without it.",
        "topics_checklist": [
            "DOM manipulation: querySelector, addEventListener, innerHTML",
            "Arrow functions, array methods (map, filter, reduce)",
            "Promises, async/await, and fetching data from REST APIs",
            "Scope, closures, and local storage (localStorage)"
        ],
        "milestone": "Interactive DOM-driven application with async data fetching.",
        "beginner_project": "Build an interactive Weather Dashboard that calls a free weather API and updates the page dynamically.",
        "free_resources": [
            {"title": "JavaScript Algorithms & Data Structures", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/", "provider": "freeCodeCamp"},
            {"title": "JavaScript.info (The Modern JS Tutorial)", "url": "https://javascript.info/", "provider": "Community"}
        ]
    },
    "TypeScript": {
        "category": "Languages", "prerequisites": ["JavaScript"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Static typing, generics, utility types, compile-time contract enforcement.",
        "plain_english": "JavaScript with superpowers (types). It catches bugs before your code even runs, preventing production crashes.",
        "why_this_skill": "Modern companies write almost all their production frontend and backend code in TypeScript.",
        "topics_checklist": [
            "Primitive types, interface definitions, and type aliases",
            "Function signatures and optional/default parameters",
            "Generics (<T>) and union/intersection types",
            "TypeScript compiler configuration (tsconfig.json)"
        ],
        "milestone": "Strictly typed API client library with complete type definitions.",
        "beginner_project": "Convert a messy JavaScript calculator into strictly typed TypeScript with zero type errors.",
        "free_resources": [
            {"title": "TypeScript Handbook (Official)", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "provider": "Microsoft"},
            {"title": "Total TypeScript Tutorials", "url": "https://www.totaltypescript.com/tutorials", "provider": "Matt Pocock"}
        ]
    },
    "SQL": {
        "category": "Data & Databases", "prerequisites": [], "difficulty": "Beginner", "estimated_weeks": 2,
        "description": "Declarative querying, window functions, CTEs, aggregation, relational schemas.",
        "plain_english": "The universal language for asking questions to databases. e.g. 'Show me all users who bought an iPhone in Bengaluru last month.'",
        "why_this_skill": "Every company stores data in databases. SQL is the #1 most requested skill across data and software roles.",
        "topics_checklist": [
            "SELECT, WHERE, ORDER BY, and LIMIT clauses",
            "GROUP BY and aggregate functions (COUNT, SUM, AVG)",
            "Table JOINs (INNER JOIN, LEFT JOIN, FULL OUTER JOIN)",
            "Subqueries and Common Table Expressions (WITH CTE AS ...)"
        ],
        "milestone": "Analytical query suite extracting business metrics from raw relational data.",
        "beginner_project": "Query an ecommerce database to find the top 5 highest-spending customer cohorts.",
        "free_resources": [
            {"title": "SQLBolt: Interactive SQL Lessons", "url": "https://sqlbolt.com/", "provider": "SQLBolt"},
            {"title": "Kaggle Intro to SQL", "url": "https://www.kaggle.com/learn/intro-to-sql", "provider": "Kaggle"}
        ]
    },
    "Git": {
        "category": "Foundations", "prerequisites": [], "difficulty": "Beginner", "estimated_weeks": 1,
        "description": "Version control branching strategies, rebasing, merge resolutions, clean histories.",
        "plain_english": "A time-machine for your code. It tracks every change you make so you can collaborate with teammates and never lose work.",
        "why_this_skill": "Every single engineering job on Earth uses Git to share, review, and deploy code.",
        "topics_checklist": [
            "git init, git add, and git commit",
            "git branch, git checkout, and git merge",
            "Connecting to GitHub: git remote, git push, and git pull",
            "Creating Pull Requests and resolving merge conflicts"
        ],
        "milestone": "Multi-branch release workflow with semantic commit conventions.",
        "beginner_project": "Initialize a GitHub repository, create a feature branch, submit a Pull Request, and merge it cleanly.",
        "free_resources": [
            {"title": "Git & GitHub for Beginners", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "provider": "freeCodeCamp"},
            {"title": "Learn Git Branching (Visual Game)", "url": "https://learngitbranching.js.org/", "provider": "Open Source"}
        ]
    },
    "Linux": {
        "category": "Foundations", "prerequisites": [], "difficulty": "Beginner", "estimated_weeks": 2,
        "description": "POSIX shell, file system permissions, process supervision, bash scripting.",
        "plain_english": "The operating system that powers 95%+ of the world's cloud servers, supercomputers, and backend infrastructure.",
        "why_this_skill": "When you deploy code to the cloud (AWS, Docker, Azure), you will interact with Linux via the command line.",
        "topics_checklist": [
            "Navigating files: ls, cd, pwd, mkdir, rm, cp, mv",
            "File permissions (chmod, chown) and superuser privileges (sudo)",
            "Piping commands: grep, cat, head, tail, | (pipe)",
            "Basic bash scripts for automating repetitive terminal tasks"
        ],
        "milestone": "Automated server health & log rotation bash daemon.",
        "beginner_project": "Write a bash script that automatically backs up your project folder into a timestamped zip archive.",
        "free_resources": [
            {"title": "Linux Command Line for Beginners", "url": "https://ubuntu.com/tutorials/command-line-for-beginners", "provider": "Ubuntu"},
            {"title": "OverTheWire: Bandit (Hands-on Game)", "url": "https://overthewire.org/wargames/bandit/", "provider": "OverTheWire"}
        ]
    },
    "Math & Statistics": {
        "category": "Data & AI", "prerequisites": [], "difficulty": "Intermediate", "estimated_weeks": 3,
        "description": "Linear algebra, multivariable calculus, probability distributions, hypothesis testing.",
        "plain_english": "The math behind data. Tells you whether an increase in sales is a real trend or just random coincidence.",
        "why_this_skill": "Machine learning algorithms are just mathematical equations minimizing error. You need basic stats to understand them.",
        "topics_checklist": [
            "Mean, median, mode, standard deviation, and variance",
            "Probability distributions (Normal distribution, p-values)",
            "Linear algebra basics: Vectors, matrices, dot products",
            "Hypothesis testing (A/B testing, null hypothesis)"
        ],
        "milestone": "From-scratch statistical validation notebook testing sample variance & distributions.",
        "beginner_project": "Conduct a statistical A/B test on two marketing campaign conversion rates in a Jupyter Notebook.",
        "free_resources": [
            {"title": "Khan Academy Statistics & Probability", "url": "https://www.khanacademy.org/math/statistics-probability", "provider": "Khan Academy"},
            {"title": "StatQuest Machine Learning Math Playlist", "url": "https://www.youtube.com/@statquest", "provider": "YouTube"}
        ]
    },
    "Networking": {
        "category": "Infrastructure", "prerequisites": [], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "TCP/IP suite, OSI layers, DNS, TLS handshake mechanics, routing protocols.",
        "plain_english": "How computers talk to each other across wires and the internet (IP addresses, ports, routers, security).",
        "why_this_skill": "Crucial for backend developers, DevOps engineers, and security analysts diagnosing connectivity issues.",
        "topics_checklist": [
            "IP addresses, subnets, and MAC addresses",
            "TCP vs UDP protocols and port numbers (80, 443, 22)",
            "DNS lookup process and HTTP/HTTPS request lifecycle",
            "Firewalls, routers, and Network Address Translation (NAT)"
        ],
        "milestone": "Packet inspection and custom HTTP/1.1 request-response parser.",
        "beginner_project": "Inspect real network packets flowing through your computer using Wireshark to see how DNS queries work.",
        "free_resources": [
            {"title": "Computer Networking Course", "url": "https://www.youtube.com/watch?v=IPvYjXCsTg8", "provider": "freeCodeCamp"},
            {"title": "Cisco Intro to Cybersecurity & Networks", "url": "https://www.skillsforall.com/", "provider": "Cisco"}
        ]
    },

    # --- Data & Analytics Track ---
    "Pandas": {
        "category": "Data & Analytics", "prerequisites": ["Python"], "difficulty": "Beginner", "estimated_weeks": 2,
        "description": "Vectorized dataframes, grouping, joins, reshaping, and time-series manipulation.",
        "plain_english": "Like Microsoft Excel, but powered by Python code. Handles millions of rows in seconds.",
        "why_this_skill": "Every data analyst and scientist spends 70% of their time cleaning and filtering data using Pandas.",
        "topics_checklist": ["DataFrames creation and indexing", "Filtering rows and selecting columns", "Handling missing values (.dropna(), .fillna())", "Grouping and aggregating (.groupby())"],
        "milestone": "ETL pipeline cleaning messy tabular data.",
        "beginner_project": "Clean a messy real-world CSV dataset of 10,000 retail sales and calculate monthly profits.",
        "free_resources": [{"title": "Kaggle Pandas Course", "url": "https://www.kaggle.com/learn/pandas", "provider": "Kaggle"}]
    },
    "Data Analysis": {
        "category": "Data & Analytics", "prerequisites": ["Python", "SQL", "Pandas"], "difficulty": "Intermediate", "estimated_weeks": 3,
        "description": "Exploratory data analysis (EDA), anomaly detection, cohort metrics, causal heuristics.",
        "plain_english": "Finding the hidden business story inside raw numbers to help companies make profitable decisions.",
        "why_this_skill": "Companies hire analysts to provide actionable business answers from data.",
        "topics_checklist": ["Exploratory Data Analysis (EDA) workflow", "Detecting outliers and skewness", "Cohort analysis and retention", "Executive storytelling"],
        "milestone": "Comprehensive cohort retention and behavioral attrition report.",
        "beginner_project": "Perform a complete EDA on a public Netflix dataset to discover which genres are growing fastest.",
        "free_resources": [{"title": "Data Analysis with Python", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "provider": "freeCodeCamp"}]
    },
    "Data Visualization": {
        "category": "Data & Analytics", "prerequisites": ["Data Analysis"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Visual hierarchy, interactive dashboards (Tableau / Power BI / Plotly).",
        "plain_english": "Turning confusing spreadsheets into clear, beautiful charts and interactive dashboards.",
        "why_this_skill": "Executives make decisions looking at dashboards, not raw code.",
        "topics_checklist": ["Choosing the right chart", "Building dashboards in Power BI/Tableau", "Interactive Plotly charts", "Color accessibility"],
        "milestone": "Interactive executive dashboard communicating complex macro trends.",
        "beginner_project": "Build an interactive IPL Cricket or sales dashboard with live filters and charts.",
        "free_resources": [{"title": "Power BI Full Course", "url": "https://www.youtube.com/watch?v=TmhQCQr_8CA", "provider": "YouTube"}]
    },
    "Data Modeling": {
        "category": "Data & Databases", "prerequisites": ["SQL"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Dimensional modeling, star/snowflake schemas, normalization, surrogate keys.",
        "plain_english": "Designing how database tables link together so queries run fast without data corruption.",
        "why_this_skill": "Poor data models cause queries to crawl or crash company reporting systems.",
        "topics_checklist": ["Primary and foreign keys", "Normalization (1NF, 2NF, 3NF)", "Star & Snowflake schemas", "Fact vs Dimension tables"],
        "milestone": "Production star schema design for high-throughput ecommerce transactions.",
        "beginner_project": "Design a relational Star Schema for an Uber-like ride-sharing service on dbdiagram.io.",
        "free_resources": [{"title": "Database Design Course", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "provider": "freeCodeCamp"}]
    },
    "Data Warehousing": {
        "category": "Data & Databases", "prerequisites": ["SQL", "Data Modeling"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Cloud warehouses (Snowflake, BigQuery), dbt transformation DAGs, partitioning.",
        "plain_english": "Giant cloud storage systems built specifically to run analytical queries over billions of rows.",
        "why_this_skill": "Modern data teams run on Snowflake, BigQuery, and dbt.",
        "topics_checklist": ["Snowflake & BigQuery architecture", "dbt modeling and transformations", "Partitioning & clustering", "Data testing"],
        "milestone": "Automated dbt modeling pipeline with data testing and lineage docs.",
        "beginner_project": "Build a transformation pipeline in dbt Cloud that cleans raw ecommerce orders.",
        "free_resources": [{"title": "dbt Fundamentals Course", "url": "https://courses.getdbt.com/courses/fundamentals", "provider": "dbt Labs"}]
    },
    "Apache Spark": {
        "category": "Data & Databases", "prerequisites": ["Python", "SQL"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Distributed computing engine for big data processing, PySpark DataFrames.",
        "plain_english": "A lightning-fast engine that distributes heavy data processing across hundreds of computers simultaneously.",
        "why_this_skill": "When data exceeds gigabytes and reaches terabytes, Pandas runs out of memory; Spark is required.",
        "topics_checklist": ["Spark architecture (Driver, Executors)", "PySpark DataFrames and transformations", "Lazy evaluation and actions", "Spark SQL queries"],
        "milestone": "Distributed ETL job processing 100M+ rows.",
        "beginner_project": "Write a PySpark script to calculate aggregate metrics on a multi-gigabyte open dataset.",
        "free_resources": [{"title": "PySpark Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=_C8kWso4ebw", "provider": "freeCodeCamp"}]
    },
    "Airflow / ETL Pipelines": {
        "category": "Data & Databases", "prerequisites": ["Python", "SQL"], "difficulty": "Advanced", "estimated_weeks": 2,
        "description": "Workflow orchestration, DAG scheduling, automated data pipeline triggers.",
        "plain_english": "An automated schedule manager that runs your data scripts at 2:00 AM every night and retries if anything fails.",
        "why_this_skill": "Airflow is the undisputed industry standard for scheduling data pipelines at tech companies.",
        "topics_checklist": ["Defining DAGs in Python code", "Operators (BashOperator, PythonOperator)", "Handling task dependencies and retries", "Monitoring pipeline runs in the Airflow UI"],
        "milestone": "Scheduled multi-stage ETL pipeline with automated slack notifications on failure.",
        "beginner_project": "Build an Apache Airflow DAG that fetches weather data every 6 hours and saves it to a database.",
        "free_resources": [{"title": "Apache Airflow Hands-on Tutorial", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "provider": "Apache.org"}]
    },

    # --- AI & Machine Learning Track ---
    "Scikit-Learn": {
        "category": "Data & AI", "prerequisites": ["Python", "Math & Statistics"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Classical supervised and unsupervised estimators, cross-validation, feature pipelines.",
        "plain_english": "The standard Python library for traditional machine learning algorithms (housing price predictions, classification).",
        "why_this_skill": "90% of real-world business tabular problems are solved with Scikit-Learn.",
        "topics_checklist": ["Train-test split & cross-validation", "Linear/Logistic Regression & Decision Trees", "Feature scaling", "Accuracy, Precision, Recall, F1"],
        "milestone": "Reproducible scikit-learn pipeline predicting customer lifetime value.",
        "beginner_project": "Build a model predicting whether a bank customer will churn based on account activity.",
        "free_resources": [{"title": "Kaggle Machine Learning", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "provider": "Kaggle"}]
    },
    "Machine Learning": {
        "category": "Data & AI", "prerequisites": ["Python", "Math & Statistics", "Scikit-Learn"], "difficulty": "Intermediate", "estimated_weeks": 4,
        "description": "Gradient boosting, loss optimization, regularisation, metric selection.",
        "plain_english": "Teaching computers to recognize patterns from past data and make predictions without hardcoded rules.",
        "why_this_skill": "Powers recommendation feeds, fraud detection, and automated decisions.",
        "topics_checklist": ["Supervised vs Unsupervised learning", "Random Forests & XGBoost", "Hyperparameter tuning (Optuna)", "SHAP model interpretability"],
        "milestone": "Production-grade tabular predictive model with SHAP interpretability.",
        "beginner_project": "Compete in Kaggle's Titanic competition and achieve an accuracy score over 82%.",
        "free_resources": [{"title": "Andrew Ng Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "provider": "Coursera"}]
    },
    "Deep Learning": {
        "category": "Data & AI", "prerequisites": ["Machine Learning"], "difficulty": "Advanced", "estimated_weeks": 4,
        "description": "Feedforward, convolutional, and transformer architectures, backprop dynamics.",
        "plain_english": "Artificial neural networks inspired by the human brain that process images, speech, and text.",
        "why_this_skill": "The foundational technology powering ChatGPT, self-driving cars, and FaceID.",
        "topics_checklist": ["Neurons & activation functions (ReLU)", "Gradient descent and backpropagation", "Convolutional Neural Networks (CNNs)", "Transformers & attention"],
        "milestone": "Custom neural network implementation with manual gradient checks.",
        "beginner_project": "Build an image classifier that distinguishes between cats and dogs with 90%+ accuracy.",
        "free_resources": [{"title": "fast.ai Deep Learning Course", "url": "https://course.fast.ai/", "provider": "fast.ai"}]
    },
    "PyTorch": {
        "category": "Data & AI", "prerequisites": ["Deep Learning"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Tensors, autograd engine, custom Datasets/DataLoaders, distributed training.",
        "plain_english": "The #1 framework used by AI researchers at OpenAI, Meta, and Google to build modern AI models.",
        "why_this_skill": "The industry standard for developing deep learning and generative AI models.",
        "topics_checklist": ["Tensors and GPU acceleration", "Building custom nn.Module models", "Custom Dataset & DataLoader classes", "Training loops and optimizers (AdamW)"],
        "milestone": "Fine-tuned vision or sequence model with mixed-precision training.",
        "beginner_project": "Build a digit recognition model on the MNIST dataset using PyTorch from scratch.",
        "free_resources": [{"title": "PyTorch for Deep Learning in 24 Hours", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "provider": "freeCodeCamp"}]
    },
    "NLP & LLMs": {
        "category": "Data & AI", "prerequisites": ["Deep Learning", "PyTorch"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Attention mechanics, tokenization, parameter-efficient fine-tuning (LoRA), prompt engineering.",
        "plain_english": "Teaching computers to read, summarize, translate, and generate human language (the tech behind ChatGPT).",
        "why_this_skill": "Generative AI and Large Language Models are currently the highest-paying skills in technology.",
        "topics_checklist": ["Tokenization and vector embeddings", "The Transformer architecture & attention", "Prompt engineering & system prompts", "Hugging Face Transformers library"],
        "milestone": "Fine-tuned domain model with LoRA adaptors.",
        "beginner_project": "Build a Python tool that reads a PDF document and generates bullet-point summaries using Hugging Face.",
        "free_resources": [{"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course", "provider": "Hugging Face"}]
    },
    "LangChain & RAG": {
        "category": "Data & AI", "prerequisites": ["Python", "NLP & LLMs"], "difficulty": "Advanced", "estimated_weeks": 2,
        "description": "Retrieval Augmented Generation, vector stores, autonomous agent tooling.",
        "plain_english": "Connecting ChatGPT to your company's private documents so it answers questions without making things up (hallucinating).",
        "why_this_skill": "95% of companies adopting AI today are building RAG applications on private company data.",
        "topics_checklist": ["Document loaders and text chunking strategies", "Generating and indexing vector embeddings", "Building RAG retrieval chains with LangChain", "Evaluating retrieval accuracy"],
        "milestone": "Production RAG assistant with conversational memory.",
        "beginner_project": "Build an AI Q&A bot that reads your personal college syllabus or resume and answers questions accurately.",
        "free_resources": [{"title": "LangChain for LLM Application Development", "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/", "provider": "DeepLearning.AI"}]
    },
    "Vector Databases": {
        "category": "Data & AI", "prerequisites": ["NLP & LLMs"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "High-dimensional similarity search, Pinecone, ChromaDB, HNSW indexing.",
        "plain_english": "Databases designed to find similar pieces of text or images based on meaning rather than exact word matches.",
        "why_this_skill": "The essential memory bank for modern AI and LLM applications.",
        "topics_checklist": ["Cosine similarity vs Euclidean distance", "ChromaDB and Pinecone setup", "Storing and querying document chunks", "Metadata filtering"],
        "milestone": "Semantic search engine indexing 50,000 document chunks.",
        "beginner_project": "Build a semantic search engine where users can search for recipes by mood or flavor profile.",
        "free_resources": [{"title": "Vector Databases for Beginners", "url": "https://www.pinecone.io/learn/vector-database/", "provider": "Pinecone"}]
    },
    "MLOps": {
        "category": "Data & AI", "prerequisites": ["Machine Learning", "Docker"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Experiment tracking (MLflow), model registries, drift monitoring, serving.",
        "plain_english": "DevOps for Machine Learning. Taking a model from a messy Jupyter Notebook and putting it into live 24/7 production.",
        "why_this_skill": "85% of machine learning models fail to reach production without MLOps engineers.",
        "topics_checklist": ["MLflow experiment tracking", "FastAPI model inference endpoints", "Data drift & model degradation monitoring", "Automated retraining triggers"],
        "milestone": "Automated retraining trigger deployed on containerized runners.",
        "beginner_project": "Deploy an ML model behind a FastAPI endpoint inside a Docker container with MLflow logging.",
        "free_resources": [{"title": "Made With ML MLOps", "url": "https://madewithml.com/", "provider": "Made With ML"}]
    },

    # --- Frontend Track ---
    "React": {
        "category": "Frontend", "prerequisites": ["JavaScript"], "difficulty": "Intermediate", "estimated_weeks": 3,
        "description": "Component composition, reactive state hooks, reconciliation, virtual DOM.",
        "plain_english": "The world's most popular frontend library for building modern user interfaces by assembling reusable LEGO-like blocks.",
        "why_this_skill": "Over 60% of frontend developer job openings in India require React proficiency.",
        "topics_checklist": ["JSX syntax and components", "Hooks: useState, useEffect, useRef", "Props and conditional rendering", "API data fetching with loading states"],
        "milestone": "Custom component library with accessible components.",
        "beginner_project": "Build an E-commerce Product Catalog with search, category filtering, and a live shopping cart.",
        "free_resources": [{"title": "React.dev Official Docs", "url": "https://react.dev/learn", "provider": "React Team"}]
    },
    "Tailwind CSS": {
        "category": "Frontend", "prerequisites": ["HTML & CSS"], "difficulty": "Beginner", "estimated_weeks": 1,
        "description": "Utility-first CSS framework for rapid UI styling directly in HTML/JSX.",
        "plain_english": "A modern tool that lets you style beautiful websites directly in your markup without writing separate CSS files.",
        "why_this_skill": "The fastest-growing CSS framework in modern web development.",
        "topics_checklist": ["Utility classes for spacing & typography", "Hover and active interactive states", "Responsive prefixes (sm:, md:, lg:)", "Dark mode configuration"],
        "milestone": "Modern responsive dashboard UI styled entirely with Tailwind.",
        "beginner_project": "Style a complete responsive pricing page with a toggle for monthly vs annual billing.",
        "free_resources": [{"title": "Tailwind CSS Docs", "url": "https://tailwindcss.com/docs", "provider": "Tailwind Labs"}]
    },
    "State Management": {
        "category": "Frontend", "prerequisites": ["React"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Global stores, selector patterns, immutable state transitions (Zustand/Redux).",
        "plain_english": "A central brain for your app so any button on any page can read and update shared data (e.g. login state, cart items).",
        "why_this_skill": "Essential when web applications grow beyond a couple of simple pages.",
        "topics_checklist": ["Local vs global state", "Zustand stores and actions", "Selector subscriptions", "State persistence in localStorage"],
        "milestone": "Collaborative canvas state engine with undo/redo action histories.",
        "beginner_project": "Build a shopping cart where adding items from any page updates the navbar cart badge instantly.",
        "free_resources": [{"title": "Redux Essentials Guide", "url": "https://redux.js.org/tutorials/essentials/part-1-overview-concepts", "provider": "Redux.js.org"}]
    },
    "Next.js": {
        "category": "Frontend", "prerequisites": ["React", "TypeScript"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Server Components, App Router, streaming SSR, edge middleware caching.",
        "plain_english": "A production framework built on top of React that makes websites load instantly with super-fast server rendering.",
        "why_this_skill": "Next.js is the default industry standard for building full-stack production React applications.",
        "topics_checklist": ["Next.js App Router & file-based routing", "Server vs Client Components", "Server-Side Rendering (SSR)", "API route handlers"],
        "milestone": "Full-stack server-rendered editorial platform.",
        "beginner_project": "Build a fast, SEO-friendly personal tech blog that renders posts on the server with Next.js.",
        "free_resources": [{"title": "Learn Next.js Interactive", "url": "https://nextjs.org/learn", "provider": "Vercel"}]
    },
    "Web Performance": {
        "category": "Frontend", "prerequisites": ["JavaScript", "React"], "difficulty": "Advanced", "estimated_weeks": 2,
        "description": "Core Web Vitals (LCP, INP, CLS), bundle splitting, critical rendering path tuning.",
        "plain_english": "Making web pages load in under 1 second so users don't get frustrated and bounce.",
        "why_this_skill": "Google directly penalizes slow websites in search rankings.",
        "topics_checklist": ["Core Web Vitals (LCP, CLS, INP)", "Image optimization & lazy loading", "Code splitting & dynamic imports", "Lighthouse auditing"],
        "milestone": "Sub-second 99-score Lighthouse optimization of a heavy content page.",
        "beginner_project": "Optimize a slow, heavy web application to score 95+ on Google Lighthouse.",
        "free_resources": [{"title": "Web.dev Performance", "url": "https://web.dev/learn/performance", "provider": "Google"}]
    },

    # --- Backend & Systems Track ---
    "Relational Databases": {
        "category": "Backend", "prerequisites": ["SQL"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "PostgreSQL administration, ACID transaction isolation levels, indexing (B-Tree, GIN).",
        "plain_english": "Industrial-strength databases (like PostgreSQL) that safely store user passwords, transactions, and profiles without data loss.",
        "why_this_skill": "PostgreSQL is the #1 database chosen by developers worldwide for modern web backends.",
        "topics_checklist": ["PostgreSQL installation & psql", "ACID transaction guarantees", "Creating indexes to speed searches", "Connecting Python/Node to Postgres"],
        "milestone": "Multi-tenant schema with row-level security and connection pooling.",
        "beginner_project": "Set up a local PostgreSQL database and write Python scripts to insert and query user accounts.",
        "free_resources": [{"title": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/", "provider": "PostgreSQL Tutorial"}]
    },
    "REST APIs": {
        "category": "Backend", "prerequisites": ["Python"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "HTTP status semantics, idempotent mutations, auth (JWT/OAuth2), serialization.",
        "plain_english": "The universal digital bridges connecting mobile apps and websites to server databases.",
        "why_this_skill": "Every mobile app (Instagram, Swiggy) communicates with backend databases via REST APIs.",
        "topics_checklist": ["HTTP methods (GET, POST, PUT, DELETE)", "Status codes (200, 201, 400, 404, 500)", "JSON data serialization", "JWT Authentication"],
        "milestone": "Robust versioned REST API with OpenAPI documentation & rate limiting.",
        "beginner_project": "Build a REST API for a Bookstore where users can create, read, update, and delete book entries.",
        "free_resources": [{"title": "REST APIs for Beginners", "url": "https://www.freecodecamp.org/news/rest-api-tutorial-rest-client-rest-service-and-resources-explained-with-examples/", "provider": "freeCodeCamp"}]
    },
    "FastAPI": {
        "category": "Backend", "prerequisites": ["Python", "REST APIs"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Async/await I/O concurrency, Pydantic type validation, dependency injection.",
        "plain_english": "A lightning-fast Python framework for building backend APIs and serving machine learning models.",
        "why_this_skill": "FastAPI is the top choice for Python backends, microservices, and AI model endpoints.",
        "topics_checklist": ["Routes with @app.get and @app.post", "Pydantic request body validation", "Dependency injection", "Swagger UI at /docs"],
        "milestone": "High-throughput asynchronous microservice handling live websocket subscriptions.",
        "beginner_project": "Build an API that receives an image or text and returns AI model predictions with automated Swagger docs.",
        "free_resources": [{"title": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "provider": "FastAPI"}]
    },
    "Node.js": {
        "category": "Backend", "prerequisites": ["JavaScript", "REST APIs"], "difficulty": "Intermediate", "estimated_weeks": 3,
        "description": "V8 engine internals, event loop libuv worker pool, Express/Fastify.",
        "plain_english": "A runtime that lets you run JavaScript on the server outside the browser.",
        "why_this_skill": "Allows you to write your entire stack (frontend and backend) in one single language: JavaScript.",
        "topics_checklist": ["The Node event loop and async I/O", "Building servers with Express.js", "npm package management", "Connecting to MongoDB/Postgres"],
        "milestone": "Stream-oriented file ingestion service processing multi-gigabyte uploads.",
        "beginner_project": "Build an authentication server that registers users with hashed passwords and issues JWT login tokens.",
        "free_resources": [{"title": "Node.js Course", "url": "https://www.youtube.com/watch?v=Oe421EPjeBE", "provider": "freeCodeCamp"}]
    },
    "Database Optimization": {
        "category": "Backend", "prerequisites": ["Relational Databases"], "difficulty": "Advanced", "estimated_weeks": 2,
        "description": "EXPLAIN ANALYZE interpretation, query rewriting, partial indexes, partition pruning.",
        "plain_english": "Making queries that take 10 seconds run in 5 milliseconds by adding smart indexes and rewriting SQL.",
        "why_this_skill": "As applications grow, unoptimized databases become the #1 bottleneck.",
        "topics_checklist": ["EXPLAIN and EXPLAIN ANALYZE query plans", "B-tree and GIN indexing", "Connection pooling", "Database sharding and replicas"],
        "milestone": "10x query performance tuning on a 100M-row production dataset.",
        "beginner_project": "Generate 1,000,000 dummy records in PostgreSQL, diagnose a slow query with EXPLAIN, and optimize it 20x.",
        "free_resources": [{"title": "Use The Index, Luke!", "url": "https://use-the-index-luke.com/", "provider": "Markus Winand"}]
    },
    "Microservices": {
        "category": "Backend", "prerequisites": ["REST APIs", "Docker"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Decoupled domain boundaries, event-driven messaging, saga patterns, resilience.",
        "plain_english": "Splitting a giant codebase into tiny independent programs (e.g. Payments Service, User Service) that talk via network.",
        "why_this_skill": "Large companies run microservices so dozens of engineering teams can ship code independently.",
        "topics_checklist": ["Monolith vs Microservices tradeoffs", "API Gateway & service discovery", "Async messaging with Kafka", "Circuit breakers"],
        "milestone": "Distributed order processing pipeline with idempotent event consumer.",
        "beginner_project": "Build two microservices (Auth Service & Order Service) that communicate via REST or message queues.",
        "free_resources": [{"title": "Microservices Architecture", "url": "https://martinfowler.com/articles/microservices.html", "provider": "Martin Fowler"}]
    },
    "System Design": {
        "category": "Backend", "prerequisites": ["REST APIs", "Microservices", "Database Optimization"], "difficulty": "Advanced", "estimated_weeks": 4,
        "description": "High-availability architectures, CAP theorem tradeoffs, load balancing, caching tiers.",
        "plain_english": "The architectural art of designing software systems that can handle 100 million users without slowing down or crashing.",
        "why_this_skill": "The primary interview topic for mid and senior engineering roles at top tech companies.",
        "topics_checklist": ["Load balancers", "Caching strategies with Redis", "CAP theorem & consistency", "Designing URL shorteners & notification systems"],
        "milestone": "Comprehensive architecture RFC for a globally distributed platform.",
        "beginner_project": "Write a complete System Architecture blueprint for a URL Shortener (like Bitly) handling 10,000 clicks/sec.",
        "free_resources": [{"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "provider": "GitHub"}]
    },

    # --- Cloud & DevOps Track ---
    "Docker": {
        "category": "DevOps", "prerequisites": ["Linux", "Git"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "OCI container runtime, multi-stage Dockerfiles, image layer caching, networking.",
        "plain_english": "Packages your app and all its dependencies into an isolated container so it runs identically on any computer or server in the world.",
        "why_this_skill": "Eliminates the dreaded excuse: 'It works on my machine!'",
        "topics_checklist": ["Containers vs Virtual Machines", "Writing Dockerfiles (FROM, COPY, RUN, CMD)", "docker build & docker run", "Docker Compose multi-container setups"],
        "milestone": "Minimalist distroless container build for an enterprise microservice.",
        "beginner_project": "Containerize a full-stack Python or React app with a PostgreSQL database using Docker Compose.",
        "free_resources": [{"title": "Docker Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "provider": "TechWorld with Nana"}]
    },
    "CI/CD": {
        "category": "DevOps", "prerequisites": ["Git", "Docker"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Automated lint/test/build pipelines, artifact registries, canary releases.",
        "plain_english": "Automated robots that run tests, build Docker containers, and deploy your code to production whenever you push to GitHub.",
        "why_this_skill": "Companies deploy code multiple times a day using CI/CD pipelines instead of manual copy-pasting.",
        "topics_checklist": ["Continuous Integration vs Continuous Deployment", "Writing GitHub Actions workflow YAML files", "Managing secrets safely in CI", "Automated container builds"],
        "milestone": "GitHub Actions workflow running matrix testing and zero-downtime deployment.",
        "beginner_project": "Create a GitHub Actions workflow that automatically runs unit tests every time someone creates a Pull Request.",
        "free_resources": [{"title": "GitHub Actions Tutorial", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "provider": "TechWorld with Nana"}]
    },
    "Cloud (AWS)": {
        "category": "DevOps", "prerequisites": ["Linux", "Networking"], "difficulty": "Intermediate", "estimated_weeks": 3,
        "description": "VPC topology, IAM least-privilege, compute (EC2/ECS/Lambda), storage (S3).",
        "plain_english": "Renting computing power, databases, and storage from Amazon's massive data centers across the globe.",
        "why_this_skill": "Amazon Web Services (AWS) powers roughly one-third of the entire internet.",
        "topics_checklist": ["IAM permissions & roles", "EC2 servers & AWS Lambda serverless", "S3 object storage buckets", "VPCs, security groups, & routing"],
        "milestone": "Secure multi-tier VPC network with private subnets and managed NAT gateways.",
        "beginner_project": "Deploy a web app on an AWS EC2 instance behind an SSL certificate with an S3 bucket for file uploads.",
        "free_resources": [{"title": "AWS Cloud Practitioner Course", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "provider": "freeCodeCamp"}]
    },
    "Kubernetes": {
        "category": "DevOps", "prerequisites": ["Docker", "Linux"], "difficulty": "Advanced", "estimated_weeks": 4,
        "description": "Pod scheduling, ReplicaSets, Ingress controllers, Helm charts, stateful sets.",
        "plain_english": "An automated traffic controller that manages hundreds of Docker containers, auto-scaling them when traffic spikes and restarting them if they crash.",
        "why_this_skill": "The de-facto operating system of cloud infrastructure at modern scale.",
        "topics_checklist": ["Control Plane & Nodes architecture", "Pods, Deployments, ReplicaSets", "Services (ClusterIP, NodePort) & Ingress", "ConfigMaps, Secrets, & Volumes"],
        "milestone": "Production Kubernetes deployment with Horizontal Pod Autoscaling and TLS ingress.",
        "beginner_project": "Set up a local Minikube cluster and deploy a multi-pod web app with automatic scaling.",
        "free_resources": [{"title": "Kubernetes Course for Beginners", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "provider": "TechWorld with Nana"}]
    },
    "Terraform": {
        "category": "DevOps", "prerequisites": ["Cloud (AWS)", "Linux"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Declarative HCL, state management, remote backends, reusable module design.",
        "plain_english": "Creating cloud servers, networks, and databases using readable code files instead of clicking buttons in the AWS console.",
        "why_this_skill": "Allows you to create, clone, or destroy an entire cloud infrastructure setup in 60 seconds with one command.",
        "topics_checklist": ["HCL syntax basics", "terraform init, plan, apply, destroy", "Managing state files (S3 backend)", "Writing reusable modules"],
        "milestone": "Modular Infrastructure-as-Code suite provisioning an end-to-end cloud environment.",
        "beginner_project": "Write a Terraform script that provisions an AWS VPC, EC2 instance, and S3 bucket automatically.",
        "free_resources": [{"title": "Terraform Course for Beginners", "url": "https://www.youtube.com/watch?v=SLB_c_wgJ24", "provider": "freeCodeCamp"}]
    },
    "Monitoring & Observability": {
        "category": "DevOps", "prerequisites": ["Docker", "Linux"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Golden signals (latency, traffic, errors, saturation), Prometheus metrics, Grafana.",
        "plain_english": "Heart monitors for your servers. Alerts engineers on their phones before users notice an outage.",
        "why_this_skill": "Essential for diagnosing server issues and maintaining 99.99% uptime.",
        "topics_checklist": ["4 Golden Signals (Latency, Traffic, Errors, Saturation)", "Prometheus metrics collection", "Building Grafana dashboards", "Centralized logging with Loki/ELK"],
        "milestone": "Grafana operational dashboard with automated alert thresholds.",
        "beginner_project": "Deploy Prometheus and Grafana on a server to graph live CPU, RAM, and network traffic.",
        "free_resources": [{"title": "Prometheus & Grafana Masterclass", "url": "https://www.youtube.com/watch?v=9TYX7HKtr3I", "provider": "TechWorld with Nana"}]
    },

    # --- Cybersecurity Track ---
    "Operating Systems": {
        "category": "Security", "prerequisites": ["Linux"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Kernel architecture, memory management, system calls, privilege rings.",
        "plain_english": "Understanding how software speaks to the physical computer chip, manages memory, and handles privileges.",
        "why_this_skill": "Security vulnerabilities exploit gaps in OS memory and kernel privileges.",
        "topics_checklist": ["User space vs Kernel space", "Processes and CPU scheduling", "Virtual memory, stack vs heap", "System calls (syscalls)"],
        "milestone": "Process audit monitor tracking unauthorized privilege escalations.",
        "beginner_project": "Write a Python or C program that inspects running processes and flags processes running as root.",
        "free_resources": [{"title": "Operating Systems Course", "url": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRitWSE_AyyyHKEl423UddkM", "provider": "Neso Academy"}]
    },
    "Cryptography": {
        "category": "Security", "prerequisites": ["Math & Statistics"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "Symmetric vs asymmetric ciphers, SHA hashing, PKI infrastructure, digital signatures.",
        "plain_english": "The mathematical science of locking information so only the intended recipient with the secret key can unlock it.",
        "why_this_skill": "Keeps bank transactions, credit card numbers, and confidential passwords secure from hackers.",
        "topics_checklist": ["Hashing (SHA-256) vs Encryption vs Encoding", "Symmetric AES-256 encryption", "Asymmetric RSA & ECC key pairs", "PKI & SSL/TLS certificates"],
        "milestone": "Custom cryptographic envelope implementation with key rotation.",
        "beginner_project": "Build an encrypted messaging tool in Python where messages are encrypted using AES-256 and signed with RSA keys.",
        "free_resources": [{"title": "Stanford Cryptography Course", "url": "https://www.coursera.org/learn/crypto", "provider": "Coursera / Stanford"}]
    },
    "Network Security": {
        "category": "Security", "prerequisites": ["Networking"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Stateful firewalls, packet filtering, IDS/IPS heuristics, VPN tunnels, zero-trust.",
        "plain_english": "Defending company internal networks against unauthorized access, port scans, and denial-of-service (DDoS) attacks.",
        "why_this_skill": "90% of cyber breaches begin with unauthorized access through exposed network ports.",
        "topics_checklist": ["Stateful firewalls & iptables", "Intrusion Detection (Snort, Suricata)", "VPN tunnels (WireGuard)", "Zero Trust Network principles"],
        "milestone": "Hardened network perimeter configuration with intrusion detection rules.",
        "beginner_project": "Set up a local firewall using iptables or ufw that blocks all incoming traffic except SSH and HTTPS.",
        "free_resources": [{"title": "TryHackMe: Network Security", "url": "https://tryhackme.com/", "provider": "TryHackMe"}]
    },
    "Security Operations": {
        "category": "Security", "prerequisites": ["Linux", "Networking", "Operating Systems"], "difficulty": "Intermediate", "estimated_weeks": 3,
        "description": "SOC tier triage, incident response lifecycle (NIST), memory forensics, chain of custody.",
        "plain_english": "The 24/7 emergency control room for cybersecurity. Detecting cyberattacks in real-time and kicking hackers off the network.",
        "why_this_skill": "The primary entry-level job title for cybersecurity professionals (SOC Analyst).",
        "topics_checklist": ["SOC triage lifecycle & alert severity", "NIST Incident Response framework", "Phishing & malware triage", "Digital forensics collection"],
        "milestone": "Post-incident forensic root cause report and remediation runbook.",
        "beginner_project": "Investigate a simulated cyber breach report, extract malicious IP addresses, and write an incident triage document.",
        "free_resources": [{"title": "TryHackMe: SOC Level 1 Path", "url": "https://tryhackme.com/path/outline/soclevel1", "provider": "TryHackMe"}]
    },
    "SIEM": {
        "category": "Security", "prerequisites": ["Security Operations"], "difficulty": "Intermediate", "estimated_weeks": 2,
        "description": "Log correlation, detection engineering, Splunk/Elastic querying, sigma rules.",
        "plain_english": "A central software hub that ingests billions of server log messages and raises an alarm when suspicious activity is detected.",
        "why_this_skill": "Every enterprise security team relies on Splunk or Microsoft Sentinel to spot hackers.",
        "topics_checklist": ["Log ingestion from Windows/Linux event logs", "Splunk SPL search queries", "Writing detection rules for brute force attacks", "SOC monitoring dashboards"],
        "milestone": "Custom behavioral detection rule catching lateral movement attempts.",
        "beginner_project": "Install Splunk Free on your machine, ingest web server logs, and write a query to detect failed login attempts.",
        "free_resources": [{"title": "Splunk Free Fundamentals", "url": "https://www.splunk.com/en_us/training/free-courses/splunk-fundamentals-1.html", "provider": "Splunk"}]
    },
    "Penetration Testing": {
        "category": "Security", "prerequisites": ["Network Security", "Linux", "Python"], "difficulty": "Advanced", "estimated_weeks": 4,
        "description": "Reconnaissance, vulnerability exploitation, privilege escalation, Metasploit, report writing.",
        "plain_english": "Ethical hacking: hacking into your own company's systems with permission to find vulnerabilities before malicious criminals do.",
        "why_this_skill": "One of the most thrilling and respected specializations in the technology sector.",
        "topics_checklist": ["Reconnaissance with Nmap & Gobuster", "Exploiting CVE vulnerabilities with Metasploit", "Linux & Windows privilege escalation", "Remediation reporting"],
        "milestone": "Full penetration assessment whitepaper targeting an isolated vulnerable sandbox.",
        "beginner_project": "Successfully crack and gain root access to 3 beginner machines on Hack The Box or TryHackMe.",
        "free_resources": [{"title": "Practical Ethical Hacking Course", "url": "https://www.youtube.com/watch?v=3Kq1MIfTWCE", "provider": "The Cyber Mentor"}]
    },
    "Application Security": {
        "category": "Security", "prerequisites": ["REST APIs", "Network Security"], "difficulty": "Advanced", "estimated_weeks": 3,
        "description": "OWASP Top 10 mitigations, SAST/DAST pipeline gates, secure authentication patterns.",
        "plain_english": "Fixing code vulnerabilities (like SQL Injection or broken access controls) in web applications before releasing to customers.",
        "why_this_skill": "Modern companies prefer preventing bugs during development rather than cleaning up after a public breach.",
        "topics_checklist": ["The OWASP Top 10 web vulnerabilities", "SQL Injection & XSS prevention", "Broken Object Authorization (IDOR)", "Automated code scanners in CI/CD"],
        "milestone": "Security code audit uncovering and patching injection & IDOR vulnerabilities.",
        "beginner_project": "Complete the first 10 free interactive vulnerability labs on PortSwigger Web Security Academy.",
        "free_resources": [{"title": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security", "provider": "PortSwigger"}]
    },
    "Threat Modeling": {
        "category": "Security", "prerequisites": ["Security Operations", "Application Security"], "difficulty": "Advanced", "estimated_weeks": 2,
        "description": "STRIDE threat modeling, attack trees, risk mitigation matrix, architecture reviews.",
        "plain_english": "Analyzing a system's blueprint before building it: 'What could go wrong? Who might attack it? How do we prevent it?'",
        "why_this_skill": "Saves millions of dollars by identifying design flaws before a single line of code is written.",
        "topics_checklist": ["The STRIDE threat model", "Data Flow Diagrams for security boundaries", "Risk scoring matrices", "Security architecture reviews"],
        "milestone": "Formal STRIDE threat model document for an enterprise financial checkout system.",
        "beginner_project": "Conduct a formal STRIDE threat analysis for an online banking mobile login screen.",
        "free_resources": [{"title": "OWASP Threat Modeling Project", "url": "https://owasp.org/www-community/Threat_Modeling", "provider": "OWASP"}]
    }
}


# ---------------------------------------------------------------------------
# Alias Mapping Dictionary
# ---------------------------------------------------------------------------

SKILL_ALIAS_MAP: dict[str, str] = {
    "python": "Python", "py": "Python", "python3": "Python", "python 3": "Python",
    "javascript": "JavaScript", "js": "JavaScript", "java script": "JavaScript", "es6+": "JavaScript", "es6": "JavaScript",
    "typescript": "TypeScript", "ts": "TypeScript", "type script": "TypeScript",
    "go": "Go (Golang)", "golang": "Go (Golang)", "go (golang)": "Go (Golang)", "go lang": "Go (Golang)",
    "java": "Java", "core java": "Java", "java 17/21": "Java",
    "html & css": "HTML & CSS", "html": "HTML & CSS", "css": "HTML & CSS", "html5/css3": "HTML & CSS", "semantic html": "HTML & CSS", "css / html": "HTML & CSS", "html/css": "HTML & CSS",
    "sql": "SQL", "structured query language": "SQL", "ansi sql": "SQL", "sql server": "SQL",
    "git": "Git", "github": "Git", "gitlab": "Git", "git / github": "Git",
    "linux": "Linux", "ubuntu / linux": "Linux", "unix": "Linux", "bash / linux": "Linux", "bash": "Linux", "shell scripting": "Linux",
    "math & statistics": "Math & Statistics", "statistics": "Math & Statistics", "applied mathematics": "Math & Statistics", "probability & stats": "Math & Statistics", "math": "Math & Statistics", "stats": "Math & Statistics",
    "networking": "Networking", "tcp/ip": "Networking", "computer networking": "Networking", "dns / http protocols": "Networking",
    "react": "React", "react.js": "React", "reactjs": "React",
    "next.js": "Next.js", "nextjs": "Next.js", "next": "Next.js", "next js": "Next.js",
    "vue.js": "Vue.js", "vue": "Vue.js", "vuejs": "Vue.js",
    "tailwind css": "Tailwind CSS", "tailwind": "Tailwind CSS", "tailwindcss": "Tailwind CSS",
    "state management": "State Management", "redux / zustand": "State Management", "redux": "State Management", "zustand": "State Management",
    "web performance": "Web Performance", "core web vitals": "Web Performance", "frontend performance": "Web Performance",
    "rest apis": "REST APIs", "restful apis": "REST APIs", "api design": "REST APIs", "rest": "REST APIs",
    "fastapi": "FastAPI", "fast api": "FastAPI",
    "node.js": "Node.js", "node": "Node.js", "nodejs": "Node.js",
    "express.js": "Express.js", "express": "Express.js", "expressjs": "Express.js",
    "django": "Django", "django rest framework": "Django",
    "spring boot": "Spring Boot", "springboot": "Spring Boot", "spring": "Spring Boot",
    "relational databases": "Relational Databases", "postgresql": "Relational Databases", "postgres": "Relational Databases", "postgres db": "Relational Databases", "mysql / postgres": "Relational Databases", "mysql": "Relational Databases",
    "nosql databases": "NoSQL Databases", "mongodb": "NoSQL Databases", "mongo": "NoSQL Databases",
    "redis": "Redis", "redis cache": "Redis", "in-memory caching": "Redis",
    "message queues": "Message Queues", "kafka": "Message Queues", "apache kafka": "Message Queues", "rabbitmq": "Message Queues",
    "database optimization": "Database Optimization", "query tuning": "Database Optimization", "indexing & sharding": "Database Optimization",
    "microservices": "Microservices", "microservices architecture": "Microservices", "service-oriented arch": "Microservices",
    "system design": "System Design", "system architecture": "System Design", "distributed systems design": "System Design", "distributed systems": "System Design",
    "pandas": "Pandas", "pandas/numpy": "Pandas", "numpy/pandas": "Pandas",
    "data analysis": "Data Analysis", "exploratory data analysis": "Data Analysis", "eda": "Data Analysis",
    "data visualization": "Data Visualization", "data viz": "Data Visualization", "tableau": "Data Visualization", "looker": "Data Visualization", "tableau / looker": "Data Visualization", "powerbi / viz": "Data Visualization", "power bi": "Data Visualization", "powerbi": "Data Visualization",
    "data modeling": "Data Modeling", "schema design": "Data Modeling", "dimensional modeling": "Data Modeling",
    "data warehousing": "Data Warehousing", "snowflake": "Data Warehousing", "bigquery": "Data Warehousing", "snowflake / bigquery": "Data Warehousing", "dbt": "Data Warehousing",
    "apache spark": "Apache Spark", "spark": "Apache Spark", "pyspark": "Apache Spark",
    "airflow / etl pipelines": "Airflow / ETL Pipelines", "apache airflow": "Airflow / ETL Pipelines", "airflow": "Airflow / ETL Pipelines", "etl pipelines": "Airflow / ETL Pipelines",
    "scikit-learn": "Scikit-Learn", "sklearn": "Scikit-Learn", "scikit learn": "Scikit-Learn",
    "machine learning": "Machine Learning", "ml": "Machine Learning", "statistical learning": "Machine Learning",
    "deep learning": "Deep Learning", "dl": "Deep Learning", "neural networks": "Deep Learning",
    "pytorch": "PyTorch", "torch": "PyTorch",
    "tensorflow": "TensorFlow", "tensorflow": "TensorFlow", "tf": "TensorFlow", "keras": "TensorFlow",
    "computer vision": "Computer Vision", "opencv": "Computer Vision", "cv": "Computer Vision",
    "nlp & llms": "NLP & LLMs", "llms": "NLP & LLMs", "nlp": "NLP & LLMs", "natural language processing": "NLP & LLMs", "langchain / llms": "NLP & LLMs",
    "langchain & rag": "LangChain & RAG", "langchain": "LangChain & RAG", "rag": "LangChain & RAG",
    "vector databases": "Vector Databases", "pinecone": "Vector Databases", "chromadb": "Vector Databases", "vector db": "Vector Databases",
    "mlops": "MLOps", "mlflow / model registry": "MLOps", "model deployment": "MLOps",
    "docker": "Docker", "docker containerization": "Docker", "docker-ce": "Docker", "containers": "Docker",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes", "kube": "Kubernetes",
    "ci/cd": "CI/CD", "ci cd": "CI/CD", "cicd": "CI/CD", "continuous integration": "CI/CD", "github actions / ci": "CI/CD", "github actions": "CI/CD",
    "cloud (aws)": "Cloud (AWS)", "aws": "Cloud (AWS)", "amazon web services": "Cloud (AWS)", "aws cloud": "Cloud (AWS)", "cloud": "Cloud (AWS)",
    "cloud (azure / gcp)": "Cloud (Azure / GCP)", "azure": "Cloud (Azure / GCP)", "gcp": "Cloud (Azure / GCP)", "google cloud": "Cloud (Azure / GCP)",
    "terraform": "Terraform", "tf": "Terraform", "iac (terraform)": "Terraform", "iac": "Terraform",
    "ansible": "Ansible", "configuration management": "Ansible",
    "monitoring & observability": "Monitoring & Observability", "prometheus / grafana": "Monitoring & Observability", "datadog": "Monitoring & Observability", "observability": "Monitoring & Observability", "grafana": "Monitoring & Observability",
    "operating systems": "Operating Systems", "os internals": "Operating Systems", "kernel / os": "Operating Systems",
    "cryptography": "Cryptography", "crypto": "Cryptography", "encryption / pki": "Cryptography", "applied cryptography": "Cryptography",
    "network security": "Network Security", "netsec": "Network Security", "firewalls / ids": "Network Security", "network defense": "Network Security",
    "security operations": "Security Operations", "secops": "Security Operations", "incident response": "Security Operations", "soc": "Security Operations",
    "siem": "SIEM", "splunk / siem": "SIEM", "splunk": "SIEM", "security information & event mgmt": "SIEM",
    "penetration testing": "Penetration Testing", "pen testing": "Penetration Testing", "pentesting": "Penetration Testing", "ethical hacking": "Penetration Testing",
    "application security": "Application Security", "appsec": "Application Security", "owasp top 10": "Application Security", "secure coding": "Application Security",
    "threat modeling": "Threat Modeling", "stride / threat analysis": "Threat Modeling",
    "wireshark": "Wireshark", "packet analysis": "Wireshark",
    "iam (identity & access)": "IAM (Identity & Access)", "iam": "IAM (Identity & Access)", "identity management": "IAM (Identity & Access)"
}


# ---------------------------------------------------------------------------
# Data Cleaning & Normalization
# ---------------------------------------------------------------------------

def normalize_skill_token(raw_token: str) -> str | None:
    cleaned = raw_token.strip().lower()
    if not cleaned or cleaned in {"n/a", "none specified", "none", "null"}:
        return None
    return SKILL_ALIAS_MAP.get(cleaned, None)


def clean_job_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    initial_count = len(df)
    
    valid_mask = df["role"].notna() & (df["role"].str.strip() != "") & \
                 df["skills"].notna() & (df["skills"].str.strip() != "")
    df_valid = df[valid_mask].copy()
    dropped_empty = initial_count - len(df_valid)
    
    before_dedup = len(df_valid)
    df_valid["clean_company"] = df_valid["company"].astype(str).str.strip().str.lower()
    df_valid["clean_role"] = df_valid["role"].astype(str).str.strip()
    df_valid["clean_skills_key"] = df_valid["skills"].astype(str).str.strip().str.lower()
    
    df_dedup = df_valid.drop_duplicates(subset=["clean_company", "clean_role", "clean_skills_key"]).copy()
    dropped_duplicates = before_dedup - len(df_dedup)
    
    def parse_skills(raw_skills: str) -> list[str]:
        tokens = [t.strip() for t in str(raw_skills).split(",")]
        canonical = []
        for token in tokens:
            norm = normalize_skill_token(token)
            if norm and norm in SKILLS_GRAPH and norm not in canonical:
                canonical.append(norm)
        return canonical
        
    df_dedup["canonical_skills"] = df_dedup["skills"].apply(parse_skills)
    df_final = df_dedup[df_dedup["canonical_skills"].apply(len) > 0].copy()
    dropped_no_skills = len(df_dedup) - len(df_final)
    
    audit_summary = {
        "raw_count": initial_count,
        "clean_count": len(df_final),
        "dropped_missing_fields": dropped_empty,
        "dropped_duplicates": dropped_duplicates,
        "dropped_unrecognized": dropped_no_skills,
        "total_filtered": initial_count - len(df_final)
    }
    
    return df_final, audit_summary


# ---------------------------------------------------------------------------
# Role Profiling Engine
# ---------------------------------------------------------------------------

def compute_role_profiles(cleaned_df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    profiles = {}
    grouped = cleaned_df.groupby("clean_role")
    
    for role_name, group in grouped:
        total_listings = len(group)
        skill_counts: dict[str, int] = {}
        
        for skill_list in group["canonical_skills"]:
            for skill in skill_list:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
        skill_metrics = []
        for skill, count in skill_counts.items():
            freq = count / total_listings
            if freq >= 0.50:
                tier = "Core Requirement"
                importance_score = freq * 1.2
            elif freq >= 0.25:
                tier = "Key Competency"
                importance_score = freq * 1.0
            else:
                tier = "High-Value Complement"
                importance_score = freq * 0.8
                
            skill_info = SKILLS_GRAPH.get(skill, {})
            skill_metrics.append({
                "skill": skill,
                "count": count,
                "frequency": freq,
                "frequency_pct": round(freq * 100, 1),
                "importance_score": round(importance_score, 3),
                "tier": tier,
                "category": skill_info.get("category", "General"),
                "difficulty": skill_info.get("difficulty", "Intermediate"),
                "estimated_weeks": skill_info.get("estimated_weeks", 2)
            })
            
        skill_metrics.sort(key=lambda x: (x["importance_score"], x["frequency"]), reverse=True)
        
        inr_bench = ROLE_INR_BENCHMARKS.get(role_name, {
            "range": "₹10.0 - ₹24.0 LPA",
            "entry": "₹7.0 - ₹11.0 LPA",
            "senior": "₹18.0 - ₹35.0 LPA",
            "hourly": "₹2,000 - ₹4,500/hr"
        })
        
        free_res = ROLE_FREE_RESOURCES.get(role_name, [])
        
        profiles[role_name] = {
            "role": role_name,
            "total_listings": total_listings,
            "skills": skill_metrics,
            "skill_lookup": {m["skill"]: m for m in skill_metrics},
            "rep_salary": inr_bench["range"],
            "inr_benchmark": inr_bench,
            "free_resources": free_res,
            "top_core_skills": [m["skill"] for m in skill_metrics if m["frequency"] >= 0.35][:7]
        }
        
    return profiles


# ---------------------------------------------------------------------------
# Path Engine: Prerequisite Resolution & Topological Sort
# ---------------------------------------------------------------------------

def calculate_prerequisite_depth(skill: str, graph: dict[str, dict[str, Any]], visited: set[str] | None = None) -> int:
    if visited is None:
        visited = set()
    if skill in visited:
        return 0
    visited.add(skill)
    
    prereqs = graph.get(skill, {}).get("prerequisites", [])
    if not prereqs:
        return 0
    return 1 + max(calculate_prerequisite_depth(p, graph, visited.copy()) for p in prereqs)


def generate_learning_path(
    current_skills: set[str],
    target_role: str,
    role_profiles: dict[str, dict[str, Any]],
    graph: dict[str, dict[str, Any]] = SKILLS_GRAPH
) -> dict[str, Any]:
    if target_role not in role_profiles:
        raise ValueError(f"Unknown target role: {target_role}")
        
    profile = role_profiles[target_role]
    role_skills_metrics = profile["skills"]
    
    target_role_skills_set = set()
    for m in role_skills_metrics:
        if m["frequency"] >= 0.22 or len(target_role_skills_set) < 7:
            target_role_skills_set.add(m["skill"])
            
    total_role_weight = 0.0
    acquired_role_weight = 0.0
    for m in role_skills_metrics:
        if m["skill"] in target_role_skills_set:
            weight = m["importance_score"]
            total_role_weight += weight
            if m["skill"] in current_skills:
                acquired_role_weight += weight
                
    match_percentage = int(round((acquired_role_weight / total_role_weight * 100))) if total_role_weight > 0 else 0
    match_percentage = min(100, max(0, match_percentage))
    
    missing_target_skills = target_role_skills_set - current_skills
    needed_to_learn: set[str] = set()
    
    def resolve_prereqs(skill: str):
        if skill in current_skills:
            return
        needed_to_learn.add(skill)
        prereqs = graph.get(skill, {}).get("prerequisites", [])
        for p in prereqs:
            if p not in current_skills:
                resolve_prereqs(p)
                
    for s in missing_target_skills:
        resolve_prereqs(s)
        
    if not needed_to_learn:
        return {
            "status": "QUALIFIED",
            "target_role": target_role,
            "match_percentage": 100,
            "total_weeks": 0,
            "current_skills": current_skills,
            "target_skills": target_role_skills_set,
            "path_steps": [],
            "acquired_count": len(target_role_skills_set),
            "missing_count": 0,
            "message": "You currently satisfy all core requirements for this role."
        }
        
    adj: dict[str, list[str]] = {s: [] for s in needed_to_learn}
    in_degree: dict[str, int] = {s: 0 for s in needed_to_learn}
    
    for s in needed_to_learn:
        prereqs = graph.get(s, {}).get("prerequisites", [])
        for p in prereqs:
            if p in needed_to_learn:
                adj[p].append(s)
                in_degree[s] += 1
                
    zero_in_degree = [s for s in needed_to_learn if in_degree[s] == 0]
    ordered_skills: list[str] = []
    
    def tie_breaker_key(s: str):
        depth = calculate_prerequisite_depth(s, graph)
        importance = profile["skill_lookup"].get(s, {}).get("importance_score", 0.1)
        return (depth, -importance)
        
    while zero_in_degree:
        zero_in_degree.sort(key=tie_breaker_key)
        current = zero_in_degree.pop(0)
        ordered_skills.append(current)
        
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)
                
    if len(ordered_skills) < len(needed_to_learn):
        remaining = needed_to_learn - set(ordered_skills)
        ordered_skills.extend(sorted(remaining, key=tie_breaker_key))
        
    total_weeks = 0
    path_steps = []
    total_steps_count = len(ordered_skills)
    
    for idx, skill in enumerate(ordered_skills, 1):
        info = graph.get(skill, {})
        role_metric = profile["skill_lookup"].get(skill)
        
        weeks = info.get("estimated_weeks", 2)
        total_weeks += weeks
        
        is_direct_target = skill in target_role_skills_set
        prereqs = info.get("prerequisites", [])
        satisfied_prereqs = [p for p in prereqs if p in current_skills or p in ordered_skills[:idx-1]]
        
        rel_position = idx / max(total_steps_count, 1)
        if rel_position <= 0.35:
            phase_num = 1
            phase_name = "Phase 1: Absolute Foundations"
            phase_color = "#2E5C3B"
        elif rel_position <= 0.70:
            phase_num = 2
            phase_name = "Phase 2: Core Engineering & Frameworks"
            phase_color = "#B44A32"
        else:
            phase_num = 3
            phase_name = "Phase 3: Production Specialization & Scale"
            phase_color = "#1E2B37"
            
        if is_direct_target:
            freq_pct = role_metric["frequency_pct"] if role_metric else "Core"
            reason = f"Primary Market Requirement ({freq_pct}% demand across listings)"
        else:
            downstream = [s for s in needed_to_learn if skill in graph.get(s, {}).get("prerequisites", [])]
            reason = f"Mandatory Foundation unlocking: {', '.join(downstream[:2])}"
            
        path_steps.append({
            "step_number": idx,
            "phase_num": phase_num,
            "phase_name": phase_name,
            "phase_color": phase_color,
            "skill": skill,
            "category": info.get("category", "General"),
            "difficulty": info.get("difficulty", "Beginner"),
            "estimated_weeks": weeks,
            "cumulative_weeks": total_weeks,
            "description": info.get("description", ""),
            "plain_english": info.get("plain_english", info.get("description", "")),
            "why_this_skill": info.get("why_this_skill", "Essential stepping stone for subsequent milestones."),
            "topics_checklist": info.get("topics_checklist", [
                "Understand fundamental concepts and vocabulary",
                "Complete hands-on interactive exercises",
                "Build a small working code example",
                "Push verified solution to GitHub"
            ]),
            "milestone": info.get("milestone", ""),
            "beginner_project": info.get("beginner_project", info.get("milestone", "")),
            "free_resources": info.get("free_resources", []),
            "is_direct_target": is_direct_target,
            "reason": reason,
            "prerequisites": prereqs,
            "satisfied_prereqs": satisfied_prereqs
        })
        
    return {
        "status": "IN_PROGRESS",
        "target_role": target_role,
        "match_percentage": match_percentage,
        "total_weeks": total_weeks,
        "current_skills": current_skills,
        "target_skills": target_role_skills_set,
        "path_steps": path_steps,
        "acquired_count": len(target_role_skills_set.intersection(current_skills)),
        "missing_count": len(path_steps),
        "message": f"Generated {len(path_steps)} optimal learning steps spanning {total_weeks} weeks."
    }


# ---------------------------------------------------------------------------
# Beginner-Friendly Graphviz DOT Generation (Phased Subgraphs & Simplified Edges)
# ---------------------------------------------------------------------------

def generate_graphviz_dot(
    current_skills: set[str],
    target_role_skills: set[str],
    path_steps: list[dict[str, Any]],
    graph: dict[str, dict[str, Any]] = SKILLS_GRAPH
) -> str:
    """
    Generate an uncluttered, beginner-friendly Graphviz DOT diagram.
    Organizes nodes into structured visual clusters (Foundations -> Core -> Target),
    removes redundant transitive bypass arrows, and styles clearly.
    """
    path_skill_names = {step["skill"]: step["step_number"] for step in path_steps}
    relevant_skills = set(current_skills) | set(target_role_skills) | set(path_skill_names.keys())
    
    # 1. Classify nodes into clear learning phases for beginners
    phase_0_have = []
    phase_1_foundations = []
    phase_2_core = []
    phase_3_target = []
    
    total_steps = len(path_steps)
    for skill in relevant_skills:
        if skill in current_skills:
            phase_0_have.append(skill)
        elif skill in path_skill_names:
            step_num = path_skill_names[skill]
            rel_pos = step_num / max(total_steps, 1)
            if rel_pos <= 0.40:
                phase_1_foundations.append(skill)
            elif rel_pos <= 0.75:
                phase_2_core.append(skill)
            else:
                phase_3_target.append(skill)
        elif skill in target_role_skills:
            phase_3_target.append(skill)
        else:
            phase_1_foundations.append(skill)

    dot_lines = [
        'digraph ChronoSkill {',
        '  graph [',
        '    bgcolor="transparent",',
        '    rankdir="LR",',
        '    concentrate=true,',  # Combines parallel edges to reduce spaghetti crossing
        '    nodesep="0.45",',
        '    ranksep="0.8",',
        '    fontname="Plus Jakarta Sans, Helvetica, Arial, sans-serif",',
        '    fontsize="11",',
        '    compound=true',
        '  ];',
        '  node [',
        '    shape="box",',
        '    style="filled,rounded",',
        '    fontname="Plus Jakarta Sans, Helvetica, Arial, sans-serif",',
        '    fontsize="10",',
        '    penwidth="1.2",',
        '    margin="0.16,0.11"',
        '  ];',
        '  edge [',
        '    color="#C8C2B7",',
        '    penwidth="1.0",',
        '    arrowsize="0.65",',
        '    arrowhead="vee"',
        '  ];'
    ]

    def render_node(skill: str) -> str:
        step_num = path_skill_names.get(skill)
        if skill in current_skills:
            label = f"✓ {skill}\\n(Completed)"
            fillcolor = "#E5EBE3"
            color = "#2E5C3B"
            fontcolor = "#1E3B27"
        elif step_num is not None:
            prefix = f"0{step_num}" if step_num < 10 else f"{step_num}"
            label = f"Step {prefix}\\n{skill}"
            fillcolor = "#FAF1ED"
            color = "#B44A32"
            fontcolor = "#141413"
        elif skill in target_role_skills:
            label = f"★ {skill}\\n(Target)"
            fillcolor = "#141413"
            color = "#141413"
            fontcolor = "#F5F3EF"
        else:
            label = skill
            fillcolor = "#EFECE6"
            color = "#DDD8CF"
            fontcolor = "#777169"
        return f'    "{skill}" [label="{label}", fillcolor="{fillcolor}", color="{color}", fontcolor="{fontcolor}"];'

    # Subgraph 0: Already Have
    if phase_0_have:
        dot_lines.append('  subgraph cluster_0 {')
        dot_lines.append('    label="✅ Skills You Already Have";')
        dot_lines.append('    style="dashed,rounded"; color="#2E5C3B"; fontcolor="#2E5C3B"; fontsize="10";')
        for s in phase_0_have:
            dot_lines.append(render_node(s))
        dot_lines.append('  }')

    # Subgraph 1: Foundations
    if phase_1_foundations:
        dot_lines.append('  subgraph cluster_1 {')
        dot_lines.append('    label="🌱 Stage 1: Foundations (Start Here)";')
        dot_lines.append('    style="dashed,rounded"; color="#8A857C"; fontcolor="#5E5A54"; fontsize="10";')
        for s in phase_1_foundations:
            dot_lines.append(render_node(s))
        dot_lines.append('  }')

    # Subgraph 2: Core Engineering
    if phase_2_core:
        dot_lines.append('  subgraph cluster_2 {')
        dot_lines.append('    label="⚙️ Stage 2: Core Engineering Tools";')
        dot_lines.append('    style="dashed,rounded"; color="#B44A32"; fontcolor="#B44A32"; fontsize="10";')
        for s in phase_2_core:
            dot_lines.append(render_node(s))
        dot_lines.append('  }')

    # Subgraph 3: Target Role Specialization
    if phase_3_target:
        dot_lines.append('  subgraph cluster_3 {')
        dot_lines.append('    label="🎯 Stage 3: Target Role Readiness";')
        dot_lines.append('    style="dashed,rounded"; color="#141413"; fontcolor="#141413"; fontsize="10";')
        for s in phase_3_target:
            dot_lines.append(render_node(s))
        dot_lines.append('  }')

    # Edges: Only draw immediate prerequisite connections
    for skill in relevant_skills:
        prereqs = graph.get(skill, {}).get("prerequisites", [])
        for p in prereqs:
            if p in relevant_skills:
                if skill in path_skill_names and (p in path_skill_names or p in current_skills):
                    edge_color = "#B44A32"
                    penwidth = "1.4"
                elif p in current_skills and skill in current_skills:
                    edge_color = "#2E5C3B"
                    penwidth = "1.2"
                else:
                    edge_color = "#D4CEC3"
                    penwidth = "0.9"
                dot_lines.append(f'  "{p}" -> "{skill}" [color="{edge_color}", penwidth="{penwidth}"];')

    dot_lines.append('}')
    return "\n".join(dot_lines)
