"""
ChronoSkill — Career Roadmap & State-Space Skill Engine.
A minimal, production-grade career-roadmap web application crafted with
Swiss editorial restraint, Indian tech market benchmarks (INR / LPA),
curated free learning resources, and beginner-friendly linear & graph views.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from typing import Any

from data.skills_graph import (
    SKILLS_GRAPH,
    ROLE_INR_BENCHMARKS,
    ROLE_FREE_RESOURCES,
    clean_job_dataset,
    compute_role_profiles,
    generate_learning_path,
    generate_graphviz_dot,
)

# -----------------------------------------------------------------------------
# Streamlit App Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ChronoSkill — Career Roadmap Atelier",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# HTML Helper: Prevents Markdown Parser from treating HTML as Code Blocks
# -----------------------------------------------------------------------------
def render_clean_html(html_str: str):
    """
    Renders raw HTML safely by stripping leading spaces from every line
    and removing blank lines. This prevents CommonMark from accidentally
    treating indented HTML lines (>= 4 spaces) as code blocks (<pre><code>).
    """
    clean_str = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean_str, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data Ingestion (Fresh on Every App Load — No Stale Cache)
# -----------------------------------------------------------------------------
def load_and_process_data():
    raw_df = pd.read_csv("data/job_listings.csv")
    cleaned_df, audit_summary = clean_job_dataset(raw_df)
    profiles = compute_role_profiles(cleaned_df)
    return cleaned_df, audit_summary, profiles


CLEANED_DF, AUDIT_SUMMARY, ROLE_PROFILES = load_and_process_data()
ALL_ROLES = sorted(list(ROLE_PROFILES.keys()))

# Group skills by category for organized selection
SKILLS_BY_CATEGORY: dict[str, list[str]] = {}
for skill_id, meta in SKILLS_GRAPH.items():
    cat = meta.get("category", "General")
    SKILLS_BY_CATEGORY.setdefault(cat, []).append(skill_id)

ALL_SKILLS = sorted(list(SKILLS_GRAPH.keys()))
CATEGORIES_LIST = ["All Disciplines"] + sorted(list(SKILLS_BY_CATEGORY.keys()))


# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "selected_role" not in st.session_state:
    st.session_state["selected_role"] = "ML Engineer"

if "current_skills" not in st.session_state:
    st.session_state["current_skills"] = ["Python", "Git", "SQL"]

if "active_skill_category" not in st.session_state:
    st.session_state["active_skill_category"] = "All Disciplines"

if "graph_view_mode" not in st.session_state:
    st.session_state["graph_view_mode"] = "Subway Line (Beginner Friendly)"


# -----------------------------------------------------------------------------
# Inject Custom CSS (High Contrast, Light Mode, No Black Background on Pills)
# -----------------------------------------------------------------------------
def inject_custom_styles():
    render_clean_html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        /* Hide Streamlit default chrome & branding */
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }
        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }
        [data-testid="stStatusWidget"] { display: none; }
        div[data-testid="stSidebarNav"] { display: none; }

        /* Root Variables */
        :root {
            --bg: #F5F3EF;
            --surface: #FAF9F6;
            --surface-hover: #FFFFFF;
            --border: #E2DCD3;
            --border-dark: #141413;
            --text-primary: #141413;
            --text-muted: #5E5A54;
            --text-subtle: #8A857C;
            --accent: #B44A32; /* Atelier terracotta */
            --accent-soft: #F9EBE7;
            --success: #2E5C3B; /* Indian moss green */
            --success-soft: #EEF4EF;
            --ease-swiss: cubic-bezier(0.22, 1, 0.36, 1);
        }

        /* Base Typography & Background */
        html, body, .stApp {
            background-color: var(--bg) !important;
            color: var(--text-primary) !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            letter-spacing: -0.01em;
            -webkit-font-smoothing: antialiased;
        }

        .main .block-container {
            max-width: 1180px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* Top Brand Navigation Bar */
        .masthead {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 0 1.5rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 2.5rem;
        }
        .masthead-logo {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.84rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .masthead-dot {
            width: 7px;
            height: 7px;
            background-color: var(--accent);
            border-radius: 50%;
            display: inline-block;
        }
        .masthead-meta {
            font-size: 0.76rem;
            color: var(--text-muted);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 500;
        }

        /* Hero Section */
        .hero-section {
            margin-bottom: 3.25rem;
        }
        .hero-eyebrow {
            font-size: 0.74rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--accent);
            margin-bottom: 0.8rem;
        }
        .hero-title {
            font-family: 'Instrument Serif', Georgia, serif;
            font-size: clamp(2.5rem, 5vw, 4.2rem);
            line-height: 1.05;
            font-weight: 400;
            color: var(--text-primary);
            letter-spacing: -0.025em;
            margin-bottom: 1.25rem;
            max-width: 950px;
        }
        .hero-title em {
            font-style: italic;
            font-family: 'Instrument Serif', Georgia, serif;
            color: var(--text-muted);
        }
        .hero-desc {
            font-size: 1.05rem;
            line-height: 1.65;
            color: var(--text-muted);
            max-width: 700px;
            margin-bottom: 1.75rem;
            font-weight: 400;
        }
        .hero-specs {
            display: flex;
            flex-wrap: wrap;
            gap: 1.25rem;
            align-items: center;
            padding-top: 1.25rem;
            border-top: 1px solid var(--border);
        }
        .spec-item {
            font-size: 0.78rem;
            color: var(--text-muted);
            letter-spacing: 0.04em;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }
        .spec-item strong {
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Section Headers */
        .section-header-box {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.75rem;
            margin-top: 3.25rem;
            margin-bottom: 1.5rem;
        }
        .section-tag {
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--text-subtle);
        }
        .section-title-editorial {
            font-family: 'Instrument Serif', Georgia, serif;
            font-size: 1.95rem;
            font-weight: 400;
            color: var(--text-primary);
            letter-spacing: -0.015em;
        }

        /* Unified Role Card */
        .role-card-wrapper {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1.2rem 1.15rem 0.9rem 1.15rem;
            transition: all 400ms var(--ease-swiss);
            margin-bottom: 0.8rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 215px;
        }
        .role-card-wrapper:hover {
            border-color: var(--border-dark);
            background-color: var(--surface-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        .role-card-wrapper.active-card {
            border-color: var(--accent) !important;
            background-color: #FAF5F2 !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }
        .role-card-index {
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            font-weight: 600;
            color: var(--text-subtle);
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }
        .role-card-name {
            font-family: 'Instrument Serif', Georgia, serif;
            font-size: 1.35rem;
            line-height: 1.15;
            color: var(--text-primary);
            font-weight: 400;
            margin-bottom: 0.4rem;
        }
        .role-card-salary {
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 0.45rem;
        }
        .role-card-skills {
            font-size: 0.76rem;
            color: var(--text-muted);
            line-height: 1.4;
            margin-bottom: 0.6rem;
            flex-grow: 1;
        }

        /* EXPLICIT HIGH-CONTRAST PILLS FIX (No Black Background) */
        div[data-testid="stPills"] {
            background: transparent !important;
            padding: 0.3rem 0 !important;
        }
        div[data-testid="stPills"] button,
        div[data-testid="stPills"] [role="checkbox"],
        div[data-testid="stPills"] [data-baseweb="tag"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1px solid #D4CEBF !important;
            border-radius: 20px !important;
            color: #141413 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            padding: 0.4rem 0.95rem !important;
            transition: all 250ms var(--ease-swiss) !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
        }
        div[data-testid="stPills"] button p,
        div[data-testid="stPills"] button span,
        div[data-testid="stPills"] [role="checkbox"] p,
        div[data-testid="stPills"] [role="checkbox"] span {
            color: #141413 !important;
            font-weight: 500 !important;
        }
        div[data-testid="stPills"] button:hover {
            background-color: #F8F3EE !important;
            background: #F8F3EE !important;
            border-color: #B44A32 !important;
            color: #B44A32 !important;
            transform: translateY(-1px) !important;
        }
        div[data-testid="stPills"] button:hover p,
        div[data-testid="stPills"] button:hover span {
            color: #B44A32 !important;
        }
        div[data-testid="stPills"] button[aria-selected="true"],
        div[data-testid="stPills"] [role="checkbox"][aria-checked="true"] {
            background-color: #B44A32 !important;
            background: #B44A32 !important;
            color: #FFFFFF !important;
            border-color: #B44A32 !important;
            box-shadow: 0 2px 5px rgba(180, 74, 50, 0.25) !important;
        }
        div[data-testid="stPills"] button[aria-selected="true"] p,
        div[data-testid="stPills"] button[aria-selected="true"] span,
        div[data-testid="stPills"] [role="checkbox"][aria-checked="true"] p,
        div[data-testid="stPills"] [role="checkbox"][aria-checked="true"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Beginner Orientation Banner */
        .beginner-guide-banner {
            background-color: #FAF6F0;
            border: 1px solid #E2DCD3;
            border-left: 3.5px solid #B44A32;
            border-radius: 4px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 2rem;
        }
        .beginner-guide-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .beginner-guide-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
            margin-top: 0.8rem;
            font-size: 0.82rem;
            color: var(--text-muted);
            line-height: 1.5;
        }
        .beginner-step-rule strong {
            color: var(--text-primary);
            display: block;
            margin-bottom: 0.2rem;
        }

        /* Beginner-Friendly Step Card (Human Readable, Zero Raw HTML Glitches) */
        .beginner-step-card {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.75rem;
            transition: all 300ms var(--ease-swiss);
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .beginner-step-card:hover {
            border-color: var(--border-dark);
            box-shadow: 0 4px 14px rgba(0,0,0,0.04);
            transform: translateX(3px);
        }
        .step-phase-tag {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            display: inline-block;
            margin-bottom: 0.4rem;
        }
        .step-heading-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.75rem;
            margin-bottom: 1rem;
        }
        .step-skill-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        .step-duration-badge {
            font-size: 0.74rem;
            font-weight: 600;
            color: var(--accent);
            background-color: var(--accent-soft);
            padding: 3px 9px;
            border-radius: 3px;
        }
        .step-plain-english {
            font-size: 0.92rem;
            color: var(--text-primary);
            line-height: 1.55;
            margin-bottom: 1rem;
            background-color: #FAF9F6;
            padding: 0.75rem 1rem;
            border-radius: 3px;
            border-left: 3px solid #8A857C;
        }
        .step-grid-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.2rem;
        }
        .checklist-box {
            background-color: #FAF9F6;
            padding: 1rem 1.2rem;
            border-radius: 3px;
            border: 1px solid #ECE7DE;
        }
        .checklist-title {
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-primary);
            margin-bottom: 0.6rem;
        }
        .checklist-item {
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-bottom: 0.35rem;
            display: flex;
            align-items: baseline;
            gap: 0.45rem;
        }
        .checklist-item span {
            color: var(--accent);
            font-weight: 700;
        }
        .project-action-box {
            background-color: var(--success-soft);
            padding: 1rem 1.2rem;
            border-radius: 3px;
            border: 1px solid #DFEBE1;
        }
        .project-action-title {
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--success);
            margin-bottom: 0.4rem;
        }
        .project-action-text {
            font-size: 0.83rem;
            color: #1E3B27;
            line-height: 1.5;
        }
        .step-resources-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            align-items: center;
            border-top: 1px solid var(--border);
            padding-top: 0.9rem;
            font-size: 0.78rem;
        }
        .step-resources-label {
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-size: 0.72rem;
        }
        .step-resource-pill {
            background-color: #FAF9F6;
            border: 1px solid #D8D2C7;
            padding: 3px 9px;
            border-radius: 3px;
            color: var(--text-primary);
            text-decoration: none;
            transition: all 200ms var(--ease-swiss);
        }
        .step-resource-pill:hover {
            border-color: var(--accent);
            color: var(--accent);
            background-color: #FFFFFF;
        }

        /* Beginner Subway Metro Line Flowchart */
        .subway-container {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 2rem 1.5rem;
            margin-bottom: 2rem;
        }
        .subway-station-row {
            display: flex;
            align-items: stretch;
            margin-bottom: 1rem;
            position: relative;
        }
        .subway-marker-col {
            width: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }
        .subway-circle {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.74rem;
            font-weight: 700;
            color: #FFFFFF;
            z-index: 2;
        }
        .subway-line {
            width: 3px;
            flex-grow: 1;
            background-color: #E2DCD3;
            margin: 4px 0;
        }
        .subway-content-card {
            flex-grow: 1;
            background-color: #FAF9F6;
            border: 1px solid #EAE5DC;
            border-radius: 4px;
            padding: 1rem 1.3rem;
            margin-left: 1rem;
            transition: all 250ms var(--ease-swiss);
        }
        .subway-content-card:hover {
            border-color: var(--border-dark);
            background-color: #FFFFFF;
            transform: translateX(3px);
        }

        /* Free Resources Cards */
        .resource-card {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 0.9rem;
            transition: all 300ms var(--ease-swiss);
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }
        .resource-card:hover {
            border-color: var(--accent);
            box-shadow: 0 3px 8px rgba(0,0,0,0.04);
            transform: translateY(-1px);
        }
        .resource-title {
            font-size: 0.96rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }
        .resource-meta {
            display: flex;
            gap: 0.5rem;
            align-items: center;
            font-size: 0.72rem;
            margin-bottom: 0.5rem;
        }
        .badge-provider {
            background-color: #F0EDE6;
            color: var(--text-primary);
            padding: 2px 7px;
            border-radius: 2px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .badge-free {
            background-color: var(--success-soft);
            color: var(--success);
            padding: 2px 7px;
            border-radius: 2px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .resource-why {
            font-size: 0.82rem;
            color: var(--text-muted);
            line-height: 1.45;
        }
        .resource-link-btn {
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--accent);
            text-decoration: none;
            padding: 0.45rem 0.85rem;
            border: 1px solid var(--accent);
            border-radius: 2px;
            white-space: nowrap;
            transition: all 250ms var(--ease-swiss);
        }
        .resource-link-btn:hover {
            background-color: var(--accent);
            color: #FFFFFF !important;
        }

        /* Mastery State Card */
        .mastery-card {
            background-color: #FAF5F2;
            border: 1.5px solid var(--accent);
            border-radius: 4px;
            padding: 2.5rem 2rem;
            text-align: center;
            margin: 2rem 0;
        }
        .mastery-title {
            font-family: 'Instrument Serif', Georgia, serif;
            font-size: 2.4rem;
            color: var(--text-primary);
            margin-bottom: 0.8rem;
        }
        .mastery-text {
            font-size: 1rem;
            color: var(--text-muted);
            max-width: 620px;
            margin: 0 auto 1.5rem auto;
            line-height: 1.6;
        }

        /* Footer */
        .editorial-footer {
            margin-top: 6rem;
            padding-top: 2.5rem;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.76rem;
            color: var(--text-muted);
            letter-spacing: 0.04em;
        }
        .footer-brand {
            font-weight: 600;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 0.16em;
        }

        /* Buttons Overrides */
        .stButton > button {
            background-color: #FFFFFF !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 3px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            padding: 0.45rem 1rem !important;
            transition: all 300ms var(--ease-swiss) !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        }
        .stButton > button:hover {
            border-color: var(--border-dark) !important;
            color: var(--accent) !important;
            transform: translateY(-1px);
        }
        </style>
        """
    )


