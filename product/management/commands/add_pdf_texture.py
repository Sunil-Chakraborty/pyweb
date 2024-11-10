import os
from PIL import Image, ImageEnhance
import tempfile
from django.conf import settings
from django.core.management.base import BaseCommand
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

#convert normal pdf to pdf with texture.
#python manage.py add_pdf_texture cas.pdf


class Command(BaseCommand):
    help = 'Add a texture or watermark to a PDF file'

    def add_arguments(self, parser):
        # Argument to specify the PDF file name (without full path)
        parser.add_argument('pdf_name', type=str, help='Name of the PDF file in media/resources/pdf directory')
        
        # Set default path for texture image
        default_texture_path = os.path.join("D:\\PyWeb\\media\\resources\\pdf\\texture_image.jpg")
        parser.add_argument('--texture', type=str, help='Path to texture image (optional)', default=default_texture_path)
        parser.add_argument('--watermark', type=str, help='Text for watermark (optional)', default=None)

    def handle(self, *args, **options):
        pdf_name = options['pdf_name']
        
        # Construct the input and output paths using MEDIA_ROOT
        input_pdf = os.path.join(settings.MEDIA_ROOT, 'resources', 'pdf', pdf_name)
        output_pdf = input_pdf  # Save the modified PDF back to the same location
        
        texture_image = options['texture']
        watermark_text = options['watermark']

        # Check if the input file exists
        if not os.path.isfile(input_pdf):
            self.stdout.write(self.style.ERROR(f"The file {input_pdf} does not exist."))
            return
        
        # Display texture and watermark details for debugging
        self.stdout.write(f"Texture path: {texture_image}")
        self.stdout.write(f"Watermark text: {watermark_text}")

        # Apply texture or watermark based on provided options
        if texture_image and os.path.isfile(texture_image):
            self.stdout.write(f"Applying texture from {texture_image}")
            self.apply_texture(input_pdf, output_pdf, texture_image)
        elif watermark_text:
            self.apply_watermark(input_pdf, output_pdf, watermark_text)
        else:
            self.stdout.write(self.style.ERROR("Please provide either a valid texture image or watermark text"))
    
    def apply_texture(self, input_pdf, output_pdf, texture_image_path, opacity=0.3):
        # Open the PDF
        doc = fitz.open(input_pdf)
        print(f"Opened PDF: {input_pdf}")

        for page_num in range(len(doc)):
            page = doc[page_num]
            rect = page.rect  # Get the page dimensions

            # Load the texture image and make it semi-transparent
            texture_image = Image.open(texture_image_path).convert("RGBA")
            texture_image = texture_image.resize((int(rect.width), int(rect.height)))

            # Adjust opacity by applying the opacity factor to the image
            alpha = texture_image.split()[3]  # Get the alpha channel
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)  # Adjust opacity
            texture_image.putalpha(alpha)
            print(f"Applied opacity to texture image for page {page_num}")

            # Save the semi-transparent image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                texture_image.save(tmp_file, "PNG")
                temp_image_path = tmp_file.name
                print(f"Saved semi-transparent texture image to temporary file: {temp_image_path}")

            # Open the image using fitz.Pixmap from the temporary file
            texture_pixmap = fitz.Pixmap(temp_image_path)
            print(f"Created pixmap for page {page_num}")

            # Insert the pixmap as an image onto the page
            page.insert_image(rect, pixmap=texture_pixmap)
            print(f"Inserted texture on page {page_num}")

            # Clean up the temporary image file
            os.remove(temp_image_path)
            print(f"Deleted temporary image file: {temp_image_path}")

        # Ensure output_pdf is not the same as input_pdf
        if input_pdf == output_pdf:
            output_pdf = f"{os.path.splitext(input_pdf)[0]}_modified.pdf"
            print(f"Output PDF path changed to: {output_pdf}")

        # Save the modified PDF to a new file (not the original one)
        doc.save(output_pdf)
        doc.close()
        print(f"Texture applied and saved to {output_pdf}") 
