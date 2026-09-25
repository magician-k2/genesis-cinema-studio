import os
import zipfile

def package_chrome_extension():
    source_dir = r"G:\マイドライブ\GENESIS_ROOT\browser_extension"
    output_dir = r"G:\マイドライブ\GENESIS_ROOT\outputs"
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, "GENESIS_muTRON_XAI_Chrome_Extension_v1.0.zip")
    
    files_to_pack = [
        "manifest.json",
        "background.js",
        "content_script.js",
        "sidepanel.html",
        "sidepanel.js",
        "settings.html",
        "settings.js",
        "README_FOR_PARTNER.md"
    ]
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in files_to_pack:
            file_path = os.path.join(source_dir, file_name)
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=f"GENESIS_muTRON_XAI_v1.0/{file_name}")
                print(f"Added: {file_name}")
            else:
                print(f"Warning: {file_name} not found!")
                
    print(f"\nSuccessfully generated extension package: {zip_path}")
    print(f"File size: {os.path.getsize(zip_path):,} bytes")

if __name__ == "__main__":
    package_chrome_extension()