inject_custom_styles()


# -----------------------------------------------------------------------------
# Component 1: Brand Masthead
# -----------------------------------------------------------------------------
render_clean_html(
    """
    <div class="masthead">
        <div class="masthead-logo">
            <span class="masthead-dot"></span>
            CHRONOSKILL
        </div>
        <div class="masthead-meta">
            Atelier Edition · 12 Tech Disciplines · Indian Tech Market Benchmark
        </div>
    </div>
    """
)


# -----------------------------------------------------------------------------
# Component 2: Hero Section
# -----------------------------------------------------------------------------
render_clean_html(
    """
    <div class="hero-section">
        <div class="hero-eyebrow">State-Space Career Trajectory Engine</div>
        <h1 class="hero-title">
            The deliberate path from <em>current craft</em><br>
            to target technical discipline.
        </h1>
        <p class="hero-desc">
            Technical skills form an interconnected directed graph. ChronoSkill evaluates real market demand
            across 580+ verified listings in Indian tech hubs, resolves prerequisite depths, and computes the exact
            step-by-step trajectory required to reach your target role with 100% free resources.
        </p>
        <div class="hero-specs">
            <div class="spec-item"><strong>587</strong> Verified Postings Analyzed</div>
            <div class="spec-item">•</div>
            <div class="spec-item"><strong>12</strong> Tech Disciplines</div>
            <div class="spec-item">•</div>
            <div class="spec-item"><strong>55+</strong> Modern Skills</div>
            <div class="spec-item">•</div>
            <div class="spec-item"><strong>INR (₹ LPA)</strong> Compensation Benchmarks</div>
            <div class="spec-item">•</div>
            <div class="spec-item"><strong>100% Free</strong> Curated Courses</div>
        </div>
    </div>
    """
)


