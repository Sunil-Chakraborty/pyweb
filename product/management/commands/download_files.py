#python manage.py download_files D:\PyWeb\Extracted\extracted_links.txt D:\PyWeb\Downloads


import os
import gdown  # For downloading Google Drive files
import requests  # For downloading general files
import certifi  # Fix SSL verification
from urllib.parse import urlparse, parse_qs
from django.core.management.base import BaseCommand

# Force requests to use the updated SSL certificates
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


class Command(BaseCommand):
    help = "Reads links from a file and downloads files from Google Drive & NAAC."

    def add_arguments(self, parser):
        parser.add_argument("links_file", type=str, help="Path to the extracted_links.txt file")
        parser.add_argument("save_dir", type=str, help="Directory to save downloaded files")

    def handle(self, *args, **options):
        links_file = options["links_file"]
        save_dir = options["save_dir"]

        # Validate input files and paths
        if not os.path.exists(links_file):
            self.stdout.write(self.style.ERROR(f"Links file not found: {links_file}"))
            return

        os.makedirs(save_dir, exist_ok=True)

        # Read all links from the file
        with open(links_file, "r") as f:
            links = [line.strip() for line in f if line.strip()]

        if not links:
            self.stdout.write(self.style.WARNING("No links found in the file."))
            return

        self.stdout.write(self.style.SUCCESS(f"Found {len(links)} links. Downloading..."))

        file_index = 1
        for link in links:
            try:
                if "drive.google.com" in link:
                    # Handle Google Drive links
                    file_id = self.extract_drive_file_id(link)
                    if file_id:
                        file_path = os.path.join(save_dir, f"file_{file_index}.pdf")
                        self.download_drive_file(file_id, file_path)
                        self.stdout.write(self.style.SUCCESS(f"Downloaded: {file_path}"))
                        file_index += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"Skipping invalid Google Drive link: {link}"))
                else:
                    # Handle NAAC direct file downloads
                    file_path = self.get_valid_filename(link, save_dir, file_index)
                    if self.download_general_file(link, file_path):
                        self.stdout.write(self.style.SUCCESS(f"Downloaded: {file_path}"))
                        file_index += 1
                    else:
                        self.stdout.write(self.style.WARNING(f"Failed to download: {link}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to process {link}: {e}"))

    def extract_drive_file_id(self, url):
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
        """Downloads a general file (e.g., NAAC-hosted files) with SSL verification enabled."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, stream=True, allow_redirects=True, verify=certifi.where())
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
