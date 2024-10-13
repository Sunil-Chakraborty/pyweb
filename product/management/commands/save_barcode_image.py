from django.core.management.base import BaseCommand
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from product.models import RawMat
import os
import re
import barcode
from barcode.writer import ImageWriter
#ZXing Decoder Online (https://zxing.org/w/decode.jspx)

def sanitize_input(input_string):
    # Replace invalid characters like µ (or any others you don't want)
    return re.sub(r'[^a-zA-Z0-9 -]', '', input_string)  # Keeps letters, numbers, spaces, and hyphens




class Command(BaseCommand):
    help = 'Generates barcode images and a PDF with barcodes for printing labels'

    def handle(self, *args, **kwargs):
        barcode_dir = r'D:\PyWeb\media\barcodes'  # Directory for barcode images
        pdf_path = os.path.join(barcode_dir, "labels.pdf")  # Path for the generated PDF
        # Set writer options to hide the text
        writer_options = {'write_text': False}
        
        # Ensure barcode directory exists
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        # Set up the PDF canvas
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        y_position = height - 50
        
        # Iterate over all Raw Materials to generate barcodes and labels
        for raw_mat in RawMat.objects.all():
            # Generate and save the barcode image
            #barcode_content = f"{raw_mat.rm_cd} - {raw_mat.rm_des} - {raw_mat.rate}"
            barcode_content = f"{raw_mat.rm_cd} | {sanitize_input(raw_mat.rm_des)} | {raw_mat.uom} | {raw_mat.rate}"

            barcode_class = barcode.get_barcode_class('code128')
            barcode_obj = barcode_class(barcode_content, writer=ImageWriter())

            # Construct the file path without .png extension
            barcode_image_path = os.path.join(barcode_dir, raw_mat.rm_cd)
            
            # Log the action of generating the barcode
            self.stdout.write(f"Generating barcode for {raw_mat.rm_des} - {raw_mat.rm_cd}")
            
            # Save the barcode image (the save method automatically adds .png)
            saved_file = barcode_obj.save(barcode_image_path, options=writer_options)  # `saved_file` already has the .png extension
            self.stdout.write(f"Saved barcode image to: {saved_file}")

            # Use the exact saved_file path without adding .png again
            barcode_image_full_path = saved_file
            self.stdout.write(f"Looking for barcode image at: {barcode_image_full_path}")
            
            # Check if the barcode image file exists
            if os.path.exists(barcode_image_full_path):
                self.stdout.write(f"Barcode image found for {raw_mat.rm_cd}")

                # Draw the Raw Material Description and Code on the PDF
                c.drawString(100, y_position, f"Desc.: {raw_mat.rm_des} UOM:{raw_mat.uom}")
                c.drawString(100, y_position - 15, f"Code: {raw_mat.rm_cd} Rate: {raw_mat.rate} ")
            
                # Draw the barcode image below the text
                c.drawImage(barcode_image_full_path, 100, y_position - 65, width=150, height=50)
            else:
                # Log a warning if the barcode image file is not found
                self.stdout.write(self.style.WARNING(f"Barcode image not found for {raw_mat.rm_cd}"))

            # Adjust position for the next label
            y_position -= 150  # Move to the next label space
            
            if y_position < 100:
                c.showPage()  # Start a new page if out of space
                y_position = height - 50

        # Save the PDF
        c.save()
        self.stdout.write(self.style.SUCCESS(f"Labels generated successfully at {pdf_path}!"))