# -----------------------------------------------------------------------------
# Component 3: Section 01 — Target Discipline Selection (12 Disciplines)
# -----------------------------------------------------------------------------
render_clean_html(
    """
    <div class="section-header-box" id="disciplines">
        <div class="section-title-editorial">01 / Target Discipline</div>
        <div class="section-tag">Choose Your Destination (12 Live Roles)</div>
    </div>
    """
)

# Direct Quick-Select Bar for 100% Instant Accessibility across all 12 roles
disc_col1, disc_col2 = st.columns([2.5, 1.5])
with disc_col1:
    current_role = st.session_state.get("selected_role", ALL_ROLES[0])
    current_idx = ALL_ROLES.index(current_role) if current_role in ALL_ROLES else 0

    selected_from_dropdown = st.selectbox(
        "Direct Discipline Selector (All 12 Disciplines):",
        options=ALL_ROLES,
        index=current_idx,
        format_func=lambda r: f"{r}  —  {ROLE_PROFILES[r]['rep_salary']} (₹ Indian Market)  ·  {ROLE_PROFILES[r]['total_listings']} Postings",
        key="discipline_quick_select",
    )
    if selected_from_dropdown != st.session_state["selected_role"]:
        st.session_state["selected_role"] = selected_from_dropdown
        st.rerun()

with disc_col2:
    active_prof = ROLE_PROFILES[st.session_state["selected_role"]]
    render_clean_html(
        f"""
        <div style="background-color: #FAF9F6; border: 1px solid #E2DCD3; border-radius: 4px; padding: 0.6rem 0.9rem; margin-top: 1.65rem;">
            <div style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #B44A32;">Active Destination</div>
            <div style="font-size: 0.88rem; font-weight: 600; color: #141413;">{st.session_state['selected_role']}</div>
            <div style="font-size: 0.74rem; color: #5E5A54;">{active_prof['rep_salary']} · {active_prof['total_listings']} listings analyzed</div>
        </div>
        """
    )

st.write("")

# Render 12 Disciplines in 3 clean rows of 4 columns each
NUM_COLS = 4
for row_start in range(0, len(ALL_ROLES), NUM_COLS):
    row_roles = ALL_ROLES[row_start : row_start + NUM_COLS]
    cols = st.columns(NUM_COLS)
    for col_idx, role in enumerate(row_roles):
        global_idx = row_start + col_idx
        col = cols[col_idx]
        profile = ROLE_PROFILES[role]
        is_active = (role == st.session_state["selected_role"])
        active_class = "active-card" if is_active else ""
        
        inr_salary = profile["rep_salary"]
        core_preview = " · ".join(profile["top_core_skills"][:3])
        
        with col:
            role_card_html = f"""
            <div class="role-card-wrapper {active_class}">
                <div>
                    <div class="role-card-index">DISCIPLINE 0{global_idx+1 if global_idx < 9 else global_idx+1}</div>
                    <div class="role-card-name">{role}</div>
                    <div class="role-card-salary">{inr_salary}</div>
                    <div class="role-card-skills">{core_preview}</div>
                </div>
                <div style="font-size: 0.72rem; color: #8A857C; padding-top: 0.5rem; border-top: 1px solid #ECE7DE;">
                    {profile['total_listings']} listings analyzed
                </div>
            </div>
            """
            render_clean_html(role_card_html)

            if st.button(
                f"{'✓ Selected' if is_active else 'Select Role →'}",
                key=f"btn_role_{role}",
                use_container_width=True
            ):
                st.session_state["selected_role"] = role
                st.rerun()


# -----------------------------------------------------------------------------
# Component 4: Section 02 — Current Skill Inventory
# -----------------------------------------------------------------------------
render_clean_html(
    """
    <div class="section-header-box" id="skills">
        <div class="section-title-editorial">02 / Verified Capabilities</div>
        <div class="section-tag">Current Skill Inventory</div>
    </div>
    """
)

# Archetype Presets
render_clean_html('<div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 0.6rem;">Quick Archetype Presets:</div>')
p_cols = st.columns(6)

with p_cols[0]:
    if st.button("Blank Slate (0)", use_container_width=True):
        st.session_state["current_skills"] = []
        st.rerun()

with p_cols[1]:
    if st.button("Junior Python", use_container_width=True):
        st.session_state["current_skills"] = ["Python", "Git", "SQL"]
        st.rerun()

with p_cols[2]:
    if st.button("Data Analyst", use_container_width=True):
        st.session_state["current_skills"] = ["Python", "SQL", "Pandas", "Data Analysis", "Data Visualization"]
        st.rerun()

with p_cols[3]:
    if st.button("Frontend Craft", use_container_width=True):
        st.session_state["current_skills"] = ["HTML & CSS", "JavaScript", "TypeScript", "React", "Git"]
        st.rerun()

