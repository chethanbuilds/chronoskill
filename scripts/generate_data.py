#!/usr/bin/env python3
"""
Generate realistic messy job listings dataset for ChronoSkill across 12 tech disciplines.
Contains at least 500 listings across 12 disciplines with realistic noise,
Indian tech hubs, INR compensation benchmarks, and variations.
"""

import csv
import random

ROLES = [
    "Data Analyst",
    "Data Scientist",
    "ML Engineer",
    "AI / GenAI Engineer",
    "Data Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full-Stack Developer",
    "DevOps Engineer",
    "Cloud Architect",
    "Site Reliability Engineer (SRE)",
    "Cybersecurity Analyst",
]

COMPANIES = [
    "Infosys Labs", "Tata Consultancy Systems", "Flipkart Engineering", "Swiggy Core",
    "Zomato Tech", "CRED Platforms", "Razorpay Engineering", "Freshworks Cloud",
    "Jio Platforms", "Groww Systems", "PhonePe Payments", "Ola Mobility",
    "Zerodha Tech", "Atelier Analytics India", "Klar Design Group", "Monolith Systems",
    "Cortex Dynamics", "Elysium Networks", "Beacon Robotics", "Apex Security India",
    "Postman India", "BrowserStack", "Dream11 Tech", "InMobi Labs"
]

LOCATIONS = [
    "Bengaluru, KA", "Hyderabad, TS", "Pune, MH", "Remote (India)",
    "Gurugram, HR", "Mumbai, MH", "Chennai, TN", "Noida, UP", ""
]

EXPERIENCE_LEVELS = ["Entry Level / Fresher", "Junior", "Mid-Level", "Senior", "Lead / Staff", ""]

ROLE_INR_SALARIES = {
    "Data Analyst": ["₹5.5 - ₹9.0 LPA", "₹7.0 - ₹12.0 LPA", "₹10.0 - ₹16.0 LPA", "₹12.0 - ₹18.0 LPA", ""],
    "Data Scientist": ["₹8.0 - ₹14.0 LPA", "₹12.0 - ₹20.0 LPA", "₹18.0 - ₹28.0 LPA", "₹24.0 - ₹38.0 LPA", ""],
    "ML Engineer": ["₹10.0 - ₹16.0 LPA", "₹15.0 - ₹24.0 LPA", "₹22.0 - ₹35.0 LPA", "₹28.0 - ₹45.0 LPA", ""],
    "AI / GenAI Engineer": ["₹12.0 - ₹18.0 LPA", "₹18.0 - ₹28.0 LPA", "₹26.0 - ₹42.0 LPA", "₹35.0 - ₹55.0 LPA", ""],
    "Data Engineer": ["₹7.0 - ₹12.0 LPA", "₹11.0 - ₹18.0 LPA", "₹16.0 - ₹26.0 LPA", "₹22.0 - ₹36.0 LPA", ""],
    "Backend Developer": ["₹6.5 - ₹11.0 LPA", "₹10.0 - ₹18.0 LPA", "₹16.0 - ₹26.0 LPA", "₹22.0 - ₹36.0 LPA", ""],
    "Frontend Developer": ["₹5.5 - ₹10.0 LPA", "₹9.0 - ₹16.0 LPA", "₹14.0 - ₹22.0 LPA", "₹18.0 - ₹30.0 LPA", ""],
    "Full-Stack Developer": ["₹7.0 - ₹12.0 LPA", "₹11.0 - ₹19.0 LPA", "₹17.0 - ₹27.0 LPA", "₹24.0 - ₹38.0 LPA", ""],
    "DevOps Engineer": ["₹7.5 - ₹12.5 LPA", "₹12.0 - ₹20.0 LPA", "₹18.0 - ₹28.0 LPA", "₹25.0 - ₹40.0 LPA", ""],
    "Cloud Architect": ["₹14.0 - ₹22.0 LPA", "₹22.0 - ₹35.0 LPA", "₹32.0 - ₹48.0 LPA", "₹42.0 - ₹65.0 LPA", ""],
    "Site Reliability Engineer (SRE)": ["₹8.0 - ₹14.0 LPA", "₹14.0 - ₹22.0 LPA", "₹20.0 - ₹32.0 LPA", "₹28.0 - ₹45.0 LPA", ""],
    "Cybersecurity Analyst": ["₹6.0 - ₹11.0 LPA", "₹10.0 - ₹17.0 LPA", "₹15.0 - ₹25.0 LPA", "₹20.0 - ₹34.0 LPA", ""]
}

