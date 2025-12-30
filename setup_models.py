import os
import zipfile
import urllib.request
import shutil
import sys

# Comprehensive list of Vosk Models
# Source: https://alphacephei.com/vosk/models
MODELS = {
    # English
    "en-us-small": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "en-us-large": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
    "en-in-small": "https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip",
    "en-in-large": "https://alphacephei.com/vosk/models/vosk-model-en-in-0.5.zip",
    
    # Indian Languages
    "hi-small": "https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip",
    "hi-large": "https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip",
    "ta-small": "https://alphacephei.com/vosk/models/vosk-model-small-ta-0.1.zip", # Tamil
    "te-small": "https://alphacephei.com/vosk/models/vosk-model-small-te-0.4.zip", # Telugu
    "gu-small": "https://alphacephei.com/vosk/models/vosk-model-small-gu-0.42.zip", # Gujarati
    
    # Global Major Languages (Large Versions)
    "cn-large": "https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip", # Chinese
    "ru-large": "https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip", # Russian
    "fr-large": "https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip", # French
    "de-large": "https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip", # German
    "es-large": "https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip", # Spanish
    "pt-large": "https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-20220516_2113.zip", # Portuguese
    "it-large": "https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip", # Italian
    "ja-large": "https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip", # Japanese
}

BASE_DIR = os.path.join(os.getcwd(), "models")

def download_and_extract(name, url):
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    # The final directory name for the model
    extract_path = os.path.join(BASE_DIR, name)

    if os.path.exists(extract_path):
        print(f"[*] Model '{name}' already exists at {extract_path}")
        return

    print(f"[+] Downloading '{name}' from {url}...")
    
    # Progress bar hook
    def progress_hook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\r  Downloading... {percent}% ({count * block_size / (1024*1024):.1f} MB)")
        sys.stdout.flush()

    model_zip = os.path.join(BASE_DIR, f"{name}.zip")
    try:
        urllib.request.urlretrieve(url, model_zip, reporthook=progress_hook)
        print("\n[+] Download complete. Extracting...")
        
        with zipfile.ZipFile(model_zip, 'r') as zip_ref:
            # Get the top-level folder name in the zip
            zip_content_roots = {item.split('/')[0] for item in zip_ref.namelist() if '/' in item}
            if not zip_content_roots:
                 zip_content_roots = {item for item in zip_ref.namelist()}
            
            zip_ref.extractall(BASE_DIR)
            
        # The zip usually contains a versioned folder name (e.g., vosk-model-en-us-0.22)
        # We need to find it and rename it to our simple 'name' (e.g., en-us-large)
        
        # Heuristic: Find the folder that was just created/extracted that isn't our target name yet
        # Since we know the zip content root, we can check for that
        extracted_folder_name = list(zip_content_roots)[0]
        full_extracted_path = os.path.join(BASE_DIR, extracted_folder_name)
        
        if os.path.exists(full_extracted_path) and full_extracted_path != extract_path:
             print(f"  Renaming {extracted_folder_name} -> {name}")
             # Handle case where rename target exists (shouldn't happen due to check above, but for safety)
             if os.path.exists(extract_path):
                 shutil.rmtree(extract_path)
             shutil.move(full_extracted_path, extract_path)
        
        print(f"[*] Setup finished for {name}")

    except Exception as e:
        print(f"\n[!] Error downloading/extracting {name}: {e}")
    finally:
        if os.path.exists(model_zip):
            os.remove(model_zip)

def list_models():
    print("\nAvailable Models:")
    print(f"{'Name':<15} {'Type':<10} {'Description'}")
    print("-" * 60)
    for name in MODELS:
        type_str = "Large" if "large" in name else "Small"
        print(f"{name:<15} {type_str:<10} Vosk Model")
    print("-" * 60)

if __name__ == "__main__":
    passed_args = sys.argv[1:]
    
    if not passed_args or "help" in passed_args:
        print("Usage: python setup_models.py [model_name] [model_name2] ...")
        print("       python setup_models.py all    (Downloads ALL models - Warning: Huge size)")
        print("       python setup_models.py large  (Downloads all Large models)")
        print("       python setup_models.py list   (List available models)")
        list_models()
        sys.exit(0)

    if "list" in passed_args:
        list_models()
        sys.exit(0)

    targets = []
    if "all" in passed_args:
        targets = list(MODELS.keys())
    elif "large" in passed_args:
        targets = [k for k in MODELS.keys() if "large" in k]
    else:
        targets = [arg for arg in passed_args if arg in MODELS]
        
        # Warn about invalid args
        invalid = [arg for arg in passed_args if arg not in MODELS and arg not in ["all", "large"]]
        if invalid:
            print(f"[!] Warning: Unknown models skipped: {invalid}")

    if not targets:
        print("No valid models selected.")
        sys.exit(1)

    print(f"Selected models: {targets}")
    for name in targets:
        download_and_extract(name, MODELS[name])
