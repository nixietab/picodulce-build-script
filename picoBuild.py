import os
import shutil
import requests
import zipfile
import subprocess

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")
    else:
        print(f"Folder already exists: {folder_name}")

def download_file(url, dest_path):
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Downloaded to: {dest_path}")
    else:
        print(f"Failed to download: {url} (status code: {response.status_code})")

def extract_zip(zip_path, extract_to):
    print(f"Extracting {zip_path} to {extract_to}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extraction complete")

def download_and_extract_repo(repo_url, dest_folder):
    zip_url = repo_url.rstrip("/") + "/archive/refs/heads/main.zip"
    zip_path = os.path.join(dest_folder, "repo.zip")
    print(f"Downloading repository as ZIP: {zip_url}")
    download_file(zip_url, zip_path)
    extract_zip(zip_path, dest_folder)
    os.remove(zip_path)
    print(f"Repository extracted to: {dest_folder}")

def move_folder_content(src_folder, dest_folder):
    print(f"Moving contents of {src_folder} to {dest_folder}")
    if os.path.exists(src_folder):
        for item in os.listdir(src_folder):
            src_path = os.path.join(src_folder, item)
            dest_path = os.path.join(dest_folder, item)
            shutil.move(src_path, dest_path)
        print(f"Moved contents of {src_folder} to {dest_folder}")

        # Remove the folder if empty
        if not os.listdir(src_folder):
            os.rmdir(src_folder)
            print(f"Removed empty folder: {src_folder}")
    else:
        print(f"Source folder does not exist: {src_folder}")

def main():
    # Create "progress" folder
    progress_folder = "progress"
    create_folder(progress_folder)

    # Step 2: Download PDS.zip
    pds_url = "https://github.com/nixietab/pds/releases/download/release/PDS.zip"
    pds_zip_path = os.path.join(progress_folder, "PDS.zip")
    download_file(pds_url, pds_zip_path)

    # Step 3: Extract PDS.zip
    extract_zip(pds_zip_path, progress_folder)

    # Step 4: Download and extract "picodulce" repository into "progress"
    picodulce_repo_url = "https://github.com/nixietab/picodulce"
    picodulce_dest_path = os.path.join(progress_folder, "picodulce")
    create_folder(picodulce_dest_path)
    download_and_extract_repo(picodulce_repo_url, picodulce_dest_path)

    # Step 4.1: Move "picodulce-main" contents to "progress" and remove the folder
    picodulce_main_path = os.path.join(picodulce_dest_path, "picodulce-main")
    move_folder_content(picodulce_main_path, progress_folder)

    # Step 4.2: Remove the "picodulce" folder after its contents are moved
    if os.path.exists(picodulce_dest_path):
        os.rmdir(picodulce_dest_path)
        print(f"Removed folder: {picodulce_dest_path}")

    # Step 5: Download and extract "2hsu" repository into current directory
    hsu_repo_url = "https://github.com/nixietab/2hsu"
    hsu_dest_path = os.path.join(os.getcwd(), "2hsu")
    create_folder(hsu_dest_path)
    download_and_extract_repo(hsu_repo_url, hsu_dest_path)

    # Step 5.1: Move "2hsu-main" contents to current directory and remove the folder
    hsu_main_path = os.path.join(hsu_dest_path, "2hsu-main")
    move_folder_content(hsu_main_path, os.getcwd())

    # Step 5.2: Remove the "2hsu" folder after its contents are moved
    if os.path.exists(hsu_dest_path):
        os.rmdir(hsu_dest_path)
        print(f"Removed folder: {hsu_dest_path}")


def compile_with_pyinstaller():
    command = [
        "pyinstaller",
        "--onefile",
        "--add-data", ".:.",
        "--console",
        "--icon=icon.png",
        "--distpath", "build",
        "2hsu.py"
    ]
    subprocess.run(command, check=True)
    print("Compilation complete.")

def rename_progress_folder():
    # Check if the "progress" folder exists
    if os.path.exists('progress'):
        # Rename it to "picodulce"
        os.rename('progress', 'picodulce')
        print("Folder 'progress' has been renamed to 'picodulce'.")
    else:
        print("The 'progress' folder does not exist.")

if __name__ == "__main__":
    main()
    rename_progress_folder()
    compile_with_pyinstaller()
