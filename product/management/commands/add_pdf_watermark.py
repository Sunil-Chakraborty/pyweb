from django.core.management.base import BaseCommand
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#convert pdf to pdf with watermark_text
#python manage.py add_pdf_watermark "D:\PyWeb\media\resources\pdf\cas_modified.pdf" "D:\PyWeb\media\resources\pdf\cas_mod_watermark.pdf" --watermark_text "Confidential"
#or python manage.py add_pdf_watermark "D:\PyWeb\media\resources\pdf\cas.pdf" "D:\PyWeb\media\resources\pdf\cas_mod_watermark.pdf" --watermark_text "Confidential"


class Command(BaseCommand):
    help = "Add a watermark to each page of a PDF"

    def add_arguments(self, parser):
        parser.add_argument("input_pdf", type=str, help="Path to the input PDF file")
        parser.add_argument("output_pdf", type=str, help="Path to the output PDF file")
        parser.add_argument("--watermark_text", type=str, help="Text for the watermark", required=True)

    def handle(self, *args, **options):
        input_pdf = options["input_pdf"]
        output_pdf = options["output_pdf"]
        watermark_text = options["watermark_text"]
        
        self.apply_watermark(input_pdf, output_pdf, watermark_text)
        self.stdout.write(self.style.SUCCESS(f"Watermark applied and saved to {output_pdf}"))

    def apply_watermark(self, input_pdf, output_pdf, watermark_text):
        # Step 1: Create a temporary watermark PDF
        watermark_pdf = "temp_watermark.pdf"
        c = canvas.Canvas(watermark_pdf, pagesize=letter)
        c.setFont("Helvetica", 40)
        c.setFillGray(0.5, alpha=0.3)
        text_x = (letter[0] / 2) - 100
        text_y = letter[1] / 2
        c.drawString(text_x, text_y, watermark_text)
        c.save()

        # Step 2: Merge the watermark with each page of the input PDF
        reader = PdfReader(input_pdf)
        watermark = PdfReader(watermark_pdf).pages[0]
        writer = PdfWriter()

        for page_num, page in enumerate(reader.pages):
            page.merge_page(watermark)
            writer.add_page(page)
            self.stdout.write(f"Watermark applied on page {page_num + 1}")

        # Step 3: Save the final PDF
        with open(output_pdf, "wb") as f:
            writer.write(f)

        os.remove(watermark_pdf)