with p_cols[4]:
    if st.button("DevOps Found.", use_container_width=True):
        st.session_state["current_skills"] = ["Linux", "Git", "Docker", "Networking", "CI/CD"]
        st.rerun()

with p_cols[5]:
    if st.button("Full Stack Dev", use_container_width=True):
        st.session_state["current_skills"] = ["HTML & CSS", "JavaScript", "TypeScript", "React", "Node.js", "Python", "SQL", "Docker", "Git"]
        st.rerun()

st.write("")

# Category Filter Bar to keep 55+ skills clean and organized
filter_col1, filter_col2 = st.columns([1, 3])
with filter_col1:
    selected_cat = st.selectbox(
        "Filter skills by track:",
        options=CATEGORIES_LIST,
        index=CATEGORIES_LIST.index(st.session_state.get("active_skill_category", "All Disciplines")),
        label_visibility="collapsed"
    )
    if selected_cat != st.session_state["active_skill_category"]:
        st.session_state["active_skill_category"] = selected_cat
        st.rerun()

if selected_cat == "All Disciplines":
    skills_to_show = ALL_SKILLS
else:
    skills_to_show = sorted(SKILLS_BY_CATEGORY.get(selected_cat, []))

render_clean_html('<div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem;">Click any pill to register or remove a skill:</div>')

currently_selected_set = set(st.session_state.get("current_skills", []))

selected_in_category = st.pills(
    "Select your verified competencies:",
    options=skills_to_show,
    default=[s for s in skills_to_show if s in currently_selected_set],
    selection_mode="multi",
    label_visibility="collapsed"
)

if selected_in_category is not None:
    category_set = set(skills_to_show)
    other_skills = currently_selected_set - category_set
    new_total_skills = sorted(list(other_skills.union(set(selected_in_category))))
    
    if new_total_skills != st.session_state["current_skills"]:
        st.session_state["current_skills"] = new_total_skills
        st.rerun()

user_skills_set = set(st.session_state["current_skills"])
st.caption(f"Currently registered: {len(user_skills_set)} of {len(ALL_SKILLS)} capabilities across all disciplines.")


# -----------------------------------------------------------------------------
# Component 5: Section 03 — Trajectory Synthesis & Roadmap View
# -----------------------------------------------------------------------------
target_role = st.session_state["selected_role"]
path_result = generate_learning_path(user_skills_set, target_role, ROLE_PROFILES, SKILLS_GRAPH)
match_pct = path_result["match_percentage"]
total_weeks = path_result["total_weeks"]
path_steps = path_result["path_steps"]
role_profile = ROLE_PROFILES[target_role]
inr_info = role_profile.get("inr_benchmark", ROLE_INR_BENCHMARKS.get(target_role, {}))

render_clean_html(
    f"""
    <div class="section-header-box" id="roadmap">
        <div class="section-title-editorial">03 / Trajectory & Synthesis</div>
        <div class="section-tag">{target_role}</div>
    </div>
    """
)

if match_pct >= 90:
    tier_desc = "Role Equilibrium · Market Ready"
elif match_pct >= 65:
    tier_desc = "Advanced Alignment · Bridge Missing Specializations"
elif match_pct >= 35:
    tier_desc = "Core Foundation Established · Prerequisite Phase"
elif match_pct > 0:
    tier_desc = "Initial Competencies Acquired"
else:
    tier_desc = "Ground Zero · First-Principles Curriculum"

