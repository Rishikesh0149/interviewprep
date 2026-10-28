ROLES_DATA = [
    {
        "role_key": "software_engineer",
        "title": "Software Engineer (Backend & Full Stack)",
        "category": "Software Engineering",
        "description": "Designs, builds, and maintains scalable server-side systems, microservices, APIs, and modern data architectures.",
        "required_skills": [
            "Python", "JavaScript", "SQL", "Git", "REST APIs", "Data Structures & Algorithms", "Relational Databases", "Object-Oriented Programming"
        ],
        "nice_to_have_skills": [
            "Docker", "Kubernetes", "Redis", "Kafka", "AWS", "CI/CD", "GraphQL", "System Design"
        ],
        "core_competencies": [
            "API Architecture & Microservices",
            "Database Optimization & Indexing",
            "Concurrency & Asynchronous Programming",
            "System Scalability & High Availability",
            "Unit Testing & Clean Code"
        ],
        "typical_interview_rounds": [
            {"round": "1. Recruiter Screen", "focus": "Background, communication, alignment with culture (30m)"},
            {"round": "2. DSA & Problem Solving", "focus": "Algorithms, data structures, edge cases, complexity (45-60m)"},
            {"round": "3. System Design & Architecture", "focus": "Scalability, caching, databases, load balancing (60m)"},
            {"round": "4. Behavioral & STAR Fit", "focus": "Conflict resolution, leadership, project deep-dive (45m)"}
        ]
    },
    {
        "role_key": "frontend_engineer",
        "title": "Frontend Engineer",
        "category": "Web Development",
        "description": "Crafts high-performance, accessible, visually stunning, and responsive user interfaces for modern web applications.",
        "required_skills": [
            "JavaScript", "TypeScript", "React", "HTML5", "CSS3", "Responsive Design", "Git", "Web Performance"
        ],
        "nice_to_have_skills": [
            "Next.js", "Tailwind CSS", "Redux", "GraphQL", "Accessibility (WCAG)", "Vitest / Jest", "WebSockets"
        ],
        "core_competencies": [
            "Component Architecture & State Management",
            "DOM Rendering, Repaints & Performance Optimization",
            "Semantic HTML & WCAG Accessibility",
            "Cross-Browser Compatibility & Mobile Responsiveness",
            "Client-Side Caching & Network Efficiency"
        ],
        "typical_interview_rounds": [
            {"round": "1. Technical Screening", "focus": "JavaScript fundamentals, closures, event loop, CSS layout (45m)"},
            {"round": "2. Live Coding / UI Challenge", "focus": "Build interactive component in React/TS with state & tests (60m)"},
            {"round": "3. Frontend System Architecture", "focus": "Client-side routing, caching, hydration, SSR/CSR trade-offs (60m)"},
            {"round": "4. Culture & Collaboration", "focus": "Cross-functional work with UX designers and backend engineers (45m)"}
        ]
    },
    {
        "role_key": "ml_engineer",
        "title": "Machine Learning Engineer",
        "category": "Artificial Intelligence",
        "description": "Develops, fine-tunes, evaluates, and deploys production machine learning, deep learning, and generative AI systems.",
        "required_skills": [
            "Python", "PyTorch", "TensorFlow", "Pandas", "NumPy", "Scikit-Learn", "SQL", "Linear Algebra & Statistics"
        ],
        "nice_to_have_skills": [
            "LangChain", "Vector Databases", "Hugging Face", "MLOps", "MLflow", "Docker", "CUDA / GPU Acceleration"
        ],
        "core_competencies": [
            "Model Selection, Feature Engineering & Evaluation Metrics",
            "Deep Learning & Transformer Architectures",
            "LLM Fine-Tuning, Prompt Engineering & RAG Pipelines",
            "Production ML Serving & Latency Optimization",
            "Data Drift Detection & Monitoring"
        ],
        "typical_interview_rounds": [
            {"round": "1. ML Fundamentals", "focus": "Loss functions, gradient descent, bias-variance tradeoff, regularization (45m)"},
            {"round": "2. ML Coding & Implementation", "focus": "Implement custom layers/data pipelines in PyTorch/Python (60m)"},
            {"round": "3. Machine Learning System Design", "focus": "Design recommendation systems, search ranking, or LLM agents (60m)"},
            {"round": "4. Behavioral & Applied Research", "focus": "Discussing published papers or real-world model failures (45m)"}
        ]
    },
    {
        "role_key": "data_analyst",
        "title": "Data Analyst",
        "category": "Data & Business Intelligence",
        "description": "Translates raw datasets into actionable commercial insights, executive dashboards, and statistically grounded recommendations.",
        "required_skills": [
            "SQL", "Python", "Excel", "Data Visualization", "Tableau", "Power BI", "Descriptive Statistics", "Business Acumen"
        ],
        "nice_to_have_skills": [
            "R", "dbt", "Snowflake", "A/B Testing", "Cohort Analysis", "BigQuery", "Git"
        ],
        "core_competencies": [
            "Complex SQL (Window Functions, CTEs, Joins, Aggregations)",
            "Statistical Significance & Hypothesis Testing",
            "KPI Definition, Funnel & Churn Analysis",
            "Interactive Dashboard Design & Executive Storytelling",
            "Data Cleaning, Imputation & Integrity Auditing"
        ],
        "typical_interview_rounds": [
            {"round": "1. SQL & Query Assessment", "focus": "Live window functions, multi-table joins, self-joins (45m)"},
            {"round": "2. Business Case Analysis", "focus": "Diagnosing a drop in metric (e.g. conversion down 12%) (45m)"},
            {"round": "3. Product Sense & Metrics", "focus": "Defining OKRs and KPIs for a new product launch (45m)"},
            {"round": "4. Stakeholder Management", "focus": "Communicating technical insights to non-technical leaders (30m)"}
        ]
    },
    {
        "role_key": "product_manager",
        "title": "Product Manager",
        "category": "Product Leadership",
        "description": "Aligns engineering, design, and business teams to discover user problems, define roadmap vision, and ship impactful software.",
        "required_skills": [
            "Product Strategy", "User Research", "Agile / Scrum", "Data-Driven Decision Making", "Wireframing", "Roadmapping", "A/B Testing", "Stakeholder Communication"
        ],
        "nice_to_have_skills": [
            "SQL", "Figma", "Jira", "Growth Modeling", "API Concepts", "GTM Strategy"
        ],
        "core_competencies": [
            "Product Sense & User Empathy",
            "Prioritization Frameworks (RICE, MoSCoW, Kano)",
            "Metric Design (North Star, Counter Metrics)",
            "Technical Empathy with Engineering",
            "Crisis Management & Trade-off Resolution"
        ],
        "typical_interview_rounds": [
            {"round": "1. Product Sense", "focus": "Design an app for elderly travelers or optimize Uber pickup (45m)"},
            {"round": "2. Execution & Metrics", "focus": "Set North Star metrics for YouTube Shorts and diagnose drop-offs (45m)"},
            {"round": "3. Technical & Engineering Collaboration", "focus": "Technical trade-offs, architecture understanding (45m)"},
            {"round": "4. Leadership & Culture", "focus": "Influencing without authority, resolving cross-team friction (45m)"}
        ]
    },
    {
        "role_key": "devops_engineer",
        "title": "DevOps & Cloud Engineer",
        "category": "Infrastructure & Operations",
        "description": "Automates deployments, ensures high reliability, manages cloud infrastructure as code, and maintains CI/CD pipelines.",
        "required_skills": [
            "Linux", "Docker", "Kubernetes", "AWS / Azure / GCP", "CI/CD (GitHub Actions / GitLab)", "Terraform", "Bash / Shell Scripting", "Networking"
        ],
        "nice_to_have_skills": [
            "Ansible", "Prometheus & Grafana", "ArgoCD", "Python / Go", "Security Compliance (SOC2 / ISO)", "Helm"
        ],
        "core_competencies": [
            "Infrastructure as Code (Terraform / CloudFormation)",
            "Container Orchestration & Cluster Management",
            "Zero-Downtime Deployments (Blue-Green, Canary)",
            "Observability, Alerting & Incident Response (SLAs/SLOs/SLIs)",
            "Cloud Security, IAM, and Least Privilege Architecture"
        ],
        "typical_interview_rounds": [
            {"round": "1. Linux & Networking Fundamentals", "focus": "TCP/IP, DNS, processes, file descriptors, troubleshooting (45m)"},
            {"round": "2. Infrastructure as Code & Scripting", "focus": "Write Terraform modules and shell/Python automation (60m)"},
            {"round": "3. Production Architecture & SRE", "focus": "High availability, disaster recovery, incident post-mortems (60m)"},
            {"round": "4. Cross-Functional Operations", "focus": "Working with dev teams on shift-left security and cost optimization (45m)"}
        ]
    },
    {
        "role_key": "embedded_engineer",
        "title": "Systems & Embedded Software Engineer",
        "category": "Systems Engineering",
        "description": "Develops firmware, real-time operating systems (RTOS), hardware drivers, and low-level code close to silicon.",
        "required_skills": [
            "C", "C++", "RTOS", "Embedded Linux", "Microcontrollers (ARM / STM32)", "Protocols (I2C, SPI, UART, CAN)", "Memory Management", "Debugging (GDB, Oscilloscopes)"
        ],
        "nice_to_have_skills": [
            "Rust", "FreeRTOS", "BLE / Zigbee", "DMA", "FPGA basics", "PCB schematic reading"
        ],
        "core_competencies": [
            "Deterministic Real-Time Scheduling & Interrupt Handling",
            "Pointer Arithmetic & Bit Manipulation",
            "Hardware-Software Interface Troubleshooting",
            "Low-Power Optimization & Battery Efficiency",
            "Safety-Critical Systems Standards (ISO 26262 / IEC 61508)"
        ],
        "typical_interview_rounds": [
            {"round": "1. C Language & Pointer Deep-Dive", "focus": "Volatile keyword, memory alignment, ISR constraints (45m)"},
            {"round": "2. Embedded Coding & Bitwise Logic", "focus": "Ring buffers, register manipulation, state machines (60m)"},
            {"round": "3. Hardware Architecture & System Integration", "focus": "Bus arbitration, timing diagrams, DMA transfers (60m)"},
            {"round": "4. Reliability & Testing", "focus": "Watchdog timers, memory leaks, defensive firmware patterns (45m)"}
        ]
    },
    {
        "role_key": "cybersecurity_analyst",
        "title": "Cybersecurity & Security Operations Analyst",
        "category": "Information Security",
        "description": "Protects digital assets, monitors SIEM telemetry for intrusion, performs threat modeling, and responds to active cyber threats.",
        "required_skills": [
            "Network Security", "SIEM (Splunk / Elastic)", "Incident Response", "Vulnerability Assessment", "Firewalls & IDS/IPS", "Wireshark", "Threat Intelligence", "OWASP Top 10"
        ],
        "nice_to_have_skills": [
            "Python / PowerShell Scripting", "MITRE ATT&CK Framework", "Penetration Testing (Kali Linux)", "Cloud Security (AWS IAM / GuardDuty)", "Digital Forensics"
        ],
        "core_competencies": [
            "Packet Analysis & Protocol Anomalies",
            "Incident Triage & Containment Workflows",
            "Vulnerability Scanning & Patch Prioritization (CVSS)",
            "Identity & Access Management (IAM / MFA / SSO)",
            "Security Compliance (NIST, CIS Benchmarks, GDPR)"
        ],
        "typical_interview_rounds": [
            {"round": "1. Networking & Threat Fundamentals", "focus": "OSI model attacks, DNS spoofing, TLS handshakes, phishing vectors (45m)"},
            {"round": "2. Incident Response Scenario", "focus": "Walkthrough investigating an endpoint alert indicating ransomware (60m)"},
            {"round": "3. Security Architecture & Hardening", "focus": "Zero Trust implementation, DMZ segmentation, bastion hosts (60m)"},
            {"round": "4. Ethics & High-Stress Scenarios", "focus": "Breach notification protocol, ethical standards, crisis communication (45m)"}
        ]
    }
]
