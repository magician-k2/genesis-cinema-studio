import os
import zipfile
from pathlib import Path

def repackage():
    staging_dir = Path("kaggle_submission_staging")
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    
    zip_paths = [
        out_dir / "kaggle_gemma4_submission.zip",
        Path("submission.zip")
    ]
    
    for zip_path in zip_paths:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(staging_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(staging_dir)
                    zf.write(file_path, arcname)
        print(f"Packed: {zip_path} (Size: {os.path.getsize(zip_path):,} bytes)")

if __name__ == "__main__":
    repackage()
