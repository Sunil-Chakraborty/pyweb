#python manage.py extract_links D:\PyWeb\NAAC-12-15.pdf D:\PyWeb\Extracted


import os
import fitz  # PyMuPDF for extracting links from PDF
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings

def extract_links_from_pdf(pdf_path):
    """Extracts all links from a PDF file."""
    doc = fitz.open(pdf_path)
    all_links = []
    
    for page in doc:
        for link in page.get_links():
            uri = link.get("uri", "")
            if uri:
                all_links.append(uri)
    
    return all_links

def upload_pdf_extract_links(request):
    """Handles PDF file upload, extracts links, and saves the results dynamically."""
    if request.method == "POST" and request.FILES.get("pdf_file"):
        pdf_file = request.FILES["pdf_file"]
        save_dir = os.path.join(settings.MEDIA_ROOT, "extracted_links")
        os.makedirs(save_dir, exist_ok=True)
        
        # Save uploaded file temporarily
        file_path = os.path.join(save_dir, pdf_file.name)
        file_name = default_storage.save(file_path, ContentFile(pdf_file.read()))
        
        # Extract links
        extracted_links = extract_links_from_pdf(default_storage.path(file_name))
        
        # Save extracted links to a text file
        links_file_path = os.path.join(save_dir, f"{pdf_file.name}_links.txt")
        with open(links_file_path, "w") as f:
            for link in extracted_links:
                f.write(link + "\n")
        
        return JsonResponse({
            "message": "Links extracted successfully",
            "links": extracted_links,
            "saved_file": links_file_path,
        })
    
    return render(request, "upload_pdf.html")
