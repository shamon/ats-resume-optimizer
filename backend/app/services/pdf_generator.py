"""Enhanced PDF generation service."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from typing import Optional
from loguru import logger
from pathlib import Path

class PDFGenerator:
    """Generate professional PDF resumes."""
    
    @staticmethod
    def generate_pdf(content: str, output_path: str, style_config: dict = None) -> bool:
        """Generate professional PDF from resume content."""
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.5 * inch,
                leftMargin=0.5 * inch,
                topMargin=0.5 * inch,
                bottomMargin=0.5 * inch,
            )
            
            # Container for PDF elements
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=14,
                textColor=colors.HexColor('#1F4E78'),
                spaceAfter=6,
                fontName='Helvetica-Bold',
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=11,
                textColor=colors.HexColor('#1F4E78'),
                spaceAfter=6,
                spaceBefore=12,
                fontName='Helvetica-Bold',
                borderBottomWidth=1,
                borderBottomColor=colors.HexColor('#1F4E78'),
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=10,
                leading=12,
                spaceAfter=4,
            )
            
            # Parse content and add to story
            lines = content.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 0.1 * inch))
                    continue
                
                # Detect section headers (lines in ALL CAPS)
                if line.isupper() and len(line) > 3:
                    if current_section:
                        story.append(Spacer(1, 0.1 * inch))
                    story.append(Paragraph(line, heading_style))
                    current_section = line
                
                # Add bullet points
                elif line.startswith('-') or line.startswith('•'):
                    bullet_text = line.lstrip('-•').strip()
                    story.append(Paragraph(f"• {bullet_text}", body_style))
                
                # Add regular text
                else:
                    story.append(Paragraph(line, body_style))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF generated successfully: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return False
    
    @staticmethod
    def generate_styled_pdf(
        content: str,
        output_path: str,
        name: str = None,
        email: str = None,
        phone: str = None,
        style: dict = None
    ) -> bool:
        """Generate professionally styled PDF resume with header."""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.5 * inch,
                leftMargin=0.5 * inch,
                topMargin=0.5 * inch,
                bottomMargin=0.5 * inch,
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            # Add header with contact info if provided
            if name or email or phone:
                header_data = []
                header_text = ""
                if name:
                    header_text += f"<b>{name}</b>"
                if email or phone:
                    header_text += " | "
                    if email:
                        header_text += f"{email}"
                    if phone:
                        header_text += f" | {phone}"
                
                header_style = ParagraphStyle(
                    'Header',
                    parent=styles['Normal'],
                    fontSize=12,
                    textColor=colors.HexColor('#1F4E78'),
                    alignment=1,  # Center
                    spaceAfter=12,
                )
                story.append(Paragraph(header_text, header_style))
                story.append(Spacer(1, 0.2 * inch))
            
            # Add main content
            heading_style = ParagraphStyle(
                'SectionHeading',
                parent=styles['Heading2'],
                fontSize=11,
                textColor=colors.HexColor('#1F4E78'),
                spaceAfter=6,
                spaceBefore=10,
                fontName='Helvetica-Bold',
                borderBottomWidth=1,
                borderBottomColor=colors.HexColor('#1F4E78'),
            )
            
            body_style = ParagraphStyle(
                'Body',
                parent=styles['Normal'],
                fontSize=10,
                leading=12,
                spaceAfter=4,
            )
            
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 0.05 * inch))
                    continue
                
                if line.isupper() and len(line) > 3:
                    story.append(Paragraph(line, heading_style))
                elif line.startswith('-') or line.startswith('•'):
                    bullet = line.lstrip('-•').strip()
                    story.append(Paragraph(f"• {bullet}", body_style))
                else:
                    story.append(Paragraph(line, body_style))
            
            # Build document
            doc.build(story)
            logger.info(f"Styled PDF generated: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating styled PDF: {e}")
            return False

pdf_generator = PDFGenerator()
