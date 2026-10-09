import re
import spacy

nlp = spacy.load("en_core_web_sm")


# Skill aliases:
# Different ways of writing the same skill are normalized
# to one standard skill name.
SKILL_ALIASES = {

    # =========================
    # Programming Languages
    # =========================
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "c sharp": "C#",
    "r programming": "R",
    "golang": "Go",
    "go programming": "Go",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "rust": "Rust",
    "php": "PHP",
    "ruby": "Ruby",
    "scala": "Scala",
    "dart": "Dart",
    "matlab": "MATLAB",

    # =========================
    # Web Development
    # =========================
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "angular": "Angular",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express.js": "Express.js",
    "expressjs": "Express.js",
    "bootstrap": "Bootstrap",
    "tailwind": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",

    # =========================
    # Backend / APIs
    # =========================
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "rest api": "REST API",
    "rest apis": "REST API",
    "graphql": "GraphQL",
    "microservices": "Microservices",

    # =========================
    # Databases / SQL
    # =========================
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "oracle": "Oracle Database",
    "oracle database": "Oracle Database",
    "sqlite": "SQLite",
    "redis": "Redis",
    "mariadb": "MariaDB",
    "nosql": "NoSQL",
    "database management": "Database Management",

    # =========================
    # Data Analysis
    # =========================
    "excel": "Excel",
    "microsoft excel": "Excel",
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "tableau": "Tableau",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analytics",
    "data visualization": "Data Visualization",
    "business intelligence": "Business Intelligence",
    "statistics": "Statistics",
    "statistical analysis": "Statistical Analysis",

    # =========================
    # AI / Machine Learning
    # =========================
    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "natural language processing": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "computer vision": "Computer Vision",
    "generative ai": "Generative AI",
    "gen ai": "Generative AI",
    "large language models": "Large Language Models",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "prompt engineering": "Prompt Engineering",
    "rag": "RAG",
    "retrieval augmented generation": "RAG",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "keras": "Keras",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "hugging face": "Hugging Face",
    "transformers": "Transformers",
    "opencv": "OpenCV",

    # =========================
    # Cloud
    # =========================
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Microsoft Azure",
    "microsoft azure": "Microsoft Azure",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "cloud computing": "Cloud Computing",
    "serverless": "Serverless",

    # =========================
    # DevOps / Infrastructure
    # =========================
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "jenkins": "Jenkins",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "devops": "DevOps",
    "linux": "Linux",
    "unix": "Unix",

    # =========================
    # Cybersecurity
    # =========================
    "cybersecurity": "Cybersecurity",
    "cyber security": "Cybersecurity",
    "network security": "Network Security",
    "ethical hacking": "Ethical Hacking",
    "penetration testing": "Penetration Testing",
    "penetration test": "Penetration Testing",
    "vulnerability assessment": "Vulnerability Assessment",
    "information security": "Information Security",
    "application security": "Application Security",
    "iam": "Identity and Access Management",
    "identity and access management": "Identity and Access Management",
    "cryptography": "Cryptography",

    # =========================
    # Networking
    # =========================
    "computer networks": "Computer Networks",
    "networking": "Networking",
    "tcp/ip": "TCP/IP",
    "dns": "DNS",
    "http": "HTTP",
    "https": "HTTPS",
    "vpn": "VPN",
    "firewalls": "Firewalls",
    "firewall": "Firewalls",

    # =========================
    # Testing / QA
    # =========================
    "software testing": "Software Testing",
    "manual testing": "Manual Testing",
    "automation testing": "Automation Testing",
    "selenium": "Selenium",
    "cypress": "Cypress",
    "playwright": "Playwright",
    "pytest": "Pytest",
    "unit testing": "Unit Testing",
    "api testing": "API Testing",

    # =========================
    # Mobile Development
    # =========================
    "android": "Android",
    "android development": "Android Development",
    "ios": "iOS",
    "ios development": "iOS Development",
    "flutter": "Flutter",
    "react native": "React Native",

    # =========================
    # Big Data
    # =========================
    "hadoop": "Hadoop",
    "spark": "Apache Spark",
    "apache spark": "Apache Spark",
    "kafka": "Apache Kafka",
    "apache kafka": "Apache Kafka",
    "hive": "Apache Hive",
    "big data": "Big Data",

    # =========================
    # Business / Management
    # =========================
    "business analysis": "Business Analysis",
    "business analyst": "Business Analysis",
    "requirements analysis": "Requirements Analysis",
    "requirements gathering": "Requirements Gathering",
    "project management": "Project Management",
    "product management": "Product Management",
    "product management": "Product Management",
    "agile": "Agile",
    "scrum": "Scrum",
    "jira": "Jira",
    "confluence": "Confluence",
    "stakeholder management": "Stakeholder Management",

    # =========================
    # Finance / Accounting
    # =========================
    "financial analysis": "Financial Analysis",
    "financial modeling": "Financial Modeling",
    "accounting": "Accounting",
    "financial reporting": "Financial Reporting",
    "quickbooks": "QuickBooks",
    "sap": "SAP",
    "erp": "ERP",

    # =========================
    # Marketing
    # =========================
    "digital marketing": "Digital Marketing",
    "seo": "SEO",
    "search engine optimization": "SEO",
    "sem": "SEM",
    "social media marketing": "Social Media Marketing",
    "content marketing": "Content Marketing",
    "google analytics": "Google Analytics",
    "google ads": "Google Ads",

    # =========================
    # Design
    # =========================
    "figma": "Figma",
    "adobe photoshop": "Adobe Photoshop",
    "photoshop": "Adobe Photoshop",
    "adobe illustrator": "Adobe Illustrator",
    "illustrator": "Adobe Illustrator",
    "ui design": "UI Design",
    "ux design": "UX Design",
    "ui/ux": "UI/UX",
    "user experience": "UX Design",
    "user interface": "UI Design",

    # =========================
    # Soft Skills
    # =========================
    "communication": "Communication",
    "leadership": "Leadership",
    "teamwork": "Teamwork",
    "problem solving": "Problem Solving",
    "problem-solving": "Problem Solving",
    "time management": "Time Management",
    "critical thinking": "Critical Thinking",
    "analytical thinking": "Analytical Thinking",
}


def extract_skills(text: str) -> list[str]:
    """
    Extract and normalize skills from resume or job-description text.
    """

    if not text:
        return []

    doc = nlp(text.lower())

    normalized_text = re.sub(r"\s+", " ", doc.text)

    detected_skills = set()

    for alias, skill_name in SKILL_ALIASES.items():
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"

        if re.search(pattern, normalized_text):
            detected_skills.add(skill_name)

    return sorted(detected_skills)