from django.shortcuts import render, redirect, get_object_or_404
from .models import Directory, File
from .forms import DirectoryForm, FileForm
from django.contrib import messages
from django_filters.views import FilterView
from .filters import FileFilter
from django.views.decorators.csrf import csrf_exempt

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from PyPDF2 import PdfReader, PdfWriter
from .forms import PDFPasswordForm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .forms import PDFWatermarkForm

import tempfile
from PIL import Image, ImageEnhance
import fitz  # PyMuPDF
from .forms import PDFTextureForm


def directory_view(request, dir_id=None):
    directory = None
    if dir_id:
        directory = get_object_or_404(Directory, id=dir_id)
        subdirectories = Directory.objects.filter(parent=directory)
        files = File.objects.filter(directory=directory)
        parent_id = directory.pk  # Parent directory ID for new subdirectories
    else:
        subdirectories = Directory.objects.filter(parent=None)
        files = File.objects.filter(directory=None)
        parent_id = None

    context = {
        'current_directory': directory if dir_id else None,
        'subdirectories': subdirectories,
        'files': files,
        'dir_form': DirectoryForm(),
        'file_form': FileForm(),
        'parent_id': parent_id,
        'current_directory_id': directory.pk if directory else None,
    }
    return render(request, 'files/file.html', context)

def add_directory(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)

        if form.is_valid():
            directory = form.save(commit=False)
            parent_id = request.POST.get('parent')

            # Debug print statements
            print("Parent ID from form:", parent_id)
            print("Form is valid. Directory name:", directory.name)

            # Determine if this is a root directory creation
            if not parent_id or parent_id in ['0', 'None', '', None]:  # Handle root directory creation
                directory.parent = None
            else:
                # Attempt to retrieve parent directory
                parent_directory = Directory.objects.filter(pk=parent_id).first()
                if parent_directory:
                    directory.parent = parent_directory
                else:
                    print("No valid parent found; creating as root directory.")
                    directory.parent = None  # Default to root if parent not found

            # Debug: Print the parent directory
            print("Resolved Parent Directory:", directory.parent)

            directory.save()

            # Redirect back to the appropriate view
            if directory.parent:
                return redirect('files:directory_view', dir_id=directory.parent.pk)
            return redirect('files:home')
        else:
            # Print form errors to debug why it's not valid
            print("Form is not valid. Errors:", form.errors)

            # Attempt to create a root directory if form is invalid
            # due to parent field issues
            if 'parent' in form.errors:
                print("Creating root directory as fallback.")
                directory = Directory(name=request.POST.get('name'), parent=None)
                directory.save()
                return redirect('files:home')

    else:
        # Debug: Log if the request method is not POST
        print("Request method is not POST.")

    return redirect('files:home')

def add_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            # Ensure either file or URL is provided
            if not (file.file or file.url):
                form.add_error(None, "Either upload a file or provide a URL.")
            else:
                file.save()
                return redirect('files:home')
                
    return redirect('files:home')
    


def delete_directory(request, pk):
    directory = get_object_or_404(Directory, pk=pk)
    directory.delete()
    return redirect('files:home')

def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    file.delete()
    return redirect('files:file_listing')


class FileListView(FilterView):
    model = File
    template_name = 'files/file_list.html'
    context_object_name = 'files'
    filterset_class = FileFilter


def file_listing(request):
    files = File.objects.select_related('directory').all()
    return render(request, 'files/file_listing.html', {'files': files})


    
# Edit file name view
@csrf_exempt
def edit_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        file.name = request.POST.get('name')
        file.owner = request.POST.get('owner')  # Update the owner field
        file.url = request.POST.get('url')
        file.save()
        return redirect('files:file_listing')

    return render(request, 'edit_file.html', {'file': file})

def add_pdf_password_view(request):
    output_pdf_filename = None  # Initialize output_pdf_filename to avoid UnboundLocalError

    if request.method == 'POST':
        form = PDFPasswordForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            password = form.cleaned_data['password']

            # Define paths
            default_path = "D:\\PyWeb\\media\\resources\\pdf"
            input_pdf_path = os.path.join(default_path, pdf_file.name)
            output_pdf_filename = os.path.splitext(pdf_file.name)[0] + "_pwd.pdf"
            output_pdf_path = os.path.join(default_path, output_pdf_filename)

            # Save uploaded PDF to the server
            with open(input_pdf_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Add password to PDF
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)

            # Write password-protected PDF to output file
            with open(output_pdf_path, 'wb') as output_pdf_file:
                writer.write(output_pdf_file)

            # Redirect to the download URL
            return redirect('files:download_pdf', filename=output_pdf_filename)

    else:
        form = PDFPasswordForm()

    return render(request, 'files/add_pdf_password.html', {
        'form': form,
        'output_pdf_filename': output_pdf_filename  # Now safely includes output_pdf_filename in the context
    })
    
    
