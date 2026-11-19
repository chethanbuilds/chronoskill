# ChronoSkill ◈

> **State-Space Career Trajectory Engine**  
> A production-feeling career roadmap web application crafted with Swiss editorial restraint, Indian tech market benchmarks (INR / LPA), 100% free curated learning resources, and a beginner-friendly step-by-step curriculum.

---

## 1. Overview

**ChronoSkill** models technical craft as an explicit directed state-space graph where nodes represent atomic capabilities and edges denote strict prerequisite relationships.

Rather than relying on black-box heuristics or stochastic AI hallucinations, ChronoSkill evaluates **414+ verified market job listings** across 8 core tech disciplines in Indian tech hubs (Bengaluru, Hyderabad, Pune, Gurugram, Mumbai, and Remote). It extracts true empirical demand frequencies, normalizes messy industry skill variants, and uses a deterministic topological sort to synthesize the most time-efficient learning curriculum from a user's current skillset to their target discipline.

---

## 2. New Features & Updates

### 🇮🇳 Indian Rupee (INR / LPA) Compensation Benchmarks
- Benchmark compensation is displayed in **Lakhs Per Annum (LPA)** based on 2026 Indian tech market surveys:
  - **Data Analyst**: ₹6.5 - ₹14.0 LPA *(Fresher: ₹5.0 - ₹8.0 LPA · Senior: ₹12.0 - ₹18.0 LPA)*
  - **Data Scientist**: ₹12.0 - ₹26.0 LPA *(Fresher: ₹8.0 - ₹14.0 LPA · Senior: ₹20.0 - ₹38.0 LPA)*
  - **ML Engineer**: ₹15.0 - ₹32.0 LPA *(Fresher: ₹10.0 - ₹16.0 LPA · Senior: ₹25.0 - ₹45.0 LPA)*
  - **Backend Developer**: ₹8.0 - ₹22.0 LPA *(Fresher: ₹6.0 - ₹10.0 LPA · Senior: ₹16.0 - ₹32.0 LPA)*
  - **Frontend Developer**: ₹7.0 - ₹20.0 LPA *(Fresher: ₹5.0 - ₹9.0 LPA · Senior: ₹14.0 - ₹28.0 LPA)*
  - **DevOps Engineer**: ₹10.0 - ₹25.0 LPA *(Fresher: ₹7.0 - ₹12.0 LPA · Senior: ₹18.0 - ₹36.0 LPA)*
  - **Full-Stack Developer**: ₹9.0 - ₹24.0 LPA *(Fresher: ₹6.0 - ₹11.0 LPA · Senior: ₹16.0 - ₹34.0 LPA)*
  - **Cybersecurity Analyst**: ₹8.5 - ₹22.0 LPA *(Fresher: ₹6.0 - ₹10.0 LPA · Senior: ₹15.0 - ₹30.0 LPA)*

### 🎓 100% Free Curated Learning Vault
- Each role features a dedicated **Free Learning Vault** pointing directly to world-class free courses:
  - **Harvard CS50** (CS50x, CS50AI, CS50W)
  - **freeCodeCamp** verified certifications
  - **Google Data Analytics** (Coursera free audit)
  - **fast.ai** (Practical Deep Learning for Coders)
  - **University of Helsinki** (Full Stack Open)
  - **The Odin Project** (Full-Stack Web Development)
  - **PortSwigger Web Security Academy** (Interactive AppSec labs)
  - **Kaggle Learn** (Interactive Python, SQL, ML micro-courses)

### 🧭 Crystal-Clear Beginner-Friendly Curriculum
- **Phase Grouping**: ChronoSkill breaks down the roadmap into 3 color-coded phases:
  - 🟢 **Phase 1: Absolute Foundations** (Beginner-friendly entry with 0 prerequisites)
  - 🟡 **Phase 2: Core Engineering & Frameworks** (Everyday industry tooling)
  - 🔴 **Phase 3: Production Specialization & Scale** (System architecture & interviews)
- **Every Step Includes**:
  - **Plain English Explanation**: What the tool actually is without confusing jargon.
  - **Why Learn This Now**: Explains the prerequisite relationship in plain words.
  - **What You Will Master (Checklist)**: 4 exact bullet points of topics to study.
  - **Hands-on Beginner Project**: A concrete portfolio project to build.
  - **Top Free Links**: Direct links to free courses, documentation, and videos.

### 🎨 Visual Polish & Contrast Fixes
- Fixed the dark background issue on pills: Unselected pills now have clean white backgrounds with dark text, and active pills have an atelier terracotta fill with white text.
- Added a **Category Filter** (`All Disciplines`, `Frontend`, `Backend`, `Data & AI`, `Languages`, `DevOps`, `Cybersecurity`) to browse 55+ technical competencies easily.
- Unified role selection cards: Cleaned up duplicate button boxes into single integrated cards.

---

## 3. Project Architecture

```
Aiproject/
├── app.py                  # Main Streamlit application
├── data/
│   ├── job_listings.csv    # 414 messy raw postings across 8 roles with INR compensation
│   └── skills_graph.py     # Prerequisite DAG, alias map, free resources, INR benchmarks, and path engine
├── scripts/
│   └── generate_data.py    # Synthetic dataset generator with Indian tech hubs and INR compensation
├── tests/
│   └── test_chronoskill.py # Automated unit test suite verifying DAG validity and path engine invariants
├── .streamlit/
│   ├── config.toml         # Streamlit theme enforcement (light mode, atelier palette)
│   └── credentials.toml    # Streamlit local credentials configuration
├── requirements.txt        # Python package dependencies
└── README.md               # Documentation and execution instructions
```

---

## 4. Run Instructions

The app is currently active in the background on port `8503`:

```
URL: http://localhost:8503
```

To run or restart the application manually:

```bash
cd /Users/chethan/Documents/Aiproject
source .venv/bin/activate
export HOME="$(pwd)"
streamlit run app.py --server.port 8503 --server.address 127.0.0.1 --server.headless true
```

*(Or simply `streamlit run app.py` on default port 8501).*

---

## 5. Automated Tests

Run the test suite to verify all invariants:
```bash
python3 tests/test_chronoskill.py
```
*(All 8 test suites pass: alias normalization, DAG acyclicity, data cleaning, role coverage, topological ordering, empty state, qualified state, and Graphviz DOT syntax).*
