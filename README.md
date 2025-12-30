# 🎙️ Live Multilingual ANN Speech-to-Text

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Vosk](https://img.shields.io/badge/Engine-Vosk-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Offline-red)

A high-performance, **Neural Network-based** Speech-to-Text (STT) engine that runs **completely offline**. Built with [Vosk](https://alphacephei.com/vosk/) and Python, it supports real-time transcription for 20+ languages including robust support for **Indian English** and **Hindi**.

**No LLMs. No Cloud APIs. Just fast, private, and accurate speech recognition.**

---

## 🚀 Key Features

- **🔒 100% Offline**: All processing happens locally on your machine. No data is sent to the cloud.
- **🧠 Neural Network Powered**: Uses Kaldi-based Deep Neural Networks (DNNs/RNNs) for state-of-the-art accuracy.
- **🏎️ Real-Time**: Instant transcription from your microphone.
- **🌍 Multilingual**: Support for English (US/IN), Hindi, Chinese, Russian, French, German, and [many more](#supported-models).
- **⚡ Lightweight to Large**: Choose between small mobile models (50MB) for speed or large server models (1GB+) for maximum accuracy.
- **🛡️ Noise Gate**: Integrated energy-based noise suppression to reduce hallucinations.

---

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- A working microphone

### 1. Clone the Repository

```bash
git clone https://github.com/ShreyashDarade//STT.git
cd STT
```

### 2. Install Dependencies

```bash
pip install vosk pyaudio
```

> _Note for Linux users: You may need to install `portaudio` (e.g., `sudo apt install python3-pyaudio`)._

### 3. Download Models

Use the included helper script to download the models you need.

**List available models:**

```bash
python setup_models.py list
```

**Download specific models:**

```bash
python setup_models.py en-in-large hi-large
```

**Download all "Large" (High Accuracy) models:**

```bash
python setup_models.py large
```

---

## 🎤 Usage

Run the main application:

```bash
python src/main.py
```

1.  The app will scan your `models/` directory.
2.  Select the language/model from the list.
3.  Start speaking!

### Keyboard Shortcuts

- `Ctrl+C`: Stop recording and exit.

---

## 📦 Supported Models (Quick List)

The `setup_models.py` script makes it easy to manage these models.

| Language           | Code          | Type  | Size    |
| :----------------- | :------------ | :---- | :------ |
| **Indian English** | `en-in-large` | Large | ~1.0 GB |
| **Indian English** | `en-in-small` | Small | ~50 MB  |
| **Hindi**          | `hi-large`    | Large | ~1.5 GB |
| **Hindi**          | `hi-small`    | Small | ~50 MB  |
| **US English**     | `en-us-large` | Large | ~1.8 GB |
| **Chinese**        | `cn-large`    | Large | ~1.0 GB |
| **French**         | `fr-large`    | Large | ~1.4 GB |
| **German**         | `de-large`    | Large | ~1.9 GB |
| **Russian**        | `ru-large`    | Large | ~1.0 GB |
| **Tamil**          | `ta-small`    | Small | ~50 MB  |

_Run `python setup_models.py list` for the full supported list._

---

## ⚙️ Configuration

### Noise Gate

To adjust the microphone sensitivity, edit `src/audio.py`:

```python
# Increase threshold if background noise is being detected as text
# Decrease it if your voice is being cut off
def __init__(self, rate=16000, chunk=8000, threshold=500):
```

### Confidence Threshold

The app displays a confidence score (e.g., `[75%]`) for words below 80% confidence. You can adjust this in `src/main.py`.

---

## 🤝 Contributing

Contributions are welcome!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Vosk API](https://alphacephei.com/vosk/) for the incredible offline speech recognition engine.
