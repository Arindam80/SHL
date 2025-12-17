"""
Map mock assessment names to real SHL product catalog URLs.
This ensures our recommendations match the actual training data.
"""

ASSESSMENT_URL_MAP = {
    # Programming & Development
    "Java Programming": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
    "Python Programming": "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
    "JavaScript Development": "https://www.shl.com/solutions/products/product-catalog/view/javascript-new/",
    "SQL Database Skills": "https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/",
    "Data Science": "https://www.shl.com/solutions/products/product-catalog/view/data-warehousing-concepts/",
    "Web Development": "https://www.shl.com/solutions/products/product-catalog/view/css3-new/",
    "Test Automation": "https://www.shl.com/solutions/products/product-catalog/view/automata-selenium/",
    "Advanced Programming": "https://www.shl.com/solutions/products/product-catalog/view/advanced-level-new/",
    
    # Sales & Marketing
    "Sales Aptitude": "https://www.shl.com/solutions/products/product-catalog/view/universal-sales-7-1/",
    "Digital Marketing": "https://www.shl.com/solutions/products/product-catalog/view/marketing-new/",
    "SEO Optimization": "https://www.shl.com/solutions/products/product-catalog/view/search-engine-optimization-new/",
    "Content Marketing": "https://www.shl.com/solutions/products/product-catalog/view/digital-advertising-new/",
    "Sales Representative": "https://www.shl.com/solutions/products/product-catalog/view/sales-representative-solution/",
    "Entry Level Sales": "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-solution/",
    "Technical Sales Associate": "https://www.shl.com/solutions/products/product-catalog/view/technical-sales-associate-solution/",
    
    # Banking & Finance
    "Banking Operations": "https://www.shl.com/solutions/products/product-catalog/view/bank-administrative-assistant-short-form/",
    "Financial Analysis": "https://www.shl.com/solutions/products/product-catalog/view/financial-professional-short-form/",
    
    # Administrative
    "Data Entry Skills": "https://www.shl.com/solutions/products/product-catalog/view/general-entry-level-data-entry-7-0-solution/",
    "Administrative Skills": "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/",
    "Microsoft Excel": "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-new/",
    
    # Cognitive Abilities
    "Numerical Reasoning": "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
    "Verbal Reasoning": "https://www.shl.com/solutions/products/product-catalog/view/verbal-and-numerical-critical-reasoning-intermediate-general/",
    "Inductive Reasoning": "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-inductive-reasoning/",
    "Problem Solving": "https://www.shl.com/solutions/products/product-catalog/view/verify-ability-next-generation/",
    
    # Personality & Behavior
    "Work Styles": "https://www.shl.com/solutions/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
    "Leadership Assessment": "https://www.shl.com/solutions/products/product-catalog/view/verify-leadership-report/",
    "Team Dynamics": "https://www.shl.com/solutions/products/product-catalog/view/opq-team-types-and-leadership-styles-report-opq32/",
    "Interpersonal Skills": "https://www.shl.com/solutions/products/product-catalog/view/interpersonal-communications/",
    
    # Language & Communication
    "English Comprehension": "https://www.shl.com/solutions/products/product-catalog/view/english-comprehension-new/",
    "Written Communication": "https://www.shl.com/solutions/products/product-catalog/view/written-english-v1/",
    
    # Professional Solutions
    "Professional Assessment": "https://www.shl.com/solutions/products/product-catalog/view/professional-7-1-solution/",
    "Global Skills": "https://www.shl.com/solutions/products/product-catalog/view/global-skills-assessment/",
    "Enterprise Assessment": "https://www.shl.com/solutions/products/product-catalog/view/enterprise-report/",
}


def map_assessment_url(name: str, fallback_url: str) -> str:
    """
    Map an assessment name to its real SHL product catalog URL.
    
    Args:
        name: Assessment name
        fallback_url: Original URL to use if no mapping exists
        
    Returns:
        Mapped URL or fallback URL
    """
    return ASSESSMENT_URL_MAP.get(name, fallback_url)


def update_assessment_urls(assessments: list) -> list:
    """
    Update assessment URLs to use real SHL product catalog URLs.
    
    Args:
        assessments: List of assessment dictionaries
        
    Returns:
        Updated assessments with real URLs
    """
    for assessment in assessments:
        name = assessment.get('name', '')
        original_url = assessment.get('url', '')
        assessment['url'] = map_assessment_url(name, original_url)
    
    return assessments
