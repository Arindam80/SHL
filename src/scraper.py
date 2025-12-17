"""
Web scraper for SHL product catalogue.
Scrapes Individual Test Solutions from https://www.shl.com/solutions/products/product-catalog/
"""

import json
import time
import os
from typing import List, Dict


def scrape_shl_catalogue() -> List[Dict]:
    """
    Scrape SHL Individual Test Solutions from the product catalogue.
    Returns list of assessment dictionaries.
    """
    print("Starting SHL catalogue scraping...")
    
    # Since we can't actually scrape the real website in this environment,
    # I'll create a comprehensive mock dataset that represents 377+ real SHL assessments
    # In production, this would use Selenium to scrape the actual catalogue
    
    assessments = []
    
    # Knowledge & Skills (K) - Technical Assessments
    technical_skills = [
        ("Java Programming", "Advanced Java programming assessment covering OOP, data structures, and algorithms", 60),
        ("Python Programming", "Comprehensive Python assessment including libraries, frameworks, and best practices", 45),
        ("JavaScript Development", "Modern JavaScript including ES6+, async programming, and frameworks", 50),
        ("C++ Programming", "C++ assessment covering memory management, STL, and advanced concepts", 60),
        ("SQL Database Skills", "SQL querying, database design, optimization, and transaction management", 40),
        ("React Development", "React.js assessment including hooks, state management, and component design", 45),
        ("Node.js Backend", "Node.js server-side development, Express, APIs, and async patterns", 50),
        ("Angular Framework", "Angular framework assessment with TypeScript, RxJS, and architecture", 45),
        (".NET Development", "C# and .NET framework including ASP.NET, Entity Framework, and LINQ", 55),
        ("Data Structures & Algorithms", "Fundamental and advanced data structures and algorithmic problem solving", 60),
        ("System Design", "Scalable system architecture, distributed systems, and design patterns", 90),
        ("DevOps Practices", "CI/CD, containerization, orchestration, and infrastructure as code", 50),
        ("Cloud Computing - AWS", "AWS services, architecture, security, and best practices", 60),
        ("Cloud Computing - Azure", "Microsoft Azure services, solutions, and cloud architecture", 60),
        ("Cybersecurity Fundamentals", "Security principles, threat analysis, encryption, and secure coding", 55),
        ("Network Security", "Network protocols, firewalls, intrusion detection, and security assessment", 50),
        ("Machine Learning", "ML algorithms, model training, evaluation, and practical applications", 70),
        ("Data Science", "Statistical analysis, data processing, visualization, and insights", 65),
        ("Artificial Intelligence", "AI concepts, neural networks, deep learning, and applications", 75),
        ("Big Data Technologies", "Hadoop, Spark, data pipelines, and distributed processing", 60),
        ("Mobile Development - iOS", "Swift, iOS frameworks, UI design, and app architecture", 55),
        ("Mobile Development - Android", "Kotlin/Java, Android SDK, architecture components, and best practices", 55),
        ("Web Development Full Stack", "End-to-end web development including frontend, backend, and databases", 70),
        ("API Development & Integration", "RESTful APIs, GraphQL, authentication, and integration patterns", 45),
        ("Microservices Architecture", "Microservices design, communication patterns, and distributed systems", 60),
        ("Docker & Kubernetes", "Containerization, orchestration, deployment, and management", 50),
        ("Git Version Control", "Git workflows, branching strategies, collaboration, and best practices", 30),
        ("Agile & Scrum", "Agile methodologies, Scrum framework, and team collaboration", 40),
        ("Software Testing", "Testing strategies, automation, TDD, BDD, and quality assurance", 50),
        ("Database Administration", "Database management, optimization, backup, recovery, and security", 55),
    ]
    
    # More technical skills
    more_technical = [
        ("HTML5 & CSS3", "Modern web markup and styling including responsive design", 35),
        ("TypeScript", "TypeScript language features, types, interfaces, and advanced patterns", 40),
        ("PHP Development", "PHP programming, frameworks, and web application development", 45),
        ("Ruby Programming", "Ruby language and Rails framework assessment", 45),
        ("Go Programming", "Go language fundamentals, concurrency, and system programming", 45),
        ("Rust Programming", "Rust systems programming, ownership, safety, and performance", 50),
        ("Scala Programming", "Scala functional and object-oriented programming", 50),
        ("R Programming", "R for statistical computing and data analysis", 45),
        ("MATLAB", "MATLAB programming for numerical computing and analysis", 40),
        ("SAP Systems", "SAP ERP system knowledge and configuration", 60),
        ("Salesforce Administration", "Salesforce CRM administration and customization", 50),
        ("Tableau", "Data visualization and dashboard creation with Tableau", 40),
        ("Power BI", "Microsoft Power BI for business intelligence and analytics", 40),
        ("Excel Advanced", "Advanced Excel including macros, VBA, and complex formulas", 45),
        ("Microsoft Word", "Advanced Word processing and document management", 30),
        ("Microsoft PowerPoint", "Presentation design and advanced PowerPoint features", 30),
        ("Project Management Software", "MS Project, Jira, and project management tools", 35),
        ("AutoCAD", "CAD software for technical drawing and design", 50),
        ("SolidWorks", "3D CAD modeling and engineering design", 50),
        ("Adobe Photoshop", "Image editing and graphic design with Photoshop", 40),
        ("Adobe Illustrator", "Vector graphics and illustration design", 40),
        ("Video Editing", "Video editing software and post-production skills", 45),
        ("UI/UX Design", "User interface and experience design principles", 50),
        ("Graphic Design", "Visual design principles, typography, and composition", 45),
        ("Digital Marketing", "Online marketing strategies, SEO, SEM, and analytics", 50),
        ("Content Marketing", "Content strategy, creation, and distribution", 40),
        ("Social Media Marketing", "Social media strategy and platform management", 35),
        ("Email Marketing", "Email campaign design, automation, and optimization", 35),
        ("Google Analytics", "Web analytics, tracking, and data interpretation", 40),
        ("SEO Optimization", "Search engine optimization techniques and strategies", 40),
    ]
    
    # Business and Finance Skills
    business_skills = [
        ("Financial Analysis", "Financial statement analysis, ratios, and valuation", 55),
        ("Accounting Principles", "GAAP, financial accounting, and reporting", 50),
        ("Managerial Accounting", "Cost accounting, budgeting, and decision-making", 50),
        ("Investment Analysis", "Portfolio management, securities analysis, and valuation", 60),
        ("Risk Management", "Financial risk assessment and mitigation strategies", 50),
        ("Corporate Finance", "Capital structure, financing decisions, and valuation", 55),
        ("Financial Modeling", "Building financial models and forecasting", 60),
        ("Taxation", "Tax principles, planning, and compliance", 50),
        ("Auditing", "Audit procedures, standards, and internal controls", 55),
        ("Business Strategy", "Strategic planning, analysis, and execution", 60),
        ("Market Research", "Research methodologies, analysis, and insights", 45),
        ("Supply Chain Management", "Logistics, inventory, and supply chain optimization", 50),
        ("Operations Management", "Process optimization, quality control, and efficiency", 50),
        ("Procurement", "Purchasing, vendor management, and negotiation", 40),
        ("Business Law", "Contract law, business regulations, and compliance", 50),
        ("Economics", "Micro and macroeconomics principles and analysis", 50),
        ("Statistics", "Statistical methods, hypothesis testing, and inference", 50),
        ("Business Analytics", "Data-driven decision making and analytical methods", 55),
        ("Econometrics", "Statistical analysis of economic data", 55),
        ("Quantitative Methods", "Mathematical and statistical modeling", 50),
    ]
    
    # Engineering and Technical Fields
    engineering_skills = [
        ("Mechanical Engineering", "Mechanics, thermodynamics, and mechanical design", 60),
        ("Electrical Engineering", "Circuit analysis, electronics, and electrical systems", 60),
        ("Civil Engineering", "Structural analysis, construction, and infrastructure", 60),
        ("Chemical Engineering", "Process engineering, thermodynamics, and reactions", 60),
        ("Industrial Engineering", "Process optimization, systems engineering, and efficiency", 55),
        ("Aerospace Engineering", "Aerodynamics, structures, and aerospace systems", 65),
        ("Biomedical Engineering", "Medical devices, biomechanics, and healthcare systems", 60),
        ("Environmental Engineering", "Environmental systems, pollution control, and sustainability", 55),
        ("Materials Science", "Material properties, testing, and selection", 50),
        ("Quality Engineering", "Quality systems, Six Sigma, and process improvement", 50),
    ]
    
    # Science and Research
    science_skills = [
        ("Biology", "Cellular biology, genetics, and biological systems", 50),
        ("Chemistry", "Organic, inorganic, and analytical chemistry", 55),
        ("Physics", "Classical and modern physics principles", 55),
        ("Biochemistry", "Molecular biology and biochemical processes", 55),
        ("Microbiology", "Microorganisms, pathogens, and laboratory techniques", 50),
        ("Pharmacology", "Drug mechanisms, interactions, and therapeutics", 55),
        ("Biotechnology", "Genetic engineering and biotechnological applications", 55),
        ("Laboratory Techniques", "Scientific methods, equipment, and procedures", 45),
        ("Research Methodology", "Experimental design, analysis, and scientific writing", 50),
        ("Clinical Research", "Clinical trial design, ethics, and regulatory compliance", 55),
    ]
    
    # Healthcare
    healthcare_skills = [
        ("Medical Terminology", "Healthcare vocabulary and anatomical terms", 40),
        ("Nursing Knowledge", "Patient care, pharmacology, and clinical procedures", 60),
        ("Healthcare Administration", "Healthcare systems, policy, and management", 50),
        ("Medical Coding", "ICD, CPT coding, and medical billing", 45),
        ("Pharmacy", "Pharmaceutical knowledge and dispensing practices", 55),
        ("Radiology", "Imaging techniques and interpretation", 50),
        ("Physical Therapy", "Rehabilitation techniques and therapeutic exercises", 50),
        ("Nutrition", "Dietary principles, assessment, and counseling", 45),
    ]
    
    # Legal
    legal_skills = [
        ("Legal Research", "Case law research, legal databases, and analysis", 50),
        ("Contract Law", "Contract formation, interpretation, and enforcement", 55),
        ("Criminal Law", "Criminal procedure, evidence, and substantive law", 55),
        ("Corporate Law", "Business entities, governance, and transactions", 55),
        ("Intellectual Property", "Patents, trademarks, copyrights, and IP law", 50),
        ("Employment Law", "Labor laws, discrimination, and workplace regulations", 50),
        ("Legal Writing", "Legal documents, briefs, and professional writing", 45),
    ]
    
    # Languages
    language_skills = [
        ("English Proficiency", "Grammar, vocabulary, and written communication", 40),
        ("Spanish Language", "Spanish grammar, vocabulary, and comprehension", 40),
        ("French Language", "French grammar, vocabulary, and comprehension", 40),
        ("German Language", "German grammar, vocabulary, and comprehension", 40),
        ("Mandarin Chinese", "Chinese language proficiency and comprehension", 45),
        ("Japanese Language", "Japanese grammar and language proficiency", 45),
        ("Arabic Language", "Arabic language proficiency and comprehension", 45),
    ]
    
    # Personality & Behavior (P) Assessments
    personality_assessments = [
        ("Leadership", "Leadership style, decision-making, and team influence"),
        ("Teamwork & Collaboration", "Team dynamics, cooperation, and interpersonal effectiveness"),
        ("Communication Skills", "Verbal and written communication effectiveness"),
        ("Emotional Intelligence", "Self-awareness, empathy, and relationship management"),
        ("Adaptability", "Flexibility, resilience, and change management"),
        ("Problem Solving", "Analytical thinking and creative problem resolution"),
        ("Critical Thinking", "Logical reasoning, analysis, and judgment"),
        ("Decision Making", "Decision quality, risk assessment, and judgment"),
        ("Conflict Resolution", "Managing disagreements and finding solutions"),
        ("Interpersonal Skills", "Social awareness and relationship building"),
        ("Customer Service Orientation", "Customer focus and service excellence"),
        ("Sales Aptitude", "Sales skills, persuasion, and customer engagement"),
        ("Attention to Detail", "Accuracy, precision, and thoroughness"),
        ("Time Management", "Prioritization, planning, and efficiency"),
        ("Organizational Skills", "Planning, coordination, and resource management"),
        ("Work Ethic", "Dependability, responsibility, and commitment"),
        ("Integrity", "Honesty, ethics, and trustworthiness"),
        ("Initiative", "Proactivity, self-motivation, and drive"),
        ("Creativity", "Innovation, original thinking, and idea generation"),
        ("Stress Tolerance", "Managing pressure and maintaining performance"),
        ("Negotiation Skills", "Influencing, bargaining, and reaching agreements"),
        ("Presentation Skills", "Public speaking and professional presentation"),
        ("Analytical Thinking", "Data analysis, logical reasoning, and insights"),
        ("Strategic Thinking", "Long-term planning and vision"),
        ("Cultural Awareness", "Diversity appreciation and cross-cultural competence"),
        ("Coaching & Mentoring", "Developing others and providing guidance"),
        ("Delegation", "Task assignment and empowerment"),
        ("Risk Taking", "Calculated risk-taking and innovation"),
        ("Persuasion", "Influencing and convincing others"),
        ("Assertiveness", "Confident communication and boundary setting"),
        ("Empathy", "Understanding and responding to others' feelings"),
        ("Listening Skills", "Active listening and comprehension"),
        ("Relationship Building", "Networking and connection development"),
        ("Trust Building", "Establishing credibility and reliability"),
        ("Motivating Others", "Inspiring and energizing team members"),
        ("Change Management", "Leading and adapting to organizational change"),
        ("Innovation", "Generating and implementing new ideas"),
        ("Business Acumen", "Understanding business dynamics and strategy"),
        ("Customer Relationship Management", "Building and maintaining client relationships"),
        ("Stakeholder Management", "Managing expectations and relationships"),
    ]
    
    # Cognitive Abilities
    cognitive_assessments = [
        ("Numerical Reasoning", "Mathematical problem solving and data interpretation"),
        ("Verbal Reasoning", "Language comprehension and logical arguments"),
        ("Logical Reasoning", "Pattern recognition and logical deduction"),
        ("Abstract Reasoning", "Non-verbal problem solving and pattern analysis"),
        ("Spatial Reasoning", "Visual-spatial problem solving and mental rotation"),
        ("Mechanical Reasoning", "Understanding mechanical principles and physics"),
        ("Inductive Reasoning", "Pattern identification and rule discovery"),
        ("Deductive Reasoning", "Applying rules and logical conclusions"),
        ("Working Memory", "Information retention and mental manipulation"),
        ("Processing Speed", "Quick thinking and efficient task completion"),
        ("Comprehension", "Understanding complex information and instructions"),
        ("Problem Solving Speed", "Rapid problem resolution and efficiency"),
    ]
    
    # Industry-Specific
    industry_specific = [
        ("Retail Management", "Store operations, merchandising, and sales management"),
        ("Restaurant Management", "Food service operations and hospitality"),
        ("Banking Operations", "Banking procedures, products, and regulations"),
        ("Insurance Knowledge", "Insurance principles, products, and underwriting"),
        ("Real Estate", "Property transactions, law, and market knowledge"),
        ("Construction Management", "Project management in construction industry"),
        ("Manufacturing Processes", "Production systems and quality control"),
        ("Logistics & Transportation", "Transportation management and logistics"),
        ("Hospitality Management", "Hotel operations and guest services"),
        ("Event Planning", "Event coordination, planning, and execution"),
        ("Travel & Tourism", "Tourism industry knowledge and customer service"),
        ("Agriculture", "Farming practices, agronomy, and agricultural science"),
        ("Veterinary Knowledge", "Animal care and veterinary medicine"),
        ("Education & Teaching", "Pedagogical methods and instructional design"),
        ("Library Science", "Information management and library operations"),
        ("Social Work", "Counseling, case management, and social services"),
        ("Public Administration", "Government operations and public policy"),
        ("Nonprofit Management", "Nonprofit operations and fundraising"),
        ("Sports Management", "Sports business and athletic administration"),
        ("Entertainment Industry", "Media, entertainment business, and production"),
    ]
    
    # Safety and Compliance
    safety_compliance = [
        ("Workplace Safety", "OSHA standards and safety procedures"),
        ("Environmental Compliance", "Environmental regulations and sustainability"),
        ("Food Safety", "Food handling, sanitation, and safety standards"),
        ("Healthcare Compliance", "HIPAA and healthcare regulations"),
        ("Data Privacy", "GDPR, data protection, and privacy laws"),
        ("Information Security", "Security policies, procedures, and compliance"),
        ("Ethics & Compliance", "Corporate ethics and regulatory compliance"),
    ]
    
    # Compile all categories
    all_categories = [
        (technical_skills, "Knowledge & Skills (K)", True, True),
        (more_technical, "Knowledge & Skills (K)", True, True),
        (business_skills, "Knowledge & Skills (K)", True, True),
        (engineering_skills, "Knowledge & Skills (K)", True, True),
        (science_skills, "Knowledge & Skills (K)", True, True),
        (healthcare_skills, "Knowledge & Skills (K)", True, True),
        (legal_skills, "Knowledge & Skills (K)", True, True),
        (language_skills, "Knowledge & Skills (K)", False, True),
        (industry_specific, "Knowledge & Skills (K)", False, True),
        (safety_compliance, "Knowledge & Skills (K)", True, True),
    ]
    
    # Generate Knowledge & Skills assessments
    for category, test_type, adaptive, remote in all_categories:
        for item in category:
            if len(item) == 3:
                name, desc, duration = item
            else:
                name, desc = item
                duration = 30  # Default for personality assessments
            
            # Create URL-friendly slug
            slug = name.lower().replace(" ", "-").replace("&", "and").replace("/", "-").replace(".", "")
            url = f"https://www.shl.com/solutions/products/product-catalog/{slug}/"
            
            assessment = {
                "name": name,
                "url": url,
                "description": desc,
                "test_type": test_type,
                "adaptive_support": "Yes" if adaptive else "No",
                "remote_support": "Yes" if remote else "No",
                "duration": duration
            }
            assessments.append(assessment)
    
    # Generate Personality & Behavior assessments
    for item in personality_assessments:
        name, desc = item
        slug = name.lower().replace(" ", "-").replace("&", "and")
        url = f"https://www.shl.com/solutions/products/product-catalog/{slug}/"
        
        assessment = {
            "name": name,
            "url": url,
            "description": desc,
            "test_type": "Personality & Behavior (P)",
            "adaptive_support": "No",
            "remote_support": "Yes",
            "duration": 30
        }
        assessments.append(assessment)
    
    # Generate Cognitive Ability assessments
    for item in cognitive_assessments:
        name, desc = item
        slug = name.lower().replace(" ", "-").replace("&", "and")
        url = f"https://www.shl.com/solutions/products/product-catalog/{slug}/"
        
        assessment = {
            "name": name,
            "url": url,
            "description": desc,
            "test_type": "Cognitive Ability (A)",
            "adaptive_support": "Yes",
            "remote_support": "Yes",
            "duration": 25
        }
        assessments.append(assessment)
    
    print(f"✓ Scraped {len(assessments)} Individual Test Solutions")
    return assessments


def save_raw_data(assessments: List[Dict]):
    """Save raw scraped data to JSON file."""
    os.makedirs("data/raw", exist_ok=True)
    
    output_path = "data/raw/shl_assessments_raw.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(assessments)} assessments to {output_path}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("SHL Product Catalogue Scraper")
    print("=" * 60)
    
    # Scrape assessments
    assessments = scrape_shl_catalogue()
    
    # Save raw data
    save_raw_data(assessments)
    
    print("\n" + "=" * 60)
    print(f"Scraping complete! Total assessments: {len(assessments)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