SKILL_VARIANTS = {
    "Python": ["Python", "py", "python3", "Python 3", "PYTHON", " python "],
    "JavaScript": ["JavaScript", "JS", "javascript", "Java Script", "ES6+", " Javascript "],
    "TypeScript": ["TypeScript", "TS", "typescript", "Type Script", " TypeScript "],
    "Go (Golang)": ["Go", "Golang", "golang", "Go (Golang)", "go lang"],
    "Java": ["Java", "java", "Core Java", "Java 17/21"],
    "HTML & CSS": ["HTML & CSS", "HTML5/CSS3", "Semantic HTML", "css / html", "HTML/CSS"],
    "SQL": ["SQL", "sql", "Structured Query Language", "ANSI SQL", " SQL "],
    "Git": ["Git", "git", "GitHub", "Git / GitHub", "Gitlab"],
    "Linux": ["Linux", "linux", "Ubuntu / Linux", "UNIX", "Bash / Linux", "Shell Scripting"],
    "Math & Statistics": ["Math & Statistics", "Statistics", "Applied Mathematics", "Probability & Stats"],
    "Networking": ["Networking", "TCP/IP", "Computer Networking", "DNS / HTTP protocols"],
    "React": ["React", "React.js", "ReactJS", "react", " React.js "],
    "Next.js": ["Next.js", "NextJS", "next.js", "Next js"],
    "Vue.js": ["Vue.js", "Vue", "VueJS", "vue.js"],
    "Tailwind CSS": ["Tailwind CSS", "Tailwind", "tailwind", "TailwindCSS"],
    "State Management": ["State Management", "Redux / Zustand", "Redux", "Zustand"],
    "Web Performance": ["Web Performance", "Core Web Vitals", "Frontend Performance"],
    "REST APIs": ["REST APIs", "RESTful APIs", "API Design", "REST"],
    "FastAPI": ["FastAPI", "fast api", "fastapi", "Fast API"],
    "Node.js": ["Node.js", "Node", "nodejs", "node.js", "NodeJS"],
    "Express.js": ["Express.js", "Express", "express", "ExpressJS"],
    "Django": ["Django", "django", "Django REST Framework"],
    "Spring Boot": ["Spring Boot", "SpringBoot", "spring-boot", "Spring"],
    "Relational Databases": ["Relational Databases", "PostgreSQL", "postgres", "Postgres DB", "MySQL"],
    "NoSQL Databases": ["NoSQL Databases", "MongoDB", "mongo", "DocumentDB"],
    "Redis": ["Redis", "redis", "Redis Cache", "In-Memory Caching"],
    "Message Queues": ["Message Queues", "Apache Kafka", "Kafka", "RabbitMQ"],
    "Database Optimization": ["Database Optimization", "query tuning", "Indexing & Sharding"],
    "Microservices": ["Microservices", "microservices architecture", "Service-Oriented Arch"],
    "System Design": ["System Design", "system architecture", "Distributed Systems Design"],
    "Pandas": ["Pandas", "pandas", "pandas/numpy", " Pandas "],
    "Data Analysis": ["Data Analysis", "data analysis", "Exploratory Data Analysis", "EDA"],
    "Data Visualization": ["Data Visualization", "data viz", "Tableau", "Power BI", "PowerBI"],
    "Data Modeling": ["Data Modeling", "data modeling", "Schema Design"],
    "Data Warehousing": ["Data Warehousing", "Snowflake", "BigQuery", "Snowflake / BigQuery", "dbt"],
    "Apache Spark": ["Apache Spark", "Spark", "PySpark", "spark"],
    "Airflow / ETL Pipelines": ["Airflow / ETL Pipelines", "Apache Airflow", "Airflow", "ETL Pipelines"],
    "Scikit-Learn": ["scikit-learn", "sklearn", "Scikit Learn", "scikit learn"],
    "Machine Learning": ["Machine Learning", "ML", "machine learning", "Statistical Learning"],
    "Deep Learning": ["Deep Learning", "DL", "deep learning", "Neural Networks"],
    "PyTorch": ["PyTorch", "pytorch", "torch", " PyTorch "],
    "TensorFlow": ["TensorFlow", "tensorflow", "TF", "Keras"],
    "Computer Vision": ["Computer Vision", "OpenCV", "CV"],
    "NLP & LLMs": ["NLP & LLMs", "LLMs", "NLP", "Natural Language Processing", "LangChain / LLMs"],
    "LangChain & RAG": ["LangChain & RAG", "LangChain", "RAG", "Retrieval Augmented Generation"],
    "Vector Databases": ["Vector Databases", "Pinecone", "ChromaDB", "Vector DB"],
    "MLOps": ["MLOps", "mlops", "MLflow / Model Registry", "Model Deployment"],
    "Docker": ["Docker", "docker", "Docker containerization", "docker-ce", " Docker "],
    "Kubernetes": ["Kubernetes", "k8s", "K8s", "kube", "kubernetes"],
    "CI/CD": ["CI/CD", "ci cd", "cicd", "continuous integration", "GitHub Actions / CI"],
    "Cloud (AWS)": ["Cloud (AWS)", "AWS", "aws", "Amazon Web Services", "AWS Cloud"],
    "Cloud (Azure / GCP)": ["Cloud (Azure / GCP)", "Azure", "GCP", "Google Cloud"],
    "Terraform": ["Terraform", "terraform", "TF", "IaC (Terraform)"],
    "Ansible": ["Ansible", "ansible", "Configuration Management"],
    "Monitoring & Observability": ["Monitoring & Observability", "Prometheus / Grafana", "Datadog", "observability"],
    "Operating Systems": ["Operating Systems", "OS Internals", "Kernel / OS"],
    "Cryptography": ["Cryptography", "Crypto", "Encryption / PKI", "applied cryptography"],
    "Network Security": ["Network Security", "NetSec", "Firewalls / IDS", "Network Defense"],
    "Security Operations": ["Security Operations", "SecOps", "Incident Response", "SOC"],
    "SIEM": ["SIEM", "Splunk / SIEM", "Security Information & Event Mgmt"],
    "Penetration Testing": ["Penetration Testing", "pen testing", "Pentesting", "Ethical Hacking"],
    "Application Security": ["Application Security", "AppSec", "OWASP Top 10", "secure coding"],
    "Threat Modeling": ["Threat Modeling", "threat modeling", "STRIDE / Threat Analysis"],
    "Wireshark": ["Wireshark", "wireshark", "Packet Analysis"],
    "IAM (Identity & Access)": ["IAM (Identity & Access)", "IAM", "OAuth2 / OIDC", "Identity Management"]
}

ROLE_SKILL_PROFILES = {
    "Data Analyst": {
        "core": ["SQL", "Python", "Data Analysis", "Data Visualization", "Pandas"],
        "secondary": ["Data Modeling", "Data Warehousing", "Math & Statistics"],
        "occasional": ["Git", "Scikit-Learn", "Apache Spark"]
    },
    "Data Scientist": {
        "core": ["Python", "SQL", "Math & Statistics", "Data Analysis", "Machine Learning", "Pandas", "Scikit-Learn"],
        "secondary": ["Data Visualization", "Deep Learning", "Git", "TensorFlow"],
        "occasional": ["PyTorch", "Data Warehousing", "Docker", "NLP & LLMs"]
    },
    "ML Engineer": {
        "core": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Docker", "Git", "Math & Statistics"],
        "secondary": ["MLOps", "Scikit-Learn", "FastAPI", "Linux", "NLP & LLMs"],
        "occasional": ["Kubernetes", "Cloud (AWS)", "CI/CD", "System Design", "Vector Databases"]
    },
    "AI / GenAI Engineer": {
        "core": ["Python", "NLP & LLMs", "PyTorch", "LangChain & RAG", "Vector Databases", "FastAPI", "Deep Learning"],
        "secondary": ["Machine Learning", "Docker", "Git", "MLOps", "Cloud (AWS)"],
        "occasional": ["Kubernetes", "System Design", "Scikit-Learn"]
    },
    "Data Engineer": {
        "core": ["Python", "SQL", "Relational Databases", "Data Modeling", "Data Warehousing", "Apache Spark", "Airflow / ETL Pipelines"],
        "secondary": ["Message Queues", "Linux", "Docker", "Cloud (AWS)", "Git"],
        "occasional": ["NoSQL Databases", "Kubernetes", "CI/CD", "System Design"]
    },
    "Backend Developer": {
        "core": ["Python", "REST APIs", "Relational Databases", "Git", "Linux", "Docker"],
        "secondary": ["FastAPI", "Node.js", "System Design", "Database Optimization", "Microservices", "Redis"],
        "occasional": ["Kubernetes", "CI/CD", "Cloud (AWS)", "Go (Golang)", "Message Queues", "Java"]
    },
    "Frontend Developer": {
        "core": ["HTML & CSS", "JavaScript", "TypeScript", "React", "Git"],
        "secondary": ["Next.js", "Tailwind CSS", "State Management", "Web Performance", "REST APIs"],
        "occasional": ["Vue.js", "Node.js", "Docker", "Linux"]
    },
    "Full-Stack Developer": {
        "core": ["JavaScript", "TypeScript", "React", "Node.js", "HTML & CSS", "REST APIs", "Git"],
        "secondary": ["Relational Databases", "Docker", "FastAPI", "Next.js", "Tailwind CSS"],
        "occasional": ["Linux", "Cloud (AWS)", "CI/CD", "System Design", "NoSQL Databases"]
    },
    "DevOps Engineer": {
        "core": ["Linux", "Docker", "Kubernetes", "CI/CD", "Cloud (AWS)", "Git"],
        "secondary": ["Terraform", "Monitoring & Observability", "Python", "Networking", "Ansible"],
        "occasional": ["System Design", "Security Operations", "Network Security", "Cloud (Azure / GCP)"]
    },
    "Cloud Architect": {
        "core": ["Cloud (AWS)", "Linux", "Networking", "Terraform", "Docker", "Kubernetes", "System Design"],
        "secondary": ["Cloud (Azure / GCP)", "CI/CD", "Network Security", "Microservices", "Python"],
        "occasional": ["Monitoring & Observability", "IAM (Identity & Access)", "Ansible"]
    },
    "Site Reliability Engineer (SRE)": {
        "core": ["Linux", "Docker", "Kubernetes", "Monitoring & Observability", "Networking", "CI/CD", "Python"],
        "secondary": ["Terraform", "System Design", "Cloud (AWS)", "Go (Golang)", "Linux"],
        "occasional": ["Database Optimization", "Security Operations", "Ansible"]
    },
    "Cybersecurity Analyst": {
        "core": ["Networking", "Linux", "Network Security", "Security Operations", "SIEM"],
        "secondary": ["Penetration Testing", "Application Security", "Threat Modeling", "Python", "Wireshark"],
        "occasional": ["Operating Systems", "Cryptography", "Git", "Docker", "IAM (Identity & Access)"]
    }
}


