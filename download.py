import mwclient
import os
import requests
import sys

# Ensure that do_images is passed as a script parameter
if len(sys.argv) != 2:
    print("Usage: python script.py <do_images>")
    sys.exit(1)

do_images = sys.argv[1].lower() == 'true'

# Get username and password from environment variables
username = os.getenv('MW_USERNAME')
password = os.getenv('MW_PASSWORD')

if not username or not password:
    print("Username and password must be set in environment variables MW_USERNAME and MW_PASSWORD.")
    sys.exit(1)

# Connect to the MediaWiki site and log in
site = mwclient.Site('paradisestation.org', path='/wiki/', scheme='https')
site.login(username, password)

# Ensure the output directory exists
output_dir = 'wiki'
media_dir = os.path.join(output_dir, 'media')
os.makedirs(media_dir, exist_ok=True)

# Function to safely create directories
def safe_create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Downloading all pages and media files
all_pages = site.allpages()
for page in all_pages:
    text = page.text()
    
    page_path = page.name.replace(' ', '_')  # Handle spaces in page names
    file_path = os.path.join(output_dir, f"{page_path}.wiki")
    
    # Create directories as needed
    safe_create_dir(os.path.dirname(file_path))
    
    # Write the page content to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Downloaded: {page.name}")

    if do_images:
        # Find and download media files
        for image in page.images():
            image_name = image.name.replace(' ', '_')
            image_path = os.path.join(media_dir, image_name)
            
            # Handle missing 'url' key
            image_info = image.imageinfo or {}
            image_url = image_info.get('url')
            if image_url:
                response = requests.get(image_url)
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Downloaded image: {image_name}")
            else:
                print(f"No URL found for image: {image_name}")

print("Download complete.")