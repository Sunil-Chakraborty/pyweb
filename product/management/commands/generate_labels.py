from django.core.management.base import BaseCommand
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from product.models import RawMat
import os
import barcode
from barcode.writer import ImageWriter

class Command(BaseCommand):
    help = 'Generates barcode images and a PDF with barcodes for printing labels'

    def handle(self, *args, **kwargs):
        barcode_dir = r'D:\PyWeb\media\barcodes'
        pdf_path = os.path.join(barcode_dir, "labels.pdf")
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        y_position = height - 50
        
        for raw_mat in RawMat.objects.all():
            barcode_class = barcode.get_barcode_class('code128')
            barcode_obj = barcode_class(str(raw_mat.rm_cd), writer=ImageWriter())
            barcode_image_path = os.path.join(barcode_dir, f'{raw_mat.rm_cd}.png')
            print(f"Saving barcode for {raw_mat.rm_des} - {raw_mat.rm_cd} to: {barcode_image_path}")
            barcode_obj.save(barcode_image_path)

            # Add raw material details and barcode image to the PDF
            c.drawString(100, y_position, f"{raw_mat.rm_des} - {raw_mat.rm_cd}")
            if os.path.exists(barcode_image_path):
                c.drawImage(barcode_image_path, 100, y_position - 50, width=150, height=50)
            else:
                self.stdout.write(self.style.WARNING(f"Barcode image not found for {raw_mat.rm_cd}"))

            y_position -= 150  # Move to the next label space
            if y_position < 100:
                c.showPage()  # Start a new page if out of space
                y_position = height - 50

        # Save the PDF
        c.save()
        self.stdout.write(self.style.SUCCESS(f"Labels generated successfully at {pdf_path}!"))
