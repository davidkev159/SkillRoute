"""
Hand-curated seed catalog for SkillRoute: skills (with a prerequisite DAG),
roles (with skill requirements), and courses. Deliberately scoped to one
domain -- software / data / product careers -- rather than a shallow sweep
across every industry, so every edge here is defensible and explainable.

Single-skill "Foundations of X" courses are generated at the bottom so every
skill has at least one course that teaches it, without hand-typing 67 rows.
"""

# ---------------------------------------------------------------------------
# Skills: (id, name, category)
# ---------------------------------------------------------------------------
SKILLS = [
    # Programming
    ("python", "Python", "Programming"),
    ("javascript", "JavaScript", "Programming"),
    ("typescript", "TypeScript", "Programming"),
    ("sql", "SQL", "Programming"),
    ("java", "Java", "Programming"),
    ("go", "Go", "Programming"),
    ("bash_scripting", "Bash Scripting", "Programming"),
    ("html_css", "HTML & CSS", "Programming"),
    # Data
    ("data_structures_algorithms", "Data Structures & Algorithms", "Data"),
    ("statistics", "Statistics", "Data"),
    ("probability", "Probability", "Data"),
    ("linear_algebra", "Linear Algebra", "Data"),
    ("data_cleaning", "Data Cleaning", "Data"),
    ("data_visualization", "Data Visualization", "Data"),
    ("exploratory_data_analysis", "Exploratory Data Analysis", "Data"),
    ("ab_testing", "A/B Testing", "Data"),
    ("experiment_design", "Experiment Design", "Data"),
    # Machine Learning
    ("ml_fundamentals", "Machine Learning Fundamentals", "Machine Learning"),
    ("deep_learning", "Deep Learning", "Machine Learning"),
    ("nlp", "Natural Language Processing", "Machine Learning"),
    ("computer_vision", "Computer Vision", "Machine Learning"),
    ("model_deployment", "Model Deployment", "Machine Learning"),
    ("feature_engineering", "Feature Engineering", "Machine Learning"),
    ("mlops", "MLOps", "Machine Learning"),
    ("reinforcement_learning", "Reinforcement Learning", "Machine Learning"),
    # Data Engineering
    ("etl_pipelines", "ETL Pipelines", "Data Engineering"),
    ("data_warehousing", "Data Warehousing", "Data Engineering"),
    ("apache_spark", "Apache Spark", "Data Engineering"),
    ("apache_airflow", "Apache Airflow", "Data Engineering"),
    ("kafka", "Kafka", "Data Engineering"),
    ("data_modeling", "Data Modeling", "Data Engineering"),
    ("database_design", "Database Design", "Data Engineering"),
    # Infrastructure
    ("docker", "Docker", "Infrastructure"),
    ("kubernetes", "Kubernetes", "Infrastructure"),
    ("ci_cd", "CI/CD", "Infrastructure"),
    ("cloud_infrastructure_aws", "Cloud Infrastructure (AWS)", "Infrastructure"),
    ("terraform", "Terraform", "Infrastructure"),
    ("linux_administration", "Linux Administration", "Infrastructure"),
    ("networking_fundamentals", "Networking Fundamentals", "Infrastructure"),
    ("monitoring_observability", "Monitoring & Observability", "Infrastructure"),
    ("incident_response", "Incident Response", "Infrastructure"),
    # Web
    ("react", "React", "Web"),
    ("state_management", "State Management", "Web"),
    ("web_accessibility", "Web Accessibility", "Web"),
    # Backend
    ("system_design", "System Design", "Backend"),
    ("microservices", "Microservices", "Backend"),
    ("rest_api_design", "REST API Design", "Backend"),
    ("graphql", "GraphQL", "Backend"),
    ("caching_strategies", "Caching Strategies", "Backend"),
    ("message_queues", "Message Queues", "Backend"),
    ("api_security", "API Security", "Backend"),
    # Leadership
    ("technical_communication", "Technical Communication", "Leadership"),
    ("code_review", "Code Review", "Leadership"),
    ("mentoring", "Mentoring", "Leadership"),
    ("project_planning", "Project Planning", "Leadership"),
    ("stakeholder_management", "Stakeholder Management", "Leadership"),
    ("cross_functional_collaboration", "Cross-functional Collaboration", "Leadership"),
    ("team_leadership", "Team Leadership", "Leadership"),
    ("hiring_interviewing", "Hiring & Interviewing", "Leadership"),
    ("roadmapping", "Roadmapping", "Leadership"),
    # QA
    ("test_case_design", "Test Case Design", "QA"),
    ("manual_testing", "Manual Testing", "QA"),
    ("test_automation", "Test Automation", "QA"),
    ("performance_testing", "Performance Testing", "QA"),
    # Product
    ("product_analytics", "Product Analytics", "Product"),
    ("user_research", "User Research", "Product"),
    ("prioritization_frameworks", "Prioritization Frameworks", "Product"),
]

# ---------------------------------------------------------------------------
# Skill prerequisite DAG: (skill_id, requires_skill_id)
# (skill)-[:REQUIRES]->(prerequisite). Chains run up to 4-5 levels deep,
# e.g. nlp -> deep_learning -> ml_fundamentals -> statistics -> probability.
# ---------------------------------------------------------------------------
SKILL_PREREQUISITES = [
    ("deep_learning", "ml_fundamentals"),
    ("nlp", "deep_learning"),
    ("computer_vision", "deep_learning"),
    ("reinforcement_learning", "deep_learning"),
    ("reinforcement_learning", "probability"),
    ("ml_fundamentals", "statistics"),
    ("ml_fundamentals", "linear_algebra"),
    ("ml_fundamentals", "python"),
    ("statistics", "probability"),
    ("model_deployment", "docker"),
    ("model_deployment", "ml_fundamentals"),
    ("mlops", "model_deployment"),
    ("mlops", "ml_fundamentals"),
    ("feature_engineering", "data_cleaning"),
    ("feature_engineering", "statistics"),
    ("ab_testing", "experiment_design"),
    ("ab_testing", "statistics"),
    ("experiment_design", "statistics"),
    ("exploratory_data_analysis", "data_cleaning"),
    ("exploratory_data_analysis", "statistics"),
    ("data_cleaning", "sql"),
    ("data_visualization", "data_cleaning"),
    ("apache_spark", "python"),
    ("apache_spark", "sql"),
    ("apache_airflow", "python"),
    ("apache_airflow", "etl_pipelines"),
    ("etl_pipelines", "sql"),
    ("etl_pipelines", "data_modeling"),
    ("data_warehousing", "data_modeling"),
    ("data_warehousing", "sql"),
    ("data_modeling", "database_design"),
    ("database_design", "sql"),
    ("kafka", "networking_fundamentals"),
    ("kafka", "linux_administration"),
    ("docker", "linux_administration"),
    ("kubernetes", "docker"),
    ("kubernetes", "linux_administration"),
    ("ci_cd", "docker"),
    ("ci_cd", "bash_scripting"),
    ("terraform", "cloud_infrastructure_aws"),
    ("terraform", "linux_administration"),
    ("cloud_infrastructure_aws", "networking_fundamentals"),
    ("cloud_infrastructure_aws", "linux_administration"),
    ("monitoring_observability", "kubernetes"),
    ("incident_response", "monitoring_observability"),
    ("system_design", "data_structures_algorithms"),
    ("system_design", "database_design"),
    ("microservices", "system_design"),
    ("microservices", "rest_api_design"),
    ("caching_strategies", "system_design"),
    ("message_queues", "system_design"),
    ("api_security", "rest_api_design"),
    ("rest_api_design", "database_design"),
    ("graphql", "rest_api_design"),
    ("react", "javascript"),
    ("react", "html_css"),
    ("state_management", "react"),
    ("web_accessibility", "html_css"),
    ("typescript", "javascript"),
    ("test_automation", "manual_testing"),
    ("test_automation", "python"),
    ("manual_testing", "test_case_design"),
    ("performance_testing", "test_automation"),
    ("code_review", "technical_communication"),
    ("mentoring", "code_review"),
    ("team_leadership", "mentoring"),
    ("team_leadership", "project_planning"),
    ("hiring_interviewing", "team_leadership"),
    ("roadmapping", "stakeholder_management"),
    ("roadmapping", "prioritization_frameworks"),
    ("prioritization_frameworks", "product_analytics"),
    ("product_analytics", "sql"),
    ("product_analytics", "data_visualization"),
    ("user_research", "stakeholder_management"),
    ("cross_functional_collaboration", "technical_communication"),
]