# Animated Match % & Indian Compensation Banner
components.html(
    f"""
    <div style="font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; background-color: #FAF9F6; border: 1px solid #E2DCD3; border-radius: 4px; padding: 2rem 2.2rem; color: #141413;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #E2DCD3; padding-bottom: 1rem; margin-bottom: 1.5rem;">
            <div>
                <span style="font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #B44A32;">Target Objective</span>
                <h2 style="font-family: 'Instrument Serif', Georgia, serif; font-size: 2.4rem; margin: 0.2rem 0 0 0; font-weight: 400; color: #141413;">{target_role}</h2>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #5E5A54;">Benchmark Compensation (INR)</span>
                <div style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.6rem; color: #B44A32; font-weight: 600;">{inr_info.get('range', '₹10.0 - ₹24.0 LPA')}</div>
                <div style="font-size: 0.74rem; color: #5E5A54;">Fresher: {inr_info.get('entry', '₹6 LPA')} · Senior: {inr_info.get('senior', '₹20+ LPA')}</div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.8rem; align-items: end;">
            <div style="border-right: 1px solid #E2DCD3; padding-right: 1.5rem;">
                <div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #5E5A54; margin-bottom: 0.4rem;">Target Role Match</div>
                <div style="display: flex; align-items: baseline; gap: 0.4rem;">
                    <span id="match-counter" style="font-family: 'Instrument Serif', Georgia, serif; font-size: 3.6rem; line-height: 0.95; color: #B44A32; font-weight: 400;">0</span>
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 2rem; color: #B44A32;">%</span>
                </div>
                <div style="font-size: 0.78rem; color: #5E5A54; margin-top: 0.3rem;">{tier_desc}</div>
            </div>

            <div style="border-right: 1px solid #E2DCD3; padding-right: 1.5rem;">
                <div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #5E5A54; margin-bottom: 0.4rem;">Estimated Duration</div>
                <div style="display: flex; align-items: baseline; gap: 0.4rem;">
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 3.6rem; line-height: 0.95; color: #141413; font-weight: 400;">{total_weeks}</span>
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.5rem; color: #5E5A54;">WEEKS</span>
                </div>
                <div style="font-size: 0.78rem; color: #5E5A54; margin-top: 0.3rem;">Sequential learning curriculum</div>
            </div>

            <div style="border-right: 1px solid #E2DCD3; padding-right: 1.5rem;">
                <div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #5E5A54; margin-bottom: 0.4rem;">Trajectory Scope</div>
                <div style="display: flex; align-items: baseline; gap: 0.4rem;">
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 3.6rem; line-height: 0.95; color: #141413; font-weight: 400;">{len(path_steps)}</span>
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.5rem; color: #5E5A54;">STEPS</span>
                </div>
                <div style="font-size: 0.78rem; color: #5E5A54; margin-top: 0.3rem;">{path_result['acquired_count']} acquired · {path_result['missing_count']} missing</div>
            </div>

            <div>
                <div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #5E5A54; margin-bottom: 0.4rem;">Indian Market Sample</div>
                <div style="display: flex; align-items: baseline; gap: 0.4rem;">
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 3.6rem; line-height: 0.95; color: #141413; font-weight: 400;">{role_profile['total_listings']}</span>
                    <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.5rem; color: #5E5A54;">POSTINGS</span>
                </div>
                <div style="font-size: 0.78rem; color: #5E5A54; margin-top: 0.3rem;">Bengaluru, Hyderabad, Pune & Remote</div>
            </div>
        </div>

        <div style="margin-top: 1.6rem; height: 3px; background-color: #E2DCD3; border-radius: 1.5px; overflow: hidden;">
            <div id="progress-line" style="height: 100%; width: 0%; background-color: #B44A32; transition: width 800ms cubic-bezier(0.22, 1, 0.36, 1);"></div>
        </div>
    </div>

    <script>
    (function animateMetrics() {{
        const targetPct = {match_pct};
        const counterEl = document.getElementById('match-counter');
        const progressEl = document.getElementById('progress-line');
        const duration = 750;
        const startTime = performance.now();

        function easeOutCubic(t) {{
            return 1 - Math.pow(1 - t, 3);
        }}

        function step(now) {{
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedVal = Math.round(easeOutCubic(progress) * targetPct);

            if (counterEl) {{
                counterEl.textContent = easedVal;
            }}

            if (progress < 1) {{
                requestAnimationFrame(step);
            }} else {{
                if (counterEl) counterEl.textContent = targetPct;
            }}
        }}

        requestAnimationFrame(step);

        setTimeout(() => {{
            if (progressEl) {{
                progressEl.style.width = targetPct + '%';
            }}
        }}, 80);
    }})();
    </script>
    """,
    height=265,
)

# -----------------------------------------------------------------------------
# Four Core Interactive Tabs
# -----------------------------------------------------------------------------
tab_timeline, tab_free_vault, tab_graph, tab_evidence = st.tabs([
    "Curriculum Timeline (Step-by-Step)",
    "Free Learning Vault (Role Courses)",
    "Visual Learning Graph (Beginner Friendly)",
    "Market Evidence & Salary Data"
])


# --- TAB 1: BEGINNER-FRIENDLY CURRICULUM TIMELINE ---
with tab_timeline:
    if path_result["status"] == "QUALIFIED":
        render_clean_html(
            f"""
            <div class="mastery-card">
                <div class="mastery-title">Role Equilibrium Achieved</div>
                <div class="mastery-text">
                    You currently satisfy every foundational and specialized competency identified across 
                    our <strong>{role_profile['total_listings']} {target_role}</strong> listings. 
                    Your next recommended trajectory involves staff-level domain depth, architecture stewardship, or lateral discipline mastery.
                </div>
            </div>
            """
        )
    elif not path_steps:
        st.info("No missing skills identified for this configuration.")
    else:
        # Beginner Orientation Guide Box
        render_clean_html(
            """
            <div class="beginner-guide-banner">
                <div class="beginner-guide-title">
                    <span>🧭</span> Beginner's Guide: How to Follow This Roadmap
                </div>
                <div class="beginner-guide-steps">
                    <div class="beginner-step-rule">
                        <strong>1. Learn Strictly in Order</strong>
                        Do not jump to Step 5 before finishing Step 1. Every single step unlocks the concepts for the next one.
                    </div>
                    <div class="beginner-step-rule">
                        <strong>2. Build the Hands-on Project</strong>
                        Watching tutorials alone is not enough. Build the specific beginner milestone project listed in each card.
                    </div>
                    <div class="beginner-step-rule">
                        <strong>3. 100% Free Resources</strong>
                        Every card includes direct links to top-tier free courses (freeCodeCamp, Harvard, Kaggle, MDN). Zero paywalls.
                    </div>
                </div>
            </div>
            """
        )

        st.markdown(
            f"Showing **{len(path_steps)}** sequential learning steps. Each step takes **1 to 3 weeks** (approx. 8–10 hours per week)."
        )

        current_phase = None
        for step in path_steps:
            if step["phase_name"] != current_phase:
                current_phase = step["phase_name"]
                phase_header_html = f"""
                <div style="margin-top: 2rem; margin-bottom: 1rem; border-bottom: 2px solid {step['phase_color']}; padding-bottom: 0.4rem;">
                    <span style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: {step['phase_color']};">
                        {step['phase_name']}
                    </span>
                </div>
                """
                render_clean_html(phase_header_html)

            step_idx = step["step_number"]
            num_str = f"0{step_idx}" if step_idx < 10 else f"{step_idx}"
            
            checklist_html = "".join([
                f'<div class="checklist-item"><span>✓</span> {item}</div>'
                for item in step["topics_checklist"]
            ])
            
            resources_pills_html = "".join([
                f'<a href="{res["url"]}" target="_blank" class="step-resource-pill">🔗 {res["title"]} ({res["provider"]})</a>'
                for res in step["free_resources"]
            ]) or '<span style="color: #8A857C;">Official documentation & community tutorials.</span>'

            prereqs_str = ", ".join(step["satisfied_prereqs"]) if step["satisfied_prereqs"] else "None (Start here directly!)"

            # Render each step card using render_clean_html to avoid code block parsing
            card_html = f"""
            <div class="beginner-step-card">
                <span class="step-phase-tag" style="color: {step['phase_color']};">
                    STEP {num_str} · {step['category']}
                </span>
                <div class="step-heading-row">
                    <div class="step-skill-title">{step['skill']}</div>
                    <div class="step-duration-badge">⏱ Est. {step['estimated_weeks']} Weeks</div>
                </div>
                <div class="step-plain-english">
                    <strong>In Simple Words:</strong> {step['plain_english']}
                </div>
                <div style="font-size: 0.8rem; color: #5E5A54; margin-bottom: 1rem;">
                    <strong>Why Learn This Now:</strong> {step['why_this_skill']} 
                    <span style="color: #8A857C; margin-left: 0.4rem;">(Pre-requisites: {prereqs_str})</span>
                </div>
                <div class="step-grid-details">
                    <div class="checklist-box">
                        <div class="checklist-title">📋 What You Will Master (Checklist):</div>
                        {checklist_html}
                    </div>
                    <div class="project-action-box">
                        <div class="project-action-title">🛠 Hands-on Beginner Project to Build:</div>
                        <div class="project-action-text">{step['beginner_project']}</div>
                    </div>
                </div>
                <div class="step-resources-bar">
                    <span class="step-resources-label">Top Free Learning Links:</span>
                    {resources_pills_html}
                </div>
            </div>
            """
            render_clean_html(card_html)


