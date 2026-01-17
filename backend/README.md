
# ClipForge Backend

This backend provides video processing APIs for **caption generation, editing, and chat-based modifications** using component models like Whisper for transcription.  

---

## Table of Contents

- [Requirements](#requirements)  
- [Installation](#installation)  
- [Folder Structure](#folder-structure)  
- [Running the Server](#running-the-server)  
- [API Endpoints](#api-endpoints)  
- [Troubleshooting](#troubleshooting)  

---

## Requirements

- Python 3.10+  
- FFmpeg installed and added to your system PATH  
- Virtual environment (recommended)  

Python packages (from `requirements.txt`):

- fastapi  
- uvicorn  
- whisper  
- moviepy  
- python-multipart  

---

## Installation

1. **Clone the repository**:

```bash
git clone <repo-url>
cd Auraverse
````

2. **Create a virtual environment**:

```bash
python -m venv venv
```

3. **Activate the virtual environment**:

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
venv\Scripts\activate
```

4. **Install dependencies**:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Ensure directories exist** (uploads & outputs):

```bash
mkdir uploads outputs
```

---

## Folder Structure

```
backend/
├─ main.py          # FastAPI entrypoint, defines /process and /chat endpoints
├─ transcription.py # Handles audio → text using Whisper
├─ rules.py         # Defines rules for caption styles and animations
├─ renderer.py      # Applies edits and generates the final video
├─ chat.py          # Modifies edit plans based on chat commands
uploads/             # Temporary folder for uploaded videos
outputs/             # Folder for processed videos
requirements.txt     # Python dependencies
```

---

## Running the Server

From the project root:

```bash
uvicorn backend.main:app --reload
```

* The server runs on [http://127.0.0.1:8000](http://127.0.0.1:8000)
* `--reload` enables live-reload when you edit code

---

## API Endpoints

### 1. `/process` – Upload and process video

* **Method:** POST
* **Request:** multipart/form-data

  * `file`: Video file (`.mp4`)
* **Response:** JSON

Example:

```json
{
  "video": "outputs/vdo1.mp4",
  "edits": [
    {"start": 0, "end": 3, "text": "Hello World", "style": "title", "animation": "fade"},
    ...
  ]
}
```

### 2. `/chat` – Edit video captions via text command

* **Method:** POST
* **Query Params:**

  * `video_name` – Name of uploaded video in `uploads/`
  * `message` – Command text like `"make captions bolder"`
* **Response:** JSON with updated video path and edits

Example:

```json
{
  "video": "outputs/vdo1.mp4",
  "edits": [
    {"start": 0, "end": 3, "text": "Hello World", "fontsize": 40, "animation": "fade"},
    ...
  ]
}
```

---

## Notes & Troubleshooting

1. **500 Internal Server Error**

   Usually occurs when Whisper fails to extract audio from the video.

   * Check if FFmpeg is installed and in PATH
   * Confirm the video has an audio stream (`ffmpeg -i uploads/vdo1.mp4`)
   * Windows paths should be converted to POSIX using `Path(video_path).as_posix()`

2. **Python module errors**

   Ensure all packages are installed in your virtual environment:

```bash
pip install moviepy python-multipart whisper fastapi uvicorn
```

3. **Output directory issues**

   `outputs/` must exist and be writable.

---

## Development Tips

* Use **try/except around transcription** to catch errors gracefully.
* All edits are returned as a **list of segments**, which can be modified before rendering.
* Chat commands in `chat.py` can be extended for more complex instructions.

```
