import mwclient
import os
import difflib
import sys
from termcolor import colored

# Function to read the content of a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to compare and display differences with color coding
def show_differences(local_content, remote_content):
    diff = difflib.unified_diff(
        remote_content.splitlines(), 
        local_content.splitlines(), 
        fromfile='remote', 
        tofile='local', 
        lineterm=''
    )
    for line in diff:
        if line.startswith('+'):
            print(colored(line, 'green'))
        elif line.startswith('-'):
            print(colored(line, 'red'))
        else:
            print(line)

# Get username and password from environment variables
username = os.getenv('MW_USERNAME')
password = os.getenv('MW_PASSWORD')

if not username or not password:
    print("Username and password must be set in environment variables MW_USERNAME and MW_PASSWORD.")
    sys.exit(1)

# Connect to the MediaWiki site
site = mwclient.Site('paradisestation.org', path='/wiki/', scheme='https')

try:
    site.login(username, password)
except mwclient.errors.LoginError as e:
    print(f"Login failed: {e}")
    sys.exit(1)

# Function to determine the page name from the file path
def get_page_name(file_path):
    return os.path.relpath(file_path, 'wiki').replace('_', ' ').replace('\\', '/').replace('.wiki', '')

# Function to process a single file
def process_file(file_path):
    page_name = get_page_name(file_path)
    local_content = read_file(file_path)
    
    try:
        page = site.pages[page_name]
        remote_content = page.text()
    except mwclient.errors.InvalidResponse as e:
        print(f"Failed to fetch page {page_name}: {e}")
        return

    if local_content != remote_content:
        print(f"Changes detected for page: {page_name}")
        show_differences(local_content, remote_content)
        
        confirm = input(f"Do you want to push these changes to {page_name}? (Y/N): ").strip().lower()
        if confirm == 'y':
            commit_message = input("Enter commit message (or leave blank to cancel): ").strip()
            if commit_message:
                confirm_commit = input(f"Are you sure you want to commit changes to {page_name}? (Y/N): ").strip().lower()
                if confirm_commit == 'y':
                    try:
                        page.save(local_content, summary=commit_message)
                        print(f"Updated page: {page_name}")
                    except mwclient.errors.EditError as e:
                        print(f"Failed to update page {page_name}: {e}")
                else:
                    print(f"Cancelled updating page: {page_name}")
            else:
                print(f"Cancelled updating page: {page_name}")
        else:
            print(f"Skipped updating page: {page_name}")
    else:
        print(f"No changes for page: {page_name}")

# Get the filename from command line arguments
if len(sys.argv) < 2:
    print("Please provide the file path as an argument.")
else:
    # Process the single file provided as argument
    file_path = sys.argv[1]
    process_file(file_path)

print("Upload process complete.")