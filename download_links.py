#python download_links.py

import os
import requests
import mimetypes

# Disable SSL warnings (Optional, but not recommended for production)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://assessmentonline.naac.gov.in/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

def get_file_extension(response):
    """Determines the correct file extension from the response headers."""
    content_type = response.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(content_type)  # Automatically detect extension

    # Handle known content types
    if "application/pdf" in content_type:
        return ".pdf"
    elif "application/vnd.ms-excel" in content_type:
        return ".xls"
    elif "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type:
        return ".xlsx"
    elif "application/msword" in content_type:
        return ".doc"
    elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type:
        return ".docx"
    elif "text/csv" in content_type:
        return ".csv"
    
    return ext or ".txt"  # Save as .txt if unknown

def download_file(url, save_dir, file_index):
    """Downloads a file and assigns the correct file extension."""
    session = requests.Session()

    try:
        response = session.get(url, headers=HEADERS, stream=True, allow_redirects=True, verify=False)
        response.raise_for_status()

        # Get file extension
        file_extension = get_file_extension(response)
        file_name = f"file_{file_index}{file_extension}"
        save_path = os.path.join(save_dir, file_name)

        # Save as .txt with a clickable link if the file type is unknown
        if file_extension == ".txt":
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(f"[Download File]({url})\n")  # Markdown-style clickable link
            print(f"📄 Saved as text file with clickable link: {save_path}")
        else:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"✅ Downloaded: {save_path}")

        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")
        return False

def main():
    #input_file = r"D:\PyWeb\Extracted\extracted_links.txt"
    input_file = r"D:\PyWeb\media\extracted_links\ABHIJIT CHANDRA_Final.pdf_links.txt"
    
    save_dir = r"D:\PyWeb\Downloads"

    # Ensure download directory exists
    os.makedirs(save_dir, exist_ok=True)

    with open(input_file, "r") as file:
        links = [line.strip() for line in file.readlines() if line.strip()]

    print(f"🔄 Found {len(links)} links. Downloading...")

    for index, link in enumerate(links, start=1):
        download_file(link, save_dir, index)

    print("✅ All downloads completed.")

if __name__ == "__main__":
    main()