def sample_skills_for_role(role: str) -> list[str]:
    profile = ROLE_SKILL_PROFILES[role]
    chosen = []
    
    for skill in profile["core"]:
        if random.random() < 0.90:
            chosen.append(skill)
    for skill in profile["secondary"]:
        if random.random() < 0.55:
            chosen.append(skill)
    for skill in profile["occasional"]:
        if random.random() < 0.25:
            chosen.append(skill)
            
    if len(chosen) < 3:
        chosen = profile["core"][:4]
        
    random.shuffle(chosen)
    
    noisy_skills = []
    for skill in chosen:
        variants = SKILL_VARIANTS.get(skill, [skill])
        variant = random.choice(variants)
        
        if random.random() < 0.20:
            variant = f"  {variant}  "
        noisy_skills.append(variant)
        
        if random.random() < 0.08:
            noisy_skills.append(random.choice(variants))
            
    return noisy_skills


def main():
    random.seed(42)
    rows = []
    job_id_counter = 1000
    
    # 12 roles * ~44 listings = ~528 listings
    for role in ROLES:
        num_listings = random.randint(42, 48)
        for _ in range(num_listings):
            job_id_counter += 1
            skills_list = sample_skills_for_role(role)
            
            separator = ", " if random.random() > 0.15 else " ,  "
            skills_str = separator.join(skills_list)
            
            company = random.choice(COMPANIES)
            location = random.choice(LOCATIONS)
            exp_level = random.choice(EXPERIENCE_LEVELS)
            salary = random.choice(ROLE_INR_SALARIES[role])
            
            title_prefix = random.choice(["", "Senior ", "Lead ", "Junior ", "Staff ", "Associate "])
            title = f"{title_prefix}{role}"
            
            rows.append({
                "job_id": f"JOB-{job_id_counter}",
                "title": title,
                "role": role,
                "company": company,
                "location": location,
                "experience_level": exp_level,
                "salary_range": salary,
                "skills": skills_str
            })
            
    # Add duplicate postings
    duplicates = random.sample(rows, 30)
    for dup in duplicates:
        dup_copy = dict(dup)
        if random.random() < 0.5:
            dup_copy["job_id"] = f"JOB-{job_id_counter + 1}"
            job_id_counter += 1
        rows.append(dup_copy)
        
    # Corrupted / noisy bad rows for cleaning verification
    rows.append({
        "job_id": "JOB-9991", "title": "Data Analyst", "role": "",
        "company": "Corrupted Row Inc", "location": "Remote", "experience_level": "Junior",
        "salary_range": "₹6.0 LPA", "skills": "Python, SQL"
    })
    rows.append({
        "job_id": "JOB-9992", "title": "Software Engineer", "role": "Backend Developer",
        "company": "Null Skills Corp", "location": "Bengaluru", "experience_level": "Senior",
        "salary_range": "₹22.0 LPA", "skills": ""
    })
    rows.append({
        "job_id": "JOB-9993", "title": "Unknown Title", "role": "DevOps Engineer",
        "company": "Ghost Post", "location": "", "experience_level": "",
        "salary_range": "", "skills": "   ,   ,   "
    })
    rows.append({
        "job_id": "JOB-9994", "title": "Frontend Lead", "role": "Frontend Developer",
        "company": "Broken String", "location": "Pune", "experience_level": "Lead",
        "salary_range": "", "skills": "n/a"
    })
    rows.append({
        "job_id": "JOB-9995", "title": "", "role": "",
        "company": "", "location": "", "experience_level": "",
        "salary_range": "", "skills": ""
    })
    rows.append({
        "job_id": "JOB-9996", "title": "Cybersecurity Analyst", "role": "Cybersecurity Analyst",
        "company": "SecureNet India", "location": "Hyderabad", "experience_level": "Junior",
        "salary_range": "₹9.5 LPA", "skills": "none specified"
    })
    
    random.shuffle(rows)
    
    out_path = "data/job_listings.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["job_id", "title", "role", "company", "location", "experience_level", "salary_range", "skills"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Generated {len(rows)} job listings at {out_path} across {len(ROLES)} roles.")


if __name__ == "__main__":
    main()