# ---------------------------------------------------------------------------
# Roles: (id, title, level, description)
# ---------------------------------------------------------------------------
ROLES = [
    ("jr_software_engineer", "Junior Software Engineer", "Entry",
     "Builds well-scoped features under review, learning the codebase and team conventions."),
    ("software_engineer", "Software Engineer", "Mid",
     "Owns features end-to-end, from design through deployment, with light oversight."),
    ("senior_software_engineer", "Senior Software Engineer", "Senior",
     "Leads technical design for multi-service features and mentors less experienced engineers."),
    ("staff_software_engineer", "Staff Software Engineer", "Lead",
     "Sets technical direction across teams and de-risks the org's hardest architectural bets."),
    ("engineering_manager", "Engineering Manager", "Lead",
     "Leads a team of engineers: hiring, roadmap, and delivery, while staying technically credible."),
    ("jr_data_analyst", "Junior Data Analyst", "Entry",
     "Writes SQL and builds dashboards to answer well-defined business questions."),
    ("data_analyst", "Data Analyst", "Mid",
     "Independently scopes analyses, partners with stakeholders, and communicates findings."),
    ("senior_data_analyst", "Senior Data Analyst", "Senior",
     "Designs experiments and owns the analytics roadmap for a product area."),
    ("data_engineer", "Data Engineer", "Mid",
     "Builds and maintains the pipelines and warehouses the rest of the org depends on."),
    ("senior_data_engineer", "Senior Data Engineer", "Senior",
     "Designs large-scale data platforms and sets standards for pipeline reliability."),
    ("ml_engineer", "Machine Learning Engineer", "Mid",
     "Takes models from notebook to production, owning training and serving pipelines."),
    ("senior_ml_engineer", "Senior Machine Learning Engineer", "Senior",
     "Designs ML systems end-to-end and owns MLOps practice for a team."),
    ("data_scientist", "Data Scientist", "Mid",
     "Turns ambiguous business questions into models and experiments with measurable impact."),
    ("senior_data_scientist", "Senior Data Scientist", "Senior",
     "Leads high-stakes experimentation and modeling work with organization-wide visibility."),
    ("devops_engineer", "DevOps Engineer", "Mid",
     "Builds and operates the deployment pipeline and cloud infrastructure."),
    ("site_reliability_engineer", "Site Reliability Engineer", "Senior",
     "Owns production reliability: on-call, incident response, and observability."),
    ("product_manager", "Product Manager", "Mid",
     "Sets product priorities, defines requirements, and aligns engineering and design."),
    ("frontend_engineer", "Frontend Engineer", "Mid",
     "Builds accessible, maintainable user interfaces and owns client-side architecture."),
    ("backend_engineer", "Backend Engineer", "Mid",
     "Designs and builds the APIs and services that power the product."),
    ("qa_engineer", "QA Engineer", "Entry",
     "Designs test plans and automation to catch regressions before customers do."),
]

