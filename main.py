from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import tempfile
import yt_dlp
import uuid

app = FastAPI(title="Video Downloader MVP")
templates = Jinja2Templates(directory="app/templates")
DOWNLOAD_DIR = Path(tempfile.gettempdir()) / "video_downloader_mvp"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/info")
def info(url: str = Form(...)):
    try:
        opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=False)
        formats = []
        for f in data.get("formats", []):
            if f.get("vcodec") != "none":
                formats.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "height": f.get("height"),
                    "fps": f.get("fps"),
                    "filesize": f.get("filesize") or f.get("filesize_approx"),
                    "has_audio": f.get("acodec") != "none"
                })
        return {"title": data.get("title"), "thumbnail": data.get("thumbnail"),
                "duration": data.get("duration"), "formats": formats[-30:]}
    except Exception as e:
        return JSONResponse({"error": "URL tidak dapat diproses oleh server.", "detail": str(e)}, status_code=400)

@app.post("/api/download")
def download(url: str = Form(...), format_id: str = Form("best")):
    job = uuid.uuid4().hex
    out = DOWNLOAD_DIR / f"{job}.%(ext)s"
    opts = {
        "quiet": True,
        "no_warnings": True,
        "format": format_id,
        "outtmpl": str(out),
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = Path(ydl.prepare_filename(info))
        return FileResponse(filename, filename=filename.name, media_type="application/octet-stream")
    except Exception as e:
        return JSONResponse({"error": "Download gagal atau sumber tidak mendukung pengunduhan.", "detail": str(e)}, status_code=400)
