#Extract Google Drive Links from PDF
#pip install pymupdf

#How to Run the Command
#python manage.py extract_and_download D:\PyWeb\cas1.pdf D:\PyWeb\Downloads

#python manage.py extract_and_download source_path target_path (pdf files)


import os
import fitz  # PyMuPDF for extracting links from PDF
import gdown  # For downloading files from Google Drive
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Extracts Google Drive links from a PDF and downloads the files."

    def add_arguments(self, parser):
        parser.add_argument("pdf_path", nargs="?", type=str, help="Path to the PDF file")
        parser.add_argument("save_dir", nargs="?", type=str, help="Directory to save downloaded files")

    def handle(self, *args, **options):
        pdf_path = options["pdf_path"]
        save_dir = options["save_dir"]

        # Prompt user for input if arguments are missing
        if not pdf_path:
            pdf_path = input("Enter the path to the PDF file: ").strip()
        if not save_dir:
            save_dir = input("Enter the directory to save downloaded files: ").strip()

        # Validate PDF path
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f"PDF file not found: {pdf_path}"))
            return

        # Ensure save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Extract links page by page
        doc = fitz.open(pdf_path)
        total_links = 0
        file_index = 1

        for page_num, page in enumerate(doc, start=1):
            links = self.extract_links(page)

            if not links:
                self.stdout.write(self.style.WARNING(f"No Google Drive links found on page {page_num}. Skipping..."))
                continue  # Move to the next page

            self.stdout.write(self.style.SUCCESS(f"Found {len(links)} links on page {page_num}. Downloading..."))

            # Download files
            for link in links:
                try:
                    file_id = self.extract_file_id(link)
                    if file_id:
                        file_path = os.path.join(save_dir, f"file_{file_index}.pdf")
                        self.download_drive_file(file_id, file_path)
                        self.stdout.write(self.style.SUCCESS(f"Downloaded: {file_path}"))
                        file_index += 1
                        total_links += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"Skipping invalid link: {link}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to download {link}: {e}"))

        if total_links == 0:
            self.stdout.write(self.style.WARNING("No valid Google Drive links were found in the entire document."))

    def extract_links(self, page):
        """Extract Google Drive links from a single PDF page."""
        links = []
        for link in page.get_links():
            uri = link.get("uri", "")
            if "drive.google.com" in uri:
                links.append(uri)
        return links

    def extract_file_id(self, url):
        """Extract the Google Drive file ID from a link."""
        try:
            file_id = url.split("/d/")[1].split("/")[0]
            return file_id
        except IndexError:
            return None

    def download_drive_file(self, file_id, save_path):
        """Download a file from Google Drive."""
        direct_link = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(direct_link, save_path, quiet=False, fuzzy=True)
        