# ---------------------------------------------------------------------------
# Role requirements: (role_id, skill_id, min_level 1-5, importance)
# importance in {"core", "important", "nice-to-have"}
# ---------------------------------------------------------------------------
ROLE_REQUIREMENTS = [
    ("jr_software_engineer", "python", 3, "core"),
    ("jr_software_engineer", "javascript", 2, "important"),
    ("jr_software_engineer", "data_structures_algorithms", 3, "core"),
    ("jr_software_engineer", "database_design", 2, "important"),
    ("jr_software_engineer", "technical_communication", 2, "important"),

    ("software_engineer", "python", 4, "core"),
    ("software_engineer", "data_structures_algorithms", 4, "core"),
    ("software_engineer", "system_design", 3, "important"),
    ("software_engineer", "rest_api_design", 3, "core"),
    ("software_engineer", "database_design", 3, "important"),
    ("software_engineer", "code_review", 3, "important"),
    ("software_engineer", "ci_cd", 2, "nice-to-have"),

    ("senior_software_engineer", "system_design", 5, "core"),
    ("senior_software_engineer", "microservices", 4, "important"),
    ("senior_software_engineer", "code_review", 4, "core"),
    ("senior_software_engineer", "mentoring", 3, "important"),
    ("senior_software_engineer", "technical_communication", 4, "core"),
    ("senior_software_engineer", "caching_strategies", 3, "nice-to-have"),

    ("staff_software_engineer", "system_design", 5, "core"),
    ("staff_software_engineer", "team_leadership", 4, "core"),
    ("staff_software_engineer", "roadmapping", 3, "important"),
    ("staff_software_engineer", "mentoring", 5, "core"),
    ("staff_software_engineer", "cross_functional_collaboration", 4, "important"),

    ("engineering_manager", "team_leadership", 5, "core"),
    ("engineering_manager", "hiring_interviewing", 4, "core"),
    ("engineering_manager", "stakeholder_management", 4, "core"),
    ("engineering_manager", "roadmapping", 4, "important"),
    ("engineering_manager", "mentoring", 4, "important"),
    ("engineering_manager", "project_planning", 4, "important"),

    ("jr_data_analyst", "sql", 3, "core"),
    ("jr_data_analyst", "data_cleaning", 2, "important"),
    ("jr_data_analyst", "data_visualization", 2, "important"),
    ("jr_data_analyst", "statistics", 2, "core"),
    ("jr_data_analyst", "technical_communication", 2, "nice-to-have"),

    ("data_analyst", "sql", 4, "core"),
    ("data_analyst", "data_visualization", 3, "core"),
    ("data_analyst", "exploratory_data_analysis", 3, "important"),
    ("data_analyst", "statistics", 3, "core"),
    ("data_analyst", "stakeholder_management", 2, "nice-to-have"),

    ("senior_data_analyst", "ab_testing", 4, "core"),
    ("senior_data_analyst", "experiment_design", 4, "important"),
    ("senior_data_analyst", "product_analytics", 3, "important"),
    ("senior_data_analyst", "statistics", 4, "core"),
    ("senior_data_analyst", "mentoring", 2, "nice-to-have"),

    ("data_engineer", "sql", 4, "core"),
    ("data_engineer", "python", 4, "core"),
    ("data_engineer", "etl_pipelines", 4, "core"),
    ("data_engineer", "data_modeling", 3, "important"),
    ("data_engineer", "apache_spark", 3, "important"),
    ("data_engineer", "data_warehousing", 3, "important"),

    ("senior_data_engineer", "apache_spark", 4, "core"),
    ("senior_data_engineer", "apache_airflow", 4, "core"),
    ("senior_data_engineer", "data_warehousing", 4, "core"),
    ("senior_data_engineer", "kafka", 3, "important"),
    ("senior_data_engineer", "system_design", 3, "important"),
    ("senior_data_engineer", "mentoring", 2, "nice-to-have"),

    ("ml_engineer", "python", 4, "core"),
    ("ml_engineer", "ml_fundamentals", 4, "core"),
    ("ml_engineer", "feature_engineering", 3, "important"),
    ("ml_engineer", "model_deployment", 3, "core"),
    ("ml_engineer", "docker", 2, "important"),
    ("ml_engineer", "statistics", 3, "important"),

    ("senior_ml_engineer", "deep_learning", 4, "core"),
    ("senior_ml_engineer", "mlops", 4, "core"),
    ("senior_ml_engineer", "model_deployment", 4, "core"),
    ("senior_ml_engineer", "system_design", 3, "important"),
    ("senior_ml_engineer", "mentoring", 3, "nice-to-have"),

    ("data_scientist", "statistics", 4, "core"),
    ("data_scientist", "ml_fundamentals", 4, "core"),
    ("data_scientist", "exploratory_data_analysis", 4, "core"),
    ("data_scientist", "ab_testing", 3, "important"),
    ("data_scientist", "python", 4, "core"),
    ("data_scientist", "data_visualization", 3, "important"),

    ("senior_data_scientist", "deep_learning", 4, "important"),
    ("senior_data_scientist", "experiment_design", 4, "core"),
    ("senior_data_scientist", "mlops", 3, "nice-to-have"),
    ("senior_data_scientist", "mentoring", 3, "important"),
    ("senior_data_scientist", "statistics", 5, "core"),

    ("devops_engineer", "docker", 4, "core"),
    ("devops_engineer", "kubernetes", 4, "core"),
    ("devops_engineer", "ci_cd", 4, "core"),
    ("devops_engineer", "cloud_infrastructure_aws", 3, "important"),
    ("devops_engineer", "linux_administration", 4, "core"),
    ("devops_engineer", "bash_scripting", 3, "important"),

    ("site_reliability_engineer", "kubernetes", 5, "core"),
    ("site_reliability_engineer", "monitoring_observability", 5, "core"),
    ("site_reliability_engineer", "incident_response", 4, "core"),
    ("site_reliability_engineer", "terraform", 3, "important"),
    ("site_reliability_engineer", "system_design", 3, "important"),

    ("product_manager", "stakeholder_management", 4, "core"),
    ("product_manager", "prioritization_frameworks", 4, "core"),
    ("product_manager", "product_analytics", 3, "important"),
    ("product_manager", "user_research", 3, "important"),
    ("product_manager", "roadmapping", 4, "core"),
    ("product_manager", "technical_communication", 3, "important"),

    ("frontend_engineer", "javascript", 4, "core"),
    ("frontend_engineer", "react", 4, "core"),
    ("frontend_engineer", "html_css", 4, "core"),
    ("frontend_engineer", "typescript", 3, "important"),
    ("frontend_engineer", "state_management", 3, "important"),
    ("frontend_engineer", "web_accessibility", 2, "nice-to-have"),

    ("backend_engineer", "java", 3, "important"),
    ("backend_engineer", "rest_api_design", 4, "core"),
    ("backend_engineer", "database_design", 4, "core"),
    ("backend_engineer", "system_design", 3, "important"),
    ("backend_engineer", "microservices", 3, "important"),
    ("backend_engineer", "api_security", 2, "nice-to-have"),

    ("qa_engineer", "test_case_design", 3, "core"),
    ("qa_engineer", "manual_testing", 3, "core"),
    ("qa_engineer", "test_automation", 3, "important"),
    ("qa_engineer", "python", 2, "nice-to-have"),
    ("qa_engineer", "performance_testing", 2, "nice-to-have"),
]

