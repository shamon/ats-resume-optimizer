"""Application constants and enumerations."""

# ATS Keywords for resume optimization
ATS_KEYWORDS = [
    'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
    'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
    'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github',
    'leadership', 'communication', 'problem-solving', 'teamwork',
    'project-management', 'agile', 'scrum', 'jira', 'confluence',
    'html', 'css', 'sass', 'webpack', 'rest', 'graphql', 'api',
    'microservices', 'testing', 'junit', 'pytest', 'ci/cd', 'jenkins',
    'linux', 'unix', 'bash', 'shell', 'devops', 'terraform', 'ansible',
    'machine-learning', 'deep-learning', 'tensorflow', 'pytorch',
    'data-analysis', 'pandas', 'numpy', 'scipy', 'scikit-learn',
    'excel', 'tableau', 'power-bi', 'analytics', 'sql', 'r', 'python',
    'communication', 'time-management', 'attention-to-detail',
    'analytical', 'critical-thinking', 'strategic-planning',
]

# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500

# File Extensions
ALLOWED_RESUME_EXTENSIONS = ['pdf', 'docx', 'doc', 'txt']
RESUME_MAX_SIZE = 10 * 1024 * 1024  # 10MB

# Pricing Tiers
PRICING_TIERS = {
    'free': {'price': 0, 'features': ['basic_analysis', 'ats_score']},
    'basic': {'price': 4.99, 'features': ['basic_analysis', 'ats_score', 'suggestions', 'pdf_export']},
    'premium': {'price': 9.99, 'features': ['basic_analysis', 'ats_score', 'suggestions', 'pdf_export', 'ai_optimization', 'job_matching']},
}

# Resume Status
RESUME_STATUS = {
    'uploaded': 'uploaded',
    'processing': 'processing',
    'completed': 'completed',
    'failed': 'failed',
}

# Payment Status
PAYMENT_STATUS = {
    'pending': 'pending',
    'completed': 'completed',
    'failed': 'failed',
    'refunded': 'refunded',
}

# Error Messages
ERROR_MESSAGES = {
    'file_not_found': 'File not found',
    'invalid_file_type': 'Invalid file type. Allowed types: pdf, docx, doc, txt',
    'file_too_large': 'File size exceeds maximum limit of 10MB',
    'processing_error': 'Error processing resume',
    'database_error': 'Database error occurred',
    'payment_error': 'Payment processing failed',
    'unauthorized': 'Unauthorized access',
    'not_found': 'Resource not found',
}

# Success Messages
SUCCESS_MESSAGES = {
    'resume_uploaded': 'Resume uploaded successfully',
    'resume_processed': 'Resume processed successfully',
    'optimization_completed': 'Resume optimization completed',
    'payment_successful': 'Payment processed successfully',
    'refund_processed': 'Refund processed successfully',
}
