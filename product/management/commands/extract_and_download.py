#Extract Google Drive Links from PDF
#pip install pymupdf

#How to Run the Command
#python manage.py extract_and_download D:\PyWeb\RANJIB_BISWAS.PDF  D:\PyWeb\Downloads

#python manage.py extract_and_download source_path target_path (pdf files)
import os
import fitz  # PyMuPDF for extracting links from PDF
import gdown  # For downloading Google Drive files
import requests  # For downloading general files
import certifi  # Fix SSL verification
from urllib.parse import urlparse, parse_qs
from django.core.management.base import BaseCommand

# Force requests to use the updated SSL certificates
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable SSL warnings

class Command(BaseCommand):
    help = "Extracts links from a PDF and downloads files (Google Drive & NAAC links)."

    def add_arguments(self, parser):
        parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
        parser.add_argument("save_dir", type=str, help="Directory to save downloaded files")

    def handle(self, *args, **options):
        pdf_path = options["pdf_path"]
        save_dir = options["save_dir"]

        # Validate paths
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f"PDF file not found: {pdf_path}"))
            return
        os.makedirs(save_dir, exist_ok=True)

        # Extract links from the PDF
        doc = fitz.open(pdf_path)
        total_links = 0
        file_index = 1

        for page_num, page in enumerate(doc, start=1):
            links = self.extract_links(page)

            if not links:
                self.stdout.write(self.style.WARNING(f"No links found on page {page_num}. Skipping..."))
                continue  # Move to the next page

            self.stdout.write(self.style.SUCCESS(f"Found {len(links)} links on page {page_num}. Downloading..."))

            # Process each link
            for link in links:
                try:
                    if "drive.google.com" in link:
                        # Handle Google Drive links
                        file_id = self.extract_file_id(link)
                        if file_id:
                            file_path = os.path.join(save_dir, f"file_{file_index}.pdf")
                            self.download_drive_file(file_id, file_path)
                            self.stdout.write(self.style.SUCCESS(f"Downloaded: {file_path}"))
                            file_index += 1
                            total_links += 1
                        else:
                            self.stdout.write(self.style.WARNING(f"Skipping invalid Google Drive link: {link}"))
                    else:
                        # Handle NAAC direct file downloads
                        file_path = self.get_valid_filename(link, save_dir, file_index)
                        if self.download_general_file(link, file_path):
                            self.stdout.write(self.style.SUCCESS(f"Downloaded: {file_path}"))
                            file_index += 1
                            total_links += 1
                        else:
                            self.stdout.write(self.style.WARNING(f"Failed to download: {link}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to process {link}: {e}"))

        if total_links == 0:
            self.stdout.write(self.style.WARNING("No valid downloadable links were found in the document."))

    def extract_links(self, page):
        """Extracts all links from a single PDF page."""
        links = []
        for link in page.get_links():
            uri = link.get("uri", "")
            if uri:
                links.append(uri)
        return links

    def extract_file_id(self, url):
        """Extracts Google Drive file ID from a link."""
        try:
            if "/d/" in url:
                return url.split("/d/")[1].split("/")[0]
            elif "id=" in url:
                return url.split("id=")[1].split("&")[0]
        except IndexError:
            return None

    def download_drive_file(self, file_id, save_path):
        """Downloads a file from Google Drive using gdown."""
        direct_link = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(direct_link, save_path, quiet=False, fuzzy=True)

    def download_general_file(self, url, save_path):
        """Downloads NAAC-hosted files using requests."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://assessmentonline.naac.gov.in/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        }
        try:
            response = requests.get(url, headers=headers, stream=True, allow_redirects=True, verify=False)  # Disabling SSL verification
            response.raise_for_status()  # Raise an error for HTTP issues

            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error downloading {url}: {e}"))
            return False

    def get_valid_filename(self, url, save_dir, file_index):
        """Generates a valid filename from the URL, avoiding query strings."""
        parsed_url = urlparse(url)
        file_name = f"file_{file_index}.pdf"  # Default name with .pdf

        # Try to get the file name from query parameters if available
        query_params = parse_qs(parsed_url.query)
        if "file_path" in query_params:
            decoded_path = query_params["file_path"][0]
            file_name = os.path.basename(decoded_path)
            if "." not in file_name:
                file_name += ".pdf"  # Ensure extension

        return os.path.join(save_dir, file_name)
