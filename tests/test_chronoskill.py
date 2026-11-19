"""
Unit test suite for ChronoSkill.
Verifies dataset cleaning, DAG acyclicity, topological sort ordering,
role profiling, edge cases, and graph visualization generation.
"""

import os
import sys

# Ensure repository root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from data.skills_graph import (
    SKILLS_GRAPH,
    SKILL_ALIAS_MAP,
    normalize_skill_token,
    clean_job_dataset,
    compute_role_profiles,
    calculate_prerequisite_depth,
    generate_learning_path,
    generate_graphviz_dot,
)

EXPECTED_ROLES = [
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


def test_alias_normalization():
    """Verify that messy skill aliases map to canonical skill names."""
    assert normalize_skill_token("py") == "Python"
    assert normalize_skill_token("python3") == "Python"
    assert normalize_skill_token("JS") == "JavaScript"
    assert normalize_skill_token("k8s") == "Kubernetes"
    assert normalize_skill_token("postgres") == "Relational Databases"
    assert normalize_skill_token("aws cloud") == "Cloud (AWS)"
    assert normalize_skill_token("sklearn") == "Scikit-Learn"
    assert normalize_skill_token("  React.js  ") == "React"
    assert normalize_skill_token("n/a") is None
    assert normalize_skill_token("") is None


def test_dag_acyclicity_and_validity():
    """Verify that SKILLS_GRAPH is a valid Directed Acyclic Graph (DAG) with valid references."""
    # 1. All prerequisites must be registered nodes
    for skill, data in SKILLS_GRAPH.items():
        for prereq in data["prerequisites"]:
            assert prereq in SKILLS_GRAPH, f"Prerequisite '{prereq}' of '{skill}' is not in SKILLS_GRAPH!"

    # 2. Cycle detection via DFS
    visited = {}  # 0: unvisited, 1: visiting, 2: visited

    def dfs(node):
        visited[node] = 1
        for p in SKILLS_GRAPH[node]["prerequisites"]:
            if visited.get(p) == 1:
                raise AssertionError(f"Cycle detected between '{node}' and '{p}'")
            if visited.get(p, 0) == 0:
                dfs(p)
        visited[node] = 2

    for node in SKILLS_GRAPH:
        if visited.get(node, 0) == 0:
            dfs(node)


def test_dataset_cleaning_and_audit():
    """Verify data cleaning logic, deduplication, and anomaly rejection."""
    raw_df = pd.read_csv("data/job_listings.csv")
    assert len(raw_df) >= 300, "Raw dataset should contain at least 300 listings."
    
    cleaned_df, audit = clean_job_dataset(raw_df)
    
    # Audit assertions
    assert audit["clean_count"] >= 300
    assert audit["dropped_duplicates"] > 0, "Expected duplicates to be pruned"
    assert audit["dropped_missing_fields"] > 0, "Expected corrupted rows to be pruned"
    
    # Check that canonical_skills are all valid
    for skill_list in cleaned_df["canonical_skills"]:
        assert len(skill_list) > 0
        for s in skill_list:
            assert s in SKILLS_GRAPH


def test_role_profiles_coverage():
    """Verify that all 8 required roles are computed with non-empty metrics."""
    raw_df = pd.read_csv("data/job_listings.csv")
    cleaned_df, _ = clean_job_dataset(raw_df)
    profiles = compute_role_profiles(cleaned_df)
    
    for expected_role in EXPECTED_ROLES:
        assert expected_role in profiles, f"Missing role profile for {expected_role}"
        prof = profiles[expected_role]
        assert prof["total_listings"] > 20
        assert len(prof["skills"]) >= 5
        assert len(prof["top_core_skills"]) >= 3


def test_path_engine_edge_case_empty_skills():
    """Empty skill selection should return 0% match and schedule foundations first."""
    raw_df = pd.read_csv("data/job_listings.csv")
    cleaned_df, _ = clean_job_dataset(raw_df)
    profiles = compute_role_profiles(cleaned_df)

    for role in EXPECTED_ROLES:
        result = generate_learning_path(set(), role, profiles, SKILLS_GRAPH)
        assert result["status"] == "IN_PROGRESS"
        assert result["match_percentage"] == 0
        assert result["total_weeks"] > 0
        assert len(result["path_steps"]) > 0

        # Foundational check: the first step in empty state must have 0 unsatisfied prerequisites
        first_step = result["path_steps"][0]
        prereqs = SKILLS_GRAPH[first_step["skill"]]["prerequisites"]
        assert len(prereqs) == 0, f"First step '{first_step['skill']}' in empty path has prerequisites {prereqs}"


def test_path_engine_edge_case_already_qualified():
    """User with all skills should return 100% match and QUALIFIED status."""
    raw_df = pd.read_csv("data/job_listings.csv")
    cleaned_df, _ = clean_job_dataset(raw_df)
    profiles = compute_role_profiles(cleaned_df)

    all_skills = set(SKILLS_GRAPH.keys())
    for role in EXPECTED_ROLES:
        result = generate_learning_path(all_skills, role, profiles, SKILLS_GRAPH)
        assert result["status"] == "QUALIFIED"
        assert result["match_percentage"] == 100
        assert result["total_weeks"] == 0
        assert len(result["path_steps"]) == 0


def test_topological_sort_invariant():
    """Verify that every step's prerequisites always appear before it in the path."""
    raw_df = pd.read_csv("data/job_listings.csv")
    cleaned_df, _ = clean_job_dataset(raw_df)
    profiles = compute_role_profiles(cleaned_df)

    # Test with partial skill sets
    test_cases = [
        ("ML Engineer", {"Python"}),
        ("Backend Developer", {"Git", "SQL"}),
        ("Frontend Developer", {"HTML & CSS"}),
        ("DevOps Engineer", {"Linux"}),
        ("Cybersecurity Analyst", {"Networking"}),
    ]

    for role, user_skills in test_cases:
        result = generate_learning_path(user_skills, role, profiles, SKILLS_GRAPH)
        steps = [step["skill"] for step in result["path_steps"]]

        # Check topological ordering invariant:
        # For each step S at index i, every prerequisite of S must either be in user_skills or appear at index < i
        known = set(user_skills)
        for s in steps:
            for p in SKILLS_GRAPH[s]["prerequisites"]:
                assert p in known, f"Prerequisite '{p}' of '{s}' violated topological ordering in role '{role}'"
            known.add(s)


def test_graphviz_dot_syntax():
    """Verify Graphviz DOT string formatting and element styles."""
    user_skills = {"Python", "SQL"}
    target_skills = {"Machine Learning", "Pandas"}
    path_steps = [
        {"skill": "Pandas", "step_number": 1},
        {"skill": "Machine Learning", "step_number": 2}
    ]

    dot = generate_graphviz_dot(user_skills, target_skills, path_steps, SKILLS_GRAPH)
    assert dot.startswith("digraph ChronoSkill {")
    assert dot.endswith("}")
    assert 'rankdir="LR"' in dot
    assert '"Python"' in dot
    assert 'fillcolor="#E5EBE3"' in dot  # Acquired styling
    assert 'fillcolor="#FAF1ED"' in dot  # Roadmap styling


if __name__ == "__main__":
    print("Running ChronoSkill unit tests...")
    test_alias_normalization()
    print("✓ test_alias_normalization passed.")
    test_dag_acyclicity_and_validity()
    print("✓ test_dag_acyclicity_and_validity passed.")
    test_dataset_cleaning_and_audit()
    print("✓ test_dataset_cleaning_and_audit passed.")
    test_role_profiles_coverage()
    print("✓ test_role_profiles_coverage passed.")
    test_path_engine_edge_case_empty_skills()
    print("✓ test_path_engine_edge_case_empty_skills passed.")
    test_path_engine_edge_case_already_qualified()
    print("✓ test_path_engine_edge_case_already_qualified passed.")
    test_topological_sort_invariant()
    print("✓ test_topological_sort_invariant passed.")
    test_graphviz_dot_syntax()
    print("✓ test_graphviz_dot_syntax passed.")
    print("\nALL 8 TEST SUITES PASSED PERFECTLY!")

