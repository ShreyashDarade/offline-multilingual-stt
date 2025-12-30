import os
import json
from vosk import Model, KaldiRecognizer

class SpeechRecognizer:
    def __init__(self, models_dir):
        self.models_dir = models_dir
        self.models = {}
        self.current_model = None
        self.rec = None
        
    def load_model(self, lang_code):
        """Loads a model for a specific language code (e.g., 'en-in', 'hi')."""
        if lang_code in self.models:
            print(f"Model {lang_code} already loaded.")
            self.current_model = self.models[lang_code]
        else:
            model_path = os.path.join(self.models_dir, lang_code)
            if not os.path.exists(model_path):
                raise ValueError(f"Model for language '{lang_code}' not found at {model_path}.")
            
            print(f"Loading model for {lang_code}...")
            model = Model(model_path)
            self.models[lang_code] = model
            self.current_model = model
            
        # Create a recognizer with 16kHz
        self.rec = KaldiRecognizer(self.current_model, 16000)
    
    def process_audio(self, data):
        """
        Accepts binary audio data and returns:
          - (True, text) if a full sentence is recognized
          - (False, partial_text) if it's partial result
        """
        if not self.rec:
            return False, ""

        if self.rec.AcceptWaveform(data):
            res = json.loads(self.rec.Result())
            text = res.get("text", "")
            
            # Calculate average confidence
            avg_conf = 0.0
            if "result" in res:
                confs = [w.get("conf", 1.0) for w in res["result"]]
                if confs:
                    avg_conf = sum(confs) / len(confs)
            
            return True, text, avg_conf
        else:
            partial = json.loads(self.rec.PartialResult())
            return False, partial.get("partial", ""), 0.0

    def get_final_result(self):
        if self.rec:
            return json.loads(self.rec.FinalResult()).get("text", "")
        return ""
