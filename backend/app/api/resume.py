"""Resume API routes."""

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import Optional
from loguru import logger
import os
from pathlib import Path
from app.core.config import settings
from app.services.resume_processor import resume_processor
from app.services.ai_optimizer import ai_optimizer
from app.services.pdf_generator import pdf_generator

router = APIRouter()

# Ensure upload directory exists
os.makedirs(settings.upload_directory, exist_ok=True)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file."""
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_extensions)}"
            )
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > settings.max_upload_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum limit of {settings.max_upload_size / 1024 / 1024}MB"
            )
        
        # Save file
        file_path = os.path.join(settings.upload_directory, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Process resume
        resume_data = resume_processor.extract_resume_data(file_path)
        
        logger.info(f"Resume uploaded and processed: {file.filename}")
        
        return {
            "success": True,
            "filename": file.filename,
            "file_path": file_path,
            "resume_data": resume_data,
            "message": "Resume uploaded and processed successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = None
):
    """Analyze resume and provide ATS score."""
    try:
        # Save temporary file
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        file_content = await file.read()
        if len(file_content) > settings.max_upload_size:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Create temp file
        temp_path = os.path.join(settings.upload_directory, f"temp_{file.filename}")
        with open(temp_path, 'wb') as f:
            f.write(file_content)
        
        # Extract resume data
        resume_data = resume_processor.extract_resume_data(temp_path, job_description)
        
        logger.info(f"Resume analyzed: {file.filename}, ATS Score: {resume_data['ats_score']}")
        
        return {
            "success": True,
            "filename": file.filename,
            "resume_data": resume_data,
            "ats_score": resume_data['ats_score'],
            "skills": resume_data['skills'],
            "experience_years": resume_data['experience_years'],
        }
    
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize")
async def optimize_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = None
):
    """Optimize resume for ATS and provide suggestions."""
    try:
        # Save file
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        file_content = await file.read()
        temp_path = os.path.join(settings.upload_directory, f"temp_{file.filename}")
        with open(temp_path, 'wb') as f:
            f.write(file_content)
        
        # Extract text
        if file_ext == 'pdf':
            text = resume_processor.extract_text_from_pdf(temp_path)
        elif file_ext == 'docx':
            text = resume_processor.extract_text_from_docx(temp_path)
        elif file_ext == 'doc':
            text = resume_processor.extract_text_from_doc(temp_path)
        else:
            with open(temp_path, 'r') as f:
                text = f.read()
        
        # Optimize resume
        optimization_result = await ai_optimizer.optimize_for_ats(text, job_description)
        
        logger.info(f"Resume optimized: {file.filename}")
        
        return {
            "success": True,
            "filename": file.filename,
            "optimization_result": optimization_result,
        }
    
    except Exception as e:
        logger.error(f"Error optimizing resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export-pdf")
async def export_resume_pdf(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
):
    """Export resume as professional PDF."""
    try:
        # Save file
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        file_content = await file.read()
        temp_path = os.path.join(settings.upload_directory, f"temp_{file.filename}")
        with open(temp_path, 'wb') as f:
            f.write(file_content)
        
        # Extract text
        if file_ext == 'pdf':
            text = resume_processor.extract_text_from_pdf(temp_path)
        elif file_ext == 'docx':
            text = resume_processor.extract_text_from_docx(temp_path)
        elif file_ext == 'doc':
            text = resume_processor.extract_text_from_doc(temp_path)
        else:
            with open(temp_path, 'r') as f:
                text = f.read()
        
        # Generate PDF
        output_path = os.path.join(settings.upload_directory, f"optimized_{Path(file.filename).stem}.pdf")
        success = pdf_generator.generate_styled_pdf(text, output_path, name, email, phone)
        
        if not success:
            raise HTTPException(status_code=500, detail="Error generating PDF")
        
        logger.info(f"PDF exported: {output_path}")
        
        return {
            "success": True,
            "message": "PDF generated successfully",
            "output_path": output_path,
        }
    
    except Exception as e:
        logger.error(f"Error exporting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def resume_health():
    """Health check for resume service."""
    return {
        "status": "healthy",
        "service": "resume-optimizer",
        "upload_dir": settings.upload_directory,
    }