# --- TAB 2: FREE LEARNING VAULT (ROLE SPECIFIC) ---
with tab_free_vault:
    free_vault = role_profile.get("free_resources", [])
    render_clean_html(
        f"""
        <div style="margin-top: 1rem; margin-bottom: 1.5rem;">
            <div style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.8rem; color: var(--text-primary);">
                The Free Learning Vault for {target_role}
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.55;">
                We have curated the highest-rated free resources on the internet for this exact career track. 
                You do not need to buy expensive bootcamps or paid subscriptions to become job-ready.
            </p>
        </div>
        """
    )

    for res in free_vault:
        res_card_html = f"""
        <div class="resource-card">
            <div>
                <div class="resource-title">{res['title']}</div>
                <div class="resource-meta">
                    <span class="badge-provider">{res['provider']}</span>
                    <span class="badge-free">100% Free</span>
                    <span style="color: #8A857C;">· {res['type']}</span>
                </div>
                <div class="resource-why">{res['why']}</div>
            </div>
            <div>
                <a href="{res['url']}" target="_blank" class="resource-link-btn">
                    Open Free Course ↗
                </a>
            </div>
        </div>
        """
        render_clean_html(res_card_html)


# --- TAB 3: VISUAL LEARNING GRAPH (BEGINNER SUBWAY MAP & STRUCTURED DAG) ---
with tab_graph:
    st.markdown(
        """
        <div style="font-size: 0.88rem; color: var(--text-muted); margin-top: 0.5rem; margin-bottom: 0.8rem;">
            Choose how you want to visualize your learning path:
        </div>
        """,
        unsafe_allow_html=True
    )

    # View Mode Switcher
    view_col1, view_col2 = st.columns([2, 3])
    with view_col1:
        chosen_view = st.radio(
            "Select Graph View:",
            options=["🚇 Metro Subway Line (Beginner Friendly)", "🕸️ Phased Dependency DAG (Full Architecture)"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )

    if "Metro Subway Line" in chosen_view:
        # 1. BEGINNER SUBWAY METRO LINE
        render_clean_html(
            f"""
            <div class="subway-container">
                <div style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.5rem; color: #141413; margin-bottom: 0.3rem;">
                    The {target_role} Learning Metro Line
                </div>
                <p style="font-size: 0.82rem; color: #5E5A54; margin-bottom: 1.5rem;">
                    A clean, linear progression from your first day to market readiness. Follow this line one stop at a time.
                </p>
            """
        )

        # Show completed skills first as "Departed Stations"
        if user_skills_set:
            completed_preview = ", ".join(sorted(list(user_skills_set))[:5])
            if len(user_skills_set) > 5:
                completed_preview += f" (+{len(user_skills_set)-5} more)"
            render_clean_html(
                f"""
                <div class="subway-station-row">
                    <div class="subway-marker-col">
                        <div class="subway-circle" style="background-color: #2E5C3B;">✓</div>
                        <div class="subway-line" style="background-color: #2E5C3B;"></div>
                    </div>
                    <div class="subway-content-card" style="background-color: #EEF4EF; border-color: #D2E4D6;">
                        <span style="font-size: 0.68rem; font-weight: 700; color: #2E5C3B; text-transform: uppercase;">Station 0: Already Acquired</span>
                        <div style="font-size: 1rem; font-weight: 700; color: #1E3B27;">{completed_preview}</div>
                        <div style="font-size: 0.78rem; color: #3A6947;">You have verified these skills. Your journey begins with the next milestone below!</div>
                    </div>
                </div>
                """
            )

        # Show each sequential step on the metro line
        for idx, step in enumerate(path_steps, 1):
            num_str = f"0{idx}" if idx < 10 else f"{idx}"
            is_last = (idx == len(path_steps))
            line_color = step["phase_color"]
            
            render_clean_html(
                f"""
                <div class="subway-station-row">
                    <div class="subway-marker-col">
                        <div class="subway-circle" style="background-color: {line_color};">{num_str}</div>
                        {'<div class="subway-line"></div>' if not is_last else ''}
                    </div>
                    <div class="subway-content-card">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <span style="font-size: 0.68rem; font-weight: 700; color: {line_color}; text-transform: uppercase;">
                                {step['phase_name']} · {step['category']}
                            </span>
                            <span style="font-size: 0.74rem; font-weight: 600; color: #B44A32;">⏱ {step['estimated_weeks']} Weeks</span>
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 700; color: #141413; margin: 0.2rem 0;">{step['skill']}</div>
                        <div style="font-size: 0.82rem; color: #5E5A54; line-height: 1.45;">{step['plain_english']}</div>
                        <div style="font-size: 0.75rem; color: #8A857C; margin-top: 0.4rem;">
                            <strong>Unlocks next:</strong> {step['reason']}
                        </div>
                    </div>
                </div>
                """
            )

        # Terminal Destination Station
        render_clean_html(
            f"""
                <div class="subway-station-row">
                    <div class="subway-marker-col">
                        <div class="subway-circle" style="background-color: #141413;">🎯</div>
                    </div>
                    <div class="subway-content-card" style="background-color: #FAF5F2; border-color: #B44A32;">
                        <span style="font-size: 0.68rem; font-weight: 700; color: #B44A32; text-transform: uppercase;">Final Destination</span>
                        <div style="font-size: 1.15rem; font-weight: 700; color: #141413;">Ready for {target_role} Roles</div>
                        <div style="font-size: 0.82rem; color: #5E5A54;">Complete! Benchmark compensation: <strong>{inr_info.get('range', '')}</strong> in Indian tech hubs.</div>
                    </div>
                </div>
            </div>
            """
        )

    else:
        # 2. STRUCTURED PHASED GRAPHVIZ DAG
        render_clean_html(
            """
            <div style="font-size: 0.82rem; color: #5E5A54; margin-bottom: 1rem;">
                Organized into 4 clear stages: <strong>Your Skills</strong> ➔ <strong>Foundations</strong> ➔ <strong>Core Engineering</strong> ➔ <strong>Target Readiness</strong>.
            </div>
            """
        )

        dot_source = generate_graphviz_dot(
            user_skills_set,
            path_result["target_skills"],
            path_steps,
            SKILLS_GRAPH
        )
        st.graphviz_chart(dot_source, use_container_width=True)


# --- TAB 4: MARKET EVIDENCE & SALARY BENCHMARKS ---
with tab_evidence:
    render_clean_html(
        f"""
        <div style="margin-top: 1rem; margin-bottom: 1.5rem;">
            <div style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.6rem; color: var(--text-primary);">
                Indian Market Evidence & Compensation Spectrum
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.55;">
                Every roadmap milestone is derived from empirical job postings across Indian tech hubs
                (Bengaluru, Hyderabad, Pune, Gurugram, Mumbai, and Remote).
            </p>
        </div>
        """
    )
    
    aud_col1, aud_col2, aud_col3, aud_col4 = st.columns(4)
    with aud_col1:
        st.metric("Raw Postings", AUDIT_SUMMARY["raw_count"])
    with aud_col2:
        st.metric("Cleaned Postings", AUDIT_SUMMARY["clean_count"])
    with aud_col3:
        st.metric("Benchmark Range", inr_info.get("range", "₹12.0 - ₹24.0 LPA"))
    with aud_col4:
        st.metric("Fresher / Junior", inr_info.get("entry", "₹6.0 LPA"))

    st.write("")
    st.subheader(f"Skill Demand Spectrum for {target_role}")
    
    role_metrics_df = pd.DataFrame(role_profile["skills"])[
        ["skill", "tier", "frequency_pct", "count", "category", "estimated_weeks"]
    ].rename(columns={
        "skill": "Skill Name",
        "tier": "Importance Tier",
        "frequency_pct": "Market Frequency (%)",
        "count": "Postings Count",
        "category": "Discipline Category",
        "estimated_weeks": "Est. Weeks"
    })
    st.dataframe(role_metrics_df, use_container_width=True, hide_index=True)

    with st.expander(f"Inspect Cleaned Indian Postings for {target_role} ({role_profile['total_listings']} listings)"):
        role_raw = CLEANED_DF[CLEANED_DF["clean_role"] == target_role][
            ["job_id", "title", "company", "location", "salary_range", "canonical_skills"]
        ].rename(columns={
            "job_id": "Job ID",
            "title": "Posting Title",
            "company": "Company",
            "location": "Location",
            "salary_range": "Salary (INR)",
            "canonical_skills": "Extracted Canonical Skills"
        })
        st.dataframe(role_raw, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# Component 6: Minimalist Atelier Footer
# -----------------------------------------------------------------------------
render_clean_html(
    """
    <div class="editorial-footer">
        <div>
            <span class="footer-brand">CHRONOSKILL</span> · State-Space Career Synthesizer
        </div>
        <div>
            12 Indian Tech Disciplines · 100% Free Curated Vault · No Paywalls
        </div>
    </div>
    """
)
