import os

resumes = {
    "01_junior_frontend_developer.txt": """
Emily Chen
emily.chen@example.com | (415) 555-0192 | San Francisco, CA
github.com/emilychen | linkedin.com/in/emily-chen-frontend

SUMMARY
Creative Junior Frontend Developer with 1.5 years of experience building accessible, responsive Single Page Applications in React, TypeScript, and Tailwind CSS.

SKILLS
Languages: JavaScript, TypeScript, HTML5, CSS3, Python
Frameworks & Libraries: React, Next.js, Redux Toolkit, Tailwind CSS, Jest
Tools: Git, Vite, Figma, Webpack, Postman

EXPERIENCE
Frontend Developer Intern | PixelCraft Studios | 2023 - 2024
• Implemented 8 responsive React components adhering strictly to WCAG AA accessibility standards.
• Reduced client bundle size by 24% by enabling code-splitting and dynamic imports via Vite.
• Collaborated with UI/UX designers in Figma to translate high-fidelity prototypes into pixel-perfect pages.

EDUCATION
B.S. in Interactive Media & Web Development | San Jose State University | 2023 | GPA: 3.7/4.0

PROJECTS
Devfolio - Developer Portfolio Generator
• Built a customizable Markdown-to-portfolio static site generator used by 1,200+ students.
    """,

    "02_senior_backend_fastapi_engineer.txt": """
Marcus Vance
marcus.vance@example.com | (206) 555-8831 | Seattle, WA
github.com/marcusvance | linkedin.com/in/marcus-vance-cloud

SUMMARY
Senior Distributed Systems & Backend Engineer with 7+ years architecting event-driven microservices, high-concurrency APIs, and low-latency database architectures.

SKILLS
Languages: Python, Go, SQL, Bash
Frameworks: FastAPI, Django, gRPC, Celery
Databases: PostgreSQL, Redis, Cassandra, MongoDB
Cloud & DevOps: Docker, Kubernetes, AWS (ECS, S3, RDS, Lambda), Terraform, Kafka

EXPERIENCE
Senior Backend Engineer | StreamMatrix Systems | 2021 - Present
• Architected and maintained 14 microservices in FastAPI and Go processing 450,000 requests per minute.
• Redesigned database indexing and connection pooling, slashing p99 API response latencies by 58% (from 160ms to 67ms).
• Orchestrated zero-downtime database sharding migration for 80 million user transaction records.

Backend Engineer | HyperScale Networks | 2018 - 2021
• Engineered distributed caching layers in Redis, eliminating redundant database roundtrips and trimming AWS RDS bill by $4,200/mo.
• Mentored 6 junior and mid-level software engineers through structured pair programming.

EDUCATION
M.S. in Computer Science | University of Washington | 2018
B.S. in Computer Engineering | Purdue University | 2016
    """,

    "03_machine_learning_researcher.txt": """
Dr. Aisha Patel
aisha.patel@example.com | (617) 555-4421 | Boston, MA
github.com/aishapatel-ml | linkedin.com/in/aisha-patel-ai

SUMMARY
Applied Machine Learning Scientist with expertise in Large Language Models (LLMs), parameter-efficient fine-tuning (LoRA), retrieval-augmented generation (RAG), and transformer inference optimization.

SKILLS
Languages: Python, C++, SQL
ML Frameworks: PyTorch, Hugging Face, LangChain, vLLM, DeepSpeed, Triton
Algorithms: Transformers, Vector Embeddings, Diffusion Models, Reinforcement Learning (DPO/RLHF)
Tools: MLflow, Weights & Biases, Docker, CUDA, Ray

EXPERIENCE
Senior ML Research Scientist | Cognition Intelligence Labs | 2022 - Present
• Spearheaded fine-tuning of 8B open-weight LLMs using QLoRA, outperforming base models on domain reasoning benchmarks by 19.4%.
• Designed low-latency RAG pipeline serving 25,000 queries daily with hybrid HNSW vector search and cross-encoder reranking.
• Reduced model inference time by 44% utilizing vLLM PagedAttention and FP8 quantization.

Machine Learning Engineer | NeuroData AI | 2020 - 2022
• Trained multi-modal classification networks for medical diagnostic imaging achieving 94.6% AUC-ROC.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence) | MIT | 2020
B.Tech in Computer Science | IIT Bombay | 2015
    """,

    "04_data_analyst_bi.txt": """
David Kim
david.kim@example.com | (312) 555-9011 | Chicago, IL
linkedin.com/in/david-kim-analytics

SUMMARY
Data Analyst with 4 years of experience translating massive multi-channel transactional datasets into executive BI dashboards and statistical experimentation insights.

SKILLS
Languages: SQL, Python (Pandas, NumPy, Scikit-learn), R
BI & Tools: Tableau, Power BI, dbt, Snowflake, BigQuery, Excel
Analytics: Cohort Retention, LTV/CAC Modeling, A/B Testing, Funnel Conversion, Hypothesis Testing

EXPERIENCE
Senior Data Analyst | RetailPulse Global | 2022 - Present
• Developed automated revenue forecasting models in Python and dbt, reducing end-of-month financial reconciliation time by 18 hours.
• Designed and analyzed 22 product A/B tests, identifying checkout optimizations that generated $1.4M in incremental annual GMV.
• Built executive Tableau dashboards monitored daily by VP-level leadership for inventory turnover.

Data Analyst | OmniMetrics Corp | 2020 - 2022
• Wrote advanced SQL window functions and CTEs to segment 2 million active mobile shoppers.

EDUCATION
B.S. in Statistics & Data Science | University of Illinois Urbana-Champaign | 2020
    """,

    "05_product_manager_technical.txt": """
Rachel Morrison
rachel.morrison@example.com | (212) 555-3312 | New York, NY
linkedin.com/in/rachel-morrison-pm

SUMMARY
Technical Product Manager with a background in software engineering. Proven track record leading cross-functional squads to ship enterprise B2B SaaS features from 0 to 1.

SKILLS
Product Strategy: Roadmapping, PRD writing, Jobs-To-Be-Done, RICE Prioritization
Technical: REST APIs, SQL, System Architecture, Agile/Scrum, Jira
Analytics: Amplitude, Mixpanel, Google Analytics, User Interviews

EXPERIENCE
Senior Technical Product Manager | CloudForge Platforms | 2021 - Present
• Defined product vision and executed GTM roadmap for enterprise API developer gateway, driving $3.2M ARR in year one.
• Increased 30-day developer onboarding activation rate from 34% to 68% by launching interactive API sandboxes.
• Collaborated with 18 engineers, 2 UX designers, and sales leaders to deliver 4 major quarterly releases on time.

Associate Product Manager | VentureScale Apps | 2019 - 2021
• Managed sprint backlog and user stories for core iOS and Android consumer mobile apps (1M+ downloads).

EDUCATION
B.S. in Computer Science & Business Management | Columbia University | 2019
    """,

    "06_devops_cloud_architect.txt": """
Carlos Santana
carlos.santana@example.com | (512) 555-7729 | Austin, TX
github.com/carlos-cloud | linkedin.com/in/carlos-santana-devops

SUMMARY
DevOps & Cloud Infrastructure Engineer with 6+ years specializing in Kubernetes cluster management, Infrastructure as Code (Terraform), and zero-downtime deployment pipelines.

SKILLS
Cloud: AWS, Google Cloud Platform (GCP)
Containers & Orchestration: Docker, Kubernetes, Helm, ArgoCD
IaC & Config: Terraform, Ansible, CloudFormation
CI/CD: GitHub Actions, GitLab CI, Jenkins
Monitoring: Prometheus, Grafana, Datadog, ELK Stack

EXPERIENCE
Lead DevOps Engineer | ScaleForge Cloud | 2021 - Present
• Migrated 60+ microservices to multi-tenant Amazon EKS clusters, achieving 99.99% infrastructure uptime SLA.
• Authored modular Terraform configurations managing 300+ cloud resources with strict GitOps PR verification.
• Implemented automated Canary deployments with ArgoCD and Istio service mesh, slashing rollout failures to zero.

Site Reliability Engineer | Apex Digital | 2018 - 2021
• Configured Prometheus alerts and Grafana dashboards, reducing Mean Time to Detection (MTTD) from 25 minutes to 4 minutes.

EDUCATION
B.S. in Information Technology & Network Security | Texas A&M University | 2018
CERTIFICATIONS: CKA (Certified Kubernetes Administrator), AWS Solutions Architect Professional
    """,

    "07_embedded_systems_firmware_dev.txt": """
Liam O'Connor
liam.oconnor@example.com | (617) 555-6610 | Cambridge, MA
github.com/liam-embedded | linkedin.com/in/liam-oconnor-firmware

SUMMARY
Embedded Firmware Engineer with 5 years of experience developing low-power real-time operating systems (RTOS), hardware drivers, and sensor communication protocols close to silicon.

SKILLS
Languages: C, C++, Assembly, Python
Protocols: I2C, SPI, UART, CAN, BLE, USB
Hardware/MCUs: ARM Cortex-M, STM32, ESP32, Nordic nRF52
Tools: FreeRTOS, GDB, Oscilloscopes, Logic Analyzers, JTAG, Keil uVision

EXPERIENCE
Embedded Firmware Engineer | BioSense Technologies | 2021 - Present
• Developed bare-metal C device drivers and FreeRTOS tasks for wearable health monitors, extending battery longevity by 32%.
• Implemented robust circular ring buffers and DMA data transfers for continuous real-time ECG telemetry streaming.
• Created secure Over-The-Air (OTA) firmware upgrade mechanism with dual-bank flash partition rollback.

Junior Firmware Developer | Robocraft Automation | 2019 - 2021
• Programmed motor control PID loops and sensor fusion filters on STM32 microcontrollers.

EDUCATION
B.S. in Electrical & Computer Engineering | Northeastern University | 2019
    """,

    "08_cybersecurity_soc_analyst.txt": """
Zainab Al-Mansoor
zainab.mansoor@example.com | (703) 555-8822 | Arlington, VA
linkedin.com/in/zainab-mansoor-sec

SUMMARY
Cybersecurity Analyst with 4+ years of experience in Security Operations Center (SOC) environments, incident response triage, vulnerability management, and threat hunting.

SKILLS
Security: SIEM (Splunk, Microsoft Sentinel), Wireshark, EDR (CrowdStrike Falcon), Snort IDS
Frameworks: MITRE ATT&CK, NIST CSF, OWASP Top 10, ISO 27001
Scripting: Python, PowerShell, Bash
Certifications: CompTIA Security+, CEH (Certified Ethical Hacker), CySA+

EXPERIENCE
Senior SOC Analyst | CyberDefense Federal Solutions | 2022 - Present
• Monitored SIEM correlation rules across 40,000 enterprise endpoints, triaging over 150 daily security events.
• Investigated and neutralized advanced phishing and credential harvesting campaigns, preventing data exfiltration incidents.
• Tuned 35 high-fidelity detection alerts in Splunk, decreasing false positive alarm volume by 46%.

Security Operations Analyst | Vanguard Global Security | 2020 - 2022
• Performed vulnerability scans with Nessus and collaborated with infrastructure teams to remediate CVSS 7+ CVEs.

EDUCATION
B.S. in Cybersecurity & Information Assurance | George Mason University | 2020
    """,

    "09_fullstack_startup_founder.txt": """
Siddharth Rao
sid.rao@example.com | (408) 555-1234 | Sunnyvale, CA
github.com/sidrao | linkedin.com/in/sid-rao-founder

SUMMARY
Versatile Full Stack Founding Engineer with experience scaling web applications from napkin idea to 100k+ active users. Strong command over Next.js, FastAPI, PostgreSQL, and Stripe payment billing.

SKILLS
Frontend: React, Next.js, TypeScript, Tailwind CSS
Backend: Python, FastAPI, Node.js, Express, PostgreSQL, Redis
Infrastructure: Vercel, Supabase, Docker, AWS, Stripe API

EXPERIENCE
Founding Engineer / Co-Founder | ShipFast SaaS | 2022 - Present
• Architected and developed entire web application stack in Next.js 14, FastAPI, and Supabase from scratch in 6 weeks.
• Scaled platform to 125,000 registered users with 99.9% uptime, processing $450k in annual subscription transactions.
• Built asynchronous webhooks and idempotency guards handling 20,000 Stripe webhook events daily.

Full Stack Engineer | EarlyStage Ventures | 2020 - 2022
• Built real-time analytics portals in React and Node.js for venture portfolio monitoring.

EDUCATION
B.S. in Computer Science | UC San Diego | 2020
    """,

    "10_career_switcher_beginner_swe.txt": """
Jessica Taylor
jessica.taylor@example.com | (303) 555-7819 | Denver, CO
github.com/jessicataylor-code | linkedin.com/in/jessica-taylor-dev

SUMMARY
Former high school mathematics teacher turned passionate Software Engineer. Completed 900+ hours of full-stack software development immersion, building algorithmic problem solving and web development projects.

SKILLS
Languages: Python, JavaScript, SQL, HTML5, CSS3
Frameworks & Libraries: React, Node.js, Express, Flask, Bootstrap
Databases: PostgreSQL, SQLite
Tools: Git, GitHub, VS Code, Postman, Heroku

PROJECTS
MathQuest - Interactive Educational STEM App (React, Express, PostgreSQL)
• Built full stack gamified math learning portal featuring 200+ interactive practice challenges.
• Implemented user authentication with JWT and bcrypt password hashing.

ExpenseTracker CLI & Web Portal (Python, Flask, SQLite)
• Developed personal budgeting application with category visualization charts and CSV export capabilities.

WORK EXPERIENCE
High School Mathematics Teacher | Denver Public Schools | 2019 - 2023
• Taught AP Calculus and Statistics to 120+ students annually; achieved 88% AP exam pass rate.
• Formulated clear curriculum milestones, breaking down abstract problem-solving methodologies into structured steps.

EDUCATION
Full-Stack Software Engineering Immersive | General Assembly | 2024
B.A. in Mathematics Education | University of Colorado Boulder | 2019
    """
}

def generate_fixtures():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, "sample_resumes")
    os.makedirs(target_dir, exist_ok=True)

    for filename, content in resumes.items():
        file_path = os.path.join(target_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created fixture: {filename}")

if __name__ == "__main__":
    generate_fixtures()