# ---------------------------------------------------------------------------
# Hand-curated multi-skill "combo" courses: (id, title, provider, hours, level, [(skill_id, level_gain), ...])
# ---------------------------------------------------------------------------
COMBO_COURSES = [
    ("course_data_eng_bootcamp", "Full-Stack Data Engineering Bootcamp", "DataCamp", 40, "Advanced",
     [("etl_pipelines", 3), ("apache_airflow", 3), ("data_warehousing", 2)]),
    ("course_cloud_native_devops", "Cloud-Native DevOps with Docker & Kubernetes", "A Cloud Guru", 30, "Intermediate",
     [("docker", 3), ("kubernetes", 3), ("ci_cd", 2)]),
    ("course_modern_frontend", "Modern Frontend Engineering", "Frontend Masters", 25, "Intermediate",
     [("react", 3), ("typescript", 2), ("state_management", 3)]),
    ("course_applied_ml_python", "Applied Machine Learning in Python", "Coursera", 35, "Intermediate",
     [("ml_fundamentals", 3), ("feature_engineering", 2), ("model_deployment", 2)]),
    ("course_stats_for_analysts", "Statistics & Experimentation for Analysts", "Coursera", 20, "Intermediate",
     [("statistics", 3), ("experiment_design", 2), ("ab_testing", 2)]),
    ("course_sql_data_modeling", "SQL & Data Modeling Bootcamp", "Udemy", 18, "Beginner",
     [("sql", 3), ("database_design", 2), ("data_modeling", 2)]),
    ("course_eng_leadership", "Engineering Leadership Accelerator", "O'Reilly Learning", 12, "Intermediate",
     [("mentoring", 2), ("team_leadership", 3), ("project_planning", 2)]),
    ("course_sre_fundamentals", "Site Reliability Engineering Fundamentals", "A Cloud Guru", 28, "Advanced",
     [("monitoring_observability", 3), ("incident_response", 3), ("kubernetes", 2)]),
    ("course_backend_system_design", "Backend System Design Masterclass", "Educative", 24, "Advanced",
     [("system_design", 3), ("microservices", 3), ("caching_strategies", 2)]),
    ("course_product_mgmt_essentials", "Product Management Essentials", "Coursera", 15, "Beginner",
     [("stakeholder_management", 2), ("prioritization_frameworks", 3), ("roadmapping", 2)]),
    ("course_qa_automation_bootcamp", "QA & Test Automation Bootcamp", "Udemy", 16, "Beginner",
     [("test_case_design", 2), ("manual_testing", 2), ("test_automation", 3)]),
    ("course_deep_learning_specialization", "Deep Learning Specialization", "Coursera", 45, "Advanced",
     [("deep_learning", 3), ("nlp", 2), ("computer_vision", 2)]),
    ("course_aws_terraform", "Cloud Infrastructure with AWS & Terraform", "A Cloud Guru", 22, "Intermediate",
     [("cloud_infrastructure_aws", 3), ("terraform", 3), ("networking_fundamentals", 2)]),
    ("course_api_design_security", "API Design & Security", "Educative", 14, "Intermediate",
     [("rest_api_design", 3), ("api_security", 2), ("graphql", 2)]),
    ("course_mlops_production", "MLOps in Production", "Pluralsight", 26, "Advanced",
     [("mlops", 3), ("model_deployment", 2), ("docker", 2)]),
]


def build_foundation_courses() -> list[tuple]:
    """One beginner-friendly course per skill, so every skill has at least
    one covering course even if it's not part of a combo above. Duration is
    shorter for leadership/soft skills, longer for deep technical skills."""
    providers = ["Coursera", "Udemy", "Pluralsight", "edX", "SkillRoute Academy"]
    short_categories = {"Leadership", "Product", "QA"}
    courses = []
    for i, (skill_id, name, category) in enumerate(SKILLS):
        hours = 6 if category in short_categories else 10
        provider = providers[i % len(providers)]
        courses.append((
            f"course_foundations_{skill_id}",
            f"Foundations of {name}",
            provider,
            hours,
            "Beginner",
            [(skill_id, 2)],
        ))
    return courses


def all_courses() -> list[tuple]:
    return COMBO_COURSES + build_foundation_courses()
