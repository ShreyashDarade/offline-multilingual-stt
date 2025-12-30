import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio import MicrophoneStream
from recognizer import SpeechRecognizer

def get_installed_models(models_dir):
    """Scans the models directory and returns a list of available model names."""
    if not os.path.exists(models_dir):
        return []
    return [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]

def main():
    print("="*60)
    print("      Live Multilingual ANN Speech-to-Text (Vosk)")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")
    
    if not os.path.exists(models_dir):
        print(f"[!] Error: Models directory not found at {models_dir}")
        print("    Run 'python setup_models.py' to download models.")
        return

    available_models = get_installed_models(models_dir)
    available_models.sort() # Alphabetical order

    if not available_models:
        print(f"[!] No models found in {models_dir}")
        print("    Run 'python setup_models.py list' to see available models.")
        print("    Example: 'python setup_models.py en-us-small'")
        return

    recognizer = SpeechRecognizer(models_dir)
    
    # Dynamic Selection Menu
    print("\nInstalled Models:")
    for idx, model_name in enumerate(available_models):
        print(f"  {idx + 1}. {model_name}")
    
    print("-" * 30)
    choice = input(f"Select Model (1-{len(available_models)}): ").strip()
    
    selected_model = None
    try:
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(available_models):
                selected_model = available_models[idx]
        else:
            # Allow typing the name directly
            if choice in available_models:
                selected_model = choice
    except Exception:
        pass

    if not selected_model:
        print("[!] Invalid selection. Exiting.")
        return

    print(f"\n[*] Initializing '{selected_model}'... (Please wait)")
    try:
        recognizer.load_model(selected_model)
    except Exception as e:
        print(f"[!] Failed to load model: {e}")
        return

    print(f"\n[*] Model loaded. Listening... (Press Ctrl+C to stop)")
    print(f"[*] Confidence threshold for display: 80%")
    print("=" * 60)

    try:
        with MicrophoneStream() as stream:
            audio_generator = stream.generator()
            for content in audio_generator:
                is_full, text, conf = recognizer.process_audio(content)
                if is_full:
                    if text:
                        # Confidence display
                        conf_str = f" [{conf:.0%}]" if conf < 0.8 else ""
                        print(f"\r>> {text}{conf_str}                                    ")
                else:
                    if text:
                        print(f"\r   ... {text}", end="", flush=True)

    except KeyboardInterrupt:
        print("\n\n[*] Stopping...")
        final = recognizer.get_final_result()
        if final:
            print(f">> {final}")
        print("Goodbye.")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
