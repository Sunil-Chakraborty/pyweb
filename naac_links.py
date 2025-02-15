import requests
import certifi

url = "https://assessmentonline.naac.gov.in/public/index.php/admin/get_file?file_path=..."  # Replace with an actual URL
response = requests.get(url, verify=certifi.where())

print(response.status_code)
print(response.headers)
print(response.text[:500])  # Print first 500 characters of the response
