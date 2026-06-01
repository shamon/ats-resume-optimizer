"""Enhanced AI Resume optimization service."""

from typing import Dict, List
from loguru import logger
import os

class AIOptimizer:
    """AI-powered resume optimization without external dependencies."""
    
    def __init__(self):
        """Initialize AI Optimizer with optional API keys."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    
    async def optimize_for_ats(self, resume_text: str, job_description: str = None) -> Dict:
        """Optimize resume for ATS compatibility."""
        try:
            # Analyze current resume
            issues = self._analyze_resume(resume_text)
            suggestions = self._generate_suggestions(resume_text, job_description)
            
            # Generate optimized content
            optimized_content = self._apply_optimizations(resume_text, suggestions)
            
            return {
                'success': True,
                'optimized_content': optimized_content,
                'suggestions': suggestions,
                'issues_found': issues,
                'optimization_report': self._generate_report(issues, suggestions),
            }
        except Exception as e:
            logger.error(f"Error optimizing resume: {e}")
            return {
                'success': False,
                'error': str(e),
                'optimized_content': resume_text,
                'suggestions': [],
            }
    
    @staticmethod
    def _analyze_resume(text: str) -> List[Dict]:
        """Analyze resume for ATS compatibility issues."""
        issues = []
        
        # Check for formatting issues
        if '\t' in text:
            issues.append({
                'type': 'formatting',
                'severity': 'high',
                'message': 'Avoid using tabs in resume. Use spaces instead.',
                'suggestion': 'Replace all tabs with appropriate spacing'
            })
        
        if '|' in text or '•' in text or '◦' in text:
            issues.append({
                'type': 'formatting',
                'severity': 'medium',
                'message': 'Special characters may not be ATS-compatible.',
                'suggestion': 'Use standard bullet points (-) instead'
            })
        
        # Check for text after page break
        pages = text.split('\f')
        if len(pages) > 1:
            issues.append({
                'type': 'formatting',
                'severity': 'medium',
                'message': 'Resume contains multiple pages.',
                'suggestion': 'Keep resume to single page if possible'
            })
        
        # Check for graphics/images (indicated by certain markers)
        if any(marker in text for marker in ['[image]', '[graphic]', '[chart]']):
            issues.append({
                'type': 'content',
                'severity': 'high',
                'message': 'Resume contains images or graphics.',
                'suggestion': 'Remove all images as ATS systems cannot parse them'
            })
        
        # Check for inconsistent formatting
        lines = text.split('\n')
        has_multiple_fonts = len(set(len(line.lstrip()) - len(line.lstrip().lstrip()) for line in lines)) > 2
        if has_multiple_fonts:
            issues.append({
                'type': 'formatting',
                'severity': 'medium',
                'message': 'Inconsistent indentation detected.',
                'suggestion': 'Use consistent indentation throughout'
            })
        
        # Check for dates format
        import re
        date_patterns = [r'\d{1,2}/\d{1,2}/\d{4}', r'\d{4}-\d{1,2}-\d{1,2}']
        has_dates = any(re.search(pattern, text) for pattern in date_patterns)
        if not has_dates:
            issues.append({
                'type': 'content',
                'severity': 'low',
                'message': 'No clear date format found.',
                'suggestion': 'Use consistent date format (MM/DD/YYYY or YYYY-MM-DD)'
            })
        
        return issues
    
    @staticmethod
    def _generate_suggestions(resume_text: str, job_description: str = None) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = [
            "✓ Use action verbs at the start of bullet points (managed, developed, improved, etc.)",
            "✓ Include quantifiable achievements with numbers and percentages",
            "✓ Tailor resume to job description keywords",
            "✓ Keep formatting simple: use standard fonts, single column layout",
            "✓ Use standard bullet points (-) instead of special characters",
            "✓ Include specific technical skills relevant to the role",
            "✓ Use clear section headers: Experience, Education, Skills, etc.",
            "✓ Remove dates in uncommon formats",
            "✓ Avoid tables, graphics, and special formatting",
            "✓ Use common industry terms and abbreviations",
        ]
        
        # Add job-specific suggestions if job description provided
        if job_description:
            suggestions.insert(0, "✓ Match resume keywords to job description requirements")
            
            # Check for specific technology matches
            tech_keywords = ['python', 'java', 'react', 'aws', 'sql', 'docker']
            job_desc_lower = job_description.lower()
            resume_lower = resume_text.lower()
            
            for tech in tech_keywords:
                if tech in job_desc_lower and tech not in resume_lower:
                    suggestions.append(f"✓ Consider highlighting {tech.upper()} experience if you have it")
        
        return suggestions[:10]  # Return top 10 suggestions
    
    @staticmethod
    def _apply_optimizations(text: str, suggestions: List[str]) -> str:
        """Apply optimizations to resume text."""
        optimized = text
        
        # Replace special bullet points with standard hyphens
        special_bullets = ['•', '◦', '◆', '○', '■', '▪']
        for bullet in special_bullets:
            optimized = optimized.replace(bullet, '-')
        
        # Replace multiple spaces with single space
        import re
        optimized = re.sub(r' {2,}', ' ', optimized)
        
        # Normalize dates
        optimized = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{2})', r'\1/\2/20\3', optimized)
        
        # Clean up excessive whitespace
        optimized = '\n'.join(line.rstrip() for line in optimized.split('\n'))
        
        return optimized
    
    @staticmethod
    def _generate_report(issues: List[Dict], suggestions: List[str]) -> Dict:
        """Generate optimization report."""
        high_severity = sum(1 for issue in issues if issue.get('severity') == 'high')
        medium_severity = sum(1 for issue in issues if issue.get('severity') == 'medium')
        low_severity = sum(1 for issue in issues if issue.get('severity') == 'low')
        
        report = {
            'total_issues': len(issues),
            'high_severity_issues': high_severity,
            'medium_severity_issues': medium_severity,
            'low_severity_issues': low_severity,
            'total_suggestions': len(suggestions),
            'priority_level': 'critical' if high_severity > 0 else 'high' if medium_severity > 0 else 'low',
        }
        
        return report

ai_optimizer = AIOptimizer()
