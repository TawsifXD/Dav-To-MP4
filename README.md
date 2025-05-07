# 🎥 DAV to MP4 Converter
### A Windows GUI tool to convert CCTV footage from `.dav` to `.mp4` format with WhatsApp-optimized presets.

![image](https://github.com/user-attachments/assets/a491b72d-b1dd-47cb-a3f5-b896b3014667)



## 🌟 Features
- **Dual Conversion Modes**:
  - WhatsApp-optimized (smaller files)
  - Standard MP4 (higher quality)
- Batch processing
- Real-time progress tracking
- Dark/light theme support
- Drag-and-drop interface

## 📦 Installation

### Method 1: Pre-built Executable
1. Download the latest release from [Releases](https://github.com/TawsifXD/Dav-To-MP4/releases)
2. Extract the ZIP file
3. Run `DAVConverter.exe`

### Method 2: From Source
```bash
git clone https://github.com/TawsifXD/Dav-To-MP4.git
cd Dav-To-MP4
pip install -r requirements.txt
python converter.py
```
## 🛠️ Usage
1. Add DAV files via "Browse" or drag-and-drop
2. Select output folder
3. Choose conversion mode:
   - WhatsApp Optimized (for smaller files)
   - Standard MP4 (for higher quality)
4. Click "Start Conversion"

## 📂 File Structure
```bash
Dav-To-MP4/
├── converter.py        # Main application
├── DAVConverter.exe    # Compiled executable
├── ffmpeg.exe          # Required binaries
├── ffprobe.exe         # Required binaries
├── requirements.txt    # Python dependencies
├── LICENSE             # License file
└── README.md           # This file
```

## ⚙️ Requirements
1. Windows 10/11
2. FFmpeg (included in release)
3. Python 3.8+ (for source version)

## 🚨 Troubleshooting
```bash
Issue	                    Solution
FFmpeg missing	            Ensure both ffmpeg.exe and ffprobe.exe are present
Conversion fails	    Verify input files are valid DAV format
```  