def download_pdf_view(request, filename):
    file_path = os.path.join("D:\\PyWeb\\media\\resources\\pdf", filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    return HttpResponse("File not found", status=404)

def add_watermark_view(request):
    output_pdf_filename = None  # Initialize to avoid UnboundLocalError

    if request.method == 'POST':
        form = PDFWatermarkForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            watermark_text = form.cleaned_data['watermark_text']

            # Define paths
            default_path = "D:\\PyWeb\\media\\resources\\pdf"
            input_pdf_path = os.path.join(default_path, pdf_file.name)
            output_pdf_filename = os.path.splitext(pdf_file.name)[0] + "_watermarked.pdf"
            output_pdf_path = os.path.join(default_path, output_pdf_filename)

            # Save uploaded PDF to the server
            with open(input_pdf_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Step 1: Create a temporary watermark PDF with diagonal text
            watermark_pdf = os.path.join(default_path, "temp_watermark.pdf")
            c = canvas.Canvas(watermark_pdf, pagesize=letter)
            c.setFont("Helvetica", 40)
            c.setFillGray(0.5, alpha=0.3)

            # Rotate the canvas to place the text diagonally
            c.saveState()
            c.translate(letter[0] / 2, letter[1] / 2)  # Move the origin to the center of the page
            c.rotate(45)  # Rotate the canvas by 45 degrees
            c.drawString(-100, 0, watermark_text)  # Adjust position as needed
            c.restoreState()

            c.save()

            # Step 2: Merge the watermark with each page of the input PDF
            reader = PdfReader(input_pdf_path)
            watermark = PdfReader(watermark_pdf).pages[0]
            writer = PdfWriter()

            for page in reader.pages:
                page.merge_page(watermark)
                writer.add_page(page)

            # Step 3: Save the watermarked PDF
            with open(output_pdf_path, "wb") as f:
                writer.write(f)

            # Clean up temporary watermark file
            os.remove(watermark_pdf)

            # Redirect to download URL
            return redirect('files:download_pdf', filename=output_pdf_filename)

    else:
        form = PDFWatermarkForm()

    return render(request, 'files/add_watermark.html', {
        'form': form,
        'output_pdf_filename': output_pdf_filename  # Pass filename to context if it exists
    })


def add_texture_view(request):
    if request.method == 'POST':
        form = PDFTextureForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            texture_image = form.cleaned_data['texture_image']
            opacity = form.cleaned_data['opacity']

            # Define paths
            default_path = "D:\\PyWeb\\media\\resources\\pdf"
            input_pdf_path = os.path.join(default_path, pdf_file.name)
            output_pdf_filename = os.path.splitext(pdf_file.name)[0] + "_textured.pdf"
            output_pdf_path = os.path.join(default_path, output_pdf_filename)

            # Save the uploaded PDF and texture image to the server
            with open(input_pdf_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            texture_image_path = os.path.join(default_path, texture_image.name)
            with open(texture_image_path, 'wb') as img:
                for chunk in texture_image.chunks():
                    img.write(chunk)

            # Apply texture to the PDF
            apply_texture(input_pdf_path, output_pdf_path, texture_image_path, opacity)

            # Provide download link to the user
            download_url = reverse('files:download_pdf', args=[output_pdf_filename])
            return HttpResponseRedirect(download_url)
    else:
        form = PDFTextureForm()

    return render(request, 'files/add_texture.html', {'form': form})

def apply_texture(input_pdf, output_pdf, texture_image_path, opacity=0.3):
    doc = fitz.open(input_pdf)
    for page_num in range(len(doc)):
        page = doc[page_num]
        rect = page.rect  # Get the page dimensions

        # Load the texture image and make it semi-transparent
        texture_image = Image.open(texture_image_path).convert("RGBA")
        texture_image = texture_image.resize((int(rect.width), int(rect.height)))

        # Adjust opacity
        alpha = texture_image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        texture_image.putalpha(alpha)

        # Save the semi-transparent image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            texture_image.save(tmp_file, "PNG")
            temp_image_path = tmp_file.name

        # Open the image using fitz.Pixmap from the temporary file
        texture_pixmap = fitz.Pixmap(temp_image_path)
        page.insert_image(rect, pixmap=texture_pixmap)

        # Clean up the temporary image file
        os.remove(temp_image_path)

    # Save the modified PDF
    doc.save(output_pdf)
    doc.close()
    