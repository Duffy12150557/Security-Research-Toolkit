# Security-Research-Toolkit
Security Research Toolkit — Video and image analysis tool for neural inpainting and AI-generated content detection with SORA signature extraction, temporal consistency analysis, CNN artifact detection, CPU/CUDA device selection, multi-format support, and colorama-styled terminal interface
<div align="center">

```
 __          _______ _    _  _____    _____                      _ _          
 \ \        / / ____| |  | |/ ____|  / ____|                    (_) |         
  \ \  /\  / / (___ | |  | | (___   | (___   ___  ___ _   _ _ __ _| |_ _   _  
   \ \/  \/ / \___ \| |  | |\___ \   \___ \ / _ \/ __| | | | '__| | __| | | | 
    \  /\  /  ____) | |__| |____) |  ____) |  __/ (__| |_| | |  | | |_| |_| | 
     \/  \/  |_____/ \____/|_____/  |_____/ \___|\___|\__,_|_|  |_|\__|\__, | 
                                                                        __/ | 
 _____                               _       _______          _ _    _|___/  
|  __ \                             | |     |__   __|        | | |  (_) |    
| |__) |___  ___  ___  __ _ _ __ ___| |__      | | ___   ___ | | | ___| |_   
|  _  // _ \/ __|/ _ \/ _` | '__/ __| '_ \     | |/ _ \ / _ \| | |/ / | __|  
| | \ \  __/\__ \  __/ (_| | | | (__| | | |    | | (_) | (_) | |   <| | |_   
|_|  \_\___||___/\___|\__,_|_|  \___|_| |_|    |_|\___/ \___/|_|_|\_\_|\__|  
```

# Security Research Toolkit

[![Python](https://img.shields.io/badge/Python-3.4+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com)
[![CUDA](https://img.shields.io/badge/CUDA-Optional-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)

**Video & image analysis for neural inpainting and AI-generated content detection**

[Features](#-features) • [Getting Started](#-getting-started) • [Configuration](#-configuration) • [Usage](#-usage) • [Project Structure](#-project-structure) • [FAQ](#-faq)

</div>

---

## Official Links

| Resource | URL |
|----------|-----|
| Repository | `https://github.com/timanmoh/Security-Research-Toolkit` |
| Issues | `https://github.com/timanmoh/Security-Research-Toolkit/issues` |
| OpenAI Sora | https://openai.com/index/sora |
| Reality Defender (Sora detection) | https://www.realitydefender.com/insights/detecting-sora-videos |

---

## Features

<table>
<tr>
<td width="50%">

**Analysis**
- [x] Video frame validation (MP4, AVI, MKV, MOV, WebM, WMV, FLV)
- [x] Image validation (PNG, JPG, BMP, WebP, TIFF)
- [x] Input path validation & format detection
- [x] Output directory management

**Detection**
- [x] SORA signature feature extraction
- [x] Temporal consistency analysis
- [x] Interpolation detection
- [x] CNN region/artifact detection

</td>
<td width="50%">

**Processing**
- [x] Neural inpainting pipeline (frame/mask)
- [x] Batch video frame processing
- [x] CPU/CUDA device selection
- [x] GPU status via nvidia-smi

**Interface**
- [x] Interactive terminal interface
- [x] Colored output (colorama)
- [x] Multi-language (EN/RU)
- [x] Settings persistence (JSON)

</td>
</tr>
</table>

---

## Getting Started

### Prerequisites

- **Python** 3.4 or higher
- **Optional:** NVIDIA GPU with CUDA for accelerated processing
- **Optional:** PyTorch with CUDA support (auto-detected)

### Installation

```bash
git clone https://github.com/timanmoh/Security-Research-Toolkit.git
cd Security-Research-Toolkit
pip install -r requirements.txt
python main.py
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| colorama | ≥0.4.6 | Cross-platform colored console output |

*Note: Neural inpainting and detection modules use default implementations. Advanced models (AOT-GAN, LaMa, ProPainter) can be integrated for higher accuracy.*

---

## Configuration

Settings are stored in `settings.json` in the project root. Edit via menu **Settings** or command `settings`.

**Example `settings.json`:**

```json
{
  "device": "auto",
  "output_dir": "./output",
  "log_level": "info",
  "language": "en"
}
```

| Parameter | Values | Description |
|-----------|--------|-------------|
| `device` | `auto`, `cpu`, `cuda` | Compute device; `auto` selects GPU if available |
| `output_dir` | path | Output directory (relative or absolute); created on first save |
| `log_level` | `debug`, `info`, `warning`, `error` | Console verbosity |
| `language` | `en`, `ru` | Interface language |

> **Tip:** Use `device=cpu` for headless servers without GPU. Use `log_level=debug` when troubleshooting.

---

## Usage

### Interactive Mode (default)

```bash
python main.py
# or
python main.py --interactive
```

**Main menu:**

```
┌──────────────────────────────────────────────────────────────┐
│  [1] Install dependencies                                     │
│  [2] Start                                                    │
│  [3] About                                                    │
│  [4] Settings                                                 │
└──────────────────────────────────────────────────────────────┘

  Choose [1]-[4]: 2
```

**Command menu:**

```
> run C:\videos\sample.mp4
> validate ./images/frame_001.png
> gpu
> settings
> help
> quit
```

### CLI Mode

```bash
python main.py --run <video_or_image_path>
python main.py --validate <path>
python main.py --gpu
```

| Command | Description |
|---------|-------------|
| `run <path>` | Process video or image (detect + inpainting pipeline) |
| `validate <path>` | Validate input file and report type (video/image) |
| `gpu` | Show NVIDIA GPU status (nvidia-smi) |
| `install` / `1` | Install dependencies from requirements.txt |
| `about` | Show project info from README |
| `settings` | View/edit settings (device, output_dir, log_level, language) |
| `help` | Show command menu |
| `quit` / `exit` | Exit application |

---

## Project Structure

```
Security-Research-Toolkit/
├── main.py                 # Entry point (CLI, interactive menu)
├── settings.json           # User settings (created on first save)
├── requirements.txt        # Python dependencies
├── README.md
│
├── gui/
│   ├── __init__.py
│   └── main_window.py      # Terminal interface (banner, menu, sections)
│
├── core/
│   ├── __init__.py
│   ├── processor.py        # Video/image processing pipeline
│   ├── inpainting.py       # Neural inpainting (region filling)
│   └── validator.py        # Input path validation
│
├── detection/
│   ├── __init__.py
│   ├── detector.py         # CNN region/artifact detection
│   ├── signature.py        # SORA signature analysis
│   └── temporal.py         # Temporal consistency, interpolation
│
└── utils/
    ├── __init__.py
    ├── settings.py         # Load/save settings.json
    ├── file_handler.py     # File operations, path sanitization
    ├── gpu_manager.py      # GPU info, device suggestion
    └── logger.py           # Logging utilities
```

---

## FAQ

<details>
<summary><b>What video formats are supported?</b></summary>

MP4, AVI, MKV, MOV, WebM, WMV, and FLV. Image formats: PNG, JPG, JPEG, BMP, WebP, TIFF, TIF.
</details>

<details>
<summary><b>Does it work without a GPU?</b></summary>

Yes. The toolkit runs on CPU by default. Set `device=cpu` in settings or use `auto` to let the app detect CUDA availability. GPU acceleration is optional.
</details>

<details>
<summary><b>What is SORA signature detection?</b></summary>

SORA is OpenAI's text-to-video model. The detection module analyzes temporal consistency, generation artifacts, and feature signatures to identify AI-generated content. The current implementation provides extensible interfaces for integrating custom classifiers.
</details>

<details>
<summary><b>How do I add real neural inpainting?</b></summary>

Extend the base implementation in `core/inpainting.py` with a model such as AOT-GAN, LaMa, or ProPainter. The `inpaint_frame(frame_region, mask_region, device)` function expects numpy/tensor input and returns the inpainted region.
</details>

<details>
<summary><b>Settings are not saving. What to check?</b></summary>

Ensure the project directory is writable. `settings.json` is created in the project root. On Windows, run as administrator if the folder has restricted permissions. Check that only valid keys (`device`, `output_dir`, `log_level`, `language`) and values are used.
</details>

<details>
<summary><b>nvidia-smi not found / GPU not detected</b></summary>

Install NVIDIA drivers and ensure `nvidia-smi` is in PATH. On Linux, it is typically in `/usr/bin`. The toolkit falls back to CPU if no GPU is detected. PyTorch CUDA support is optional and checked at runtime.
</details>

<details>
<summary><b>Can I use this for production?</b></summary>

This is a research/educational toolkit. Detection and inpainting modules are extensible base implementations. For production use, integrate validated models, add error handling, and perform security audits. See the Disclaimer below.
</details>

---

## Disclaimer

This project is intended **exclusively for educational and security research purposes**. Use it only on content you own or have explicit permission to analyze. Do not use it to create, distribute, or analyze deepfakes or manipulated media for deceptive purposes. The authors are not responsible for misuse. AI-generated content detection is an evolving field; results may be inaccurate. Always comply with local laws and platform terms of service.

---

<div align="center">

**If this project helped your research, consider giving it a star.**

ETH: `0x6f1A3c5E9B2a4D6e8C0b3F5a7D9c1E3b5A7f28e1`

</div>
