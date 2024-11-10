import os
from django.core.management.base import BaseCommand, CommandError
from PyPDF2 import PdfReader, PdfWriter

# python manage.py add_pdf_password cas.pdf cas123
#In this example:
#cas.pdf should be located in D:\\PyWeb\\media\\resources\\pdf.
#The output file will be named cas_pwd.pdf and saved in the same directory.


class Command(BaseCommand):
    help = "Add password protection to a PDF file."

    def add_arguments(self, parser):
        parser.add_argument("input_pdf", type=str, help="Filename of the input PDF file (should be in default path)")
        parser.add_argument("password", type=str, help="Password to apply to the PDF")

    def handle(self, *args, **options):
        default_path = os.path.join("D:\\PyWeb\\media\\resources\\pdf")
        input_pdf_filename = options["input_pdf"]
        password = options["password"]

        # Construct full input path
        input_pdf = os.path.join(default_path, input_pdf_filename)
        
        # Check if the input PDF exists
        if not os.path.exists(input_pdf):
            raise CommandError(f"The file {input_pdf} does not exist.")

        # Construct output PDF filename with "_pwd" suffix
        output_pdf_filename = os.path.splitext(input_pdf_filename)[0] + "_pwd.pdf"
        output_pdf = os.path.join(default_path, output_pdf_filename)

        # Add password protection to the PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)

        writer.encrypt(password)

        # Save the password-protected PDF to output path
        with open(output_pdf, "wb") as output_pdf_file:
            writer.write(output_pdf_file)

        self.stdout.write(self.style.SUCCESS(f"Password-protected PDF saved to: {output_pdf}"))
