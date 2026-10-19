import os
import time
import subprocess
import nest_asyncio
from fastapi import FastAPI, UploadFile, File, Form, Request, Response, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
import uvicorn
import threading

nest_asyncio.apply()

app = FastAPI()
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔑 আপনার কাস্টমারদের জন্য নির্ধারিত সিকিউরিটি কোড (এটি আপনি যেকোনো সময় পরিবর্তন করতে পারবেন)
ACCESS_CODE = "ULTRA2026"

# ১. লগইন বা পাসওয়ার্ড দেওয়ার ইন্টারফেস
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Ultra Method - Security Verification</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #050b14; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: linear-gradient(145deg, #111827, #0f172a); border: 1px solid #334155; padding: 30px; border-radius: 22px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.8); }
        h2 { color: #38bdf8; margin-bottom: 10px; }
        p { font-size: 13px; color: #94a3b8; margin-bottom: 20px; }
        input[type="password"] { width: 100%; padding: 13px; background: #1e293b; border: 1px solid #475569; border-radius: 12px; color: #fff; font-size: 15px; box-sizing: border-box; outline: none; text-align: center; margin-bottom: 15px; }
        button { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; padding: 14px; border-radius: 12px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; transition: 0.3s; }
        button:hover { background: linear-gradient(135deg, #0369a1, #1d4ed8); }
        .error { color: #f43f5e; font-size: 12px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔒 সিকিউরিটি ভেরিফিকেশন</h2>
        <p>সফটওয়্যারটি ব্যবহার করতে আপনার প্রিমিয়াম সিকিউরিটি কোডটি দিন:</p>
        <form action="/verify" method="post">
            <input type="password" name="code" placeholder="সিকিউরিটি কোড লিখুন" required>
            <button type="submit">প্রবেশ করুন</button>
        </form>
        <div class="error"></div>
    </div>
</body>
</html>
"""

# ২. মূল ভিডিও প্রসেসিং ইন্টারফেস
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Ultra Method Studio</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #050b14; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: linear-gradient(145deg, #111827, #0f172a); border: 1px solid #334155; padding: 30px; border-radius: 22px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.8); }
        .top-title { font-size: 11px; font-weight: bold; color: #38bdf8; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }
        .sub-title { font-size: 10px; color: #94a3b8; margin-bottom: 18px; line-height: 1.4; font-style: italic; }
        .main-heading { color: #f8fafc; font-size: 24px; margin: 10px 0 5px 0; font-weight: 800; text-shadow: 0 2px 10px rgba(56,189,248,0.3); }
        .sub-heading { font-size: 13px; color: #38bdf8; margin-bottom: 22px; font-weight: 600; }
        .input-group { text-align: left; margin-bottom: 16px; }
        label { display: block; font-size: 13px; color: #cbd5e1; margin-bottom: 6px; font-weight: 600; }
        input[type="file"], select { width: 100%; padding: 13px; background: #1e293b; border: 1px solid #475569; border-radius: 12px; color: #fff; font-size: 14px; box-sizing: border-box; outline: none; transition: 0.3s; }
        input[type="file"]:focus, select:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.2); }
        button { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; padding: 15px; border-radius: 12px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5); transition: 0.3s; }
        button:hover { background: linear-gradient(135deg, #0369a1, #1d4ed8); }
        .loader { display: none; margin-top: 18px; color: #38bdf8; font-weight: bold; font-size: 13px; line-height: 1.5; }
        .footer-warning { margin-top: 25px; font-size: 12px; color: #f43f5e; font-weight: bold; border-top: 1px solid #334155; padding-top: 15px; background: rgba(244, 63, 94, 0.08); border-radius: 0 0 12px 12px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="card">
        <div class="top-title">TikTok Instagram Facebook High Quality Videos Generator</div>
        <div class="sub-title">TikTok High Quality Method Dolby Vision 4K 60fps Dolby Vision HDR Ultra High Quality Method</div>
        
        <div class="main-heading">✨ এআই আল্ট্রা মেথড</div>
        <div class="sub-heading">প্রিমিয়াম মেথড (ডলবি ভিশন ও তেলতেলে এইচডি)</div>
        
        <form action="/process" method="post" enctype="multipart/form-data" onsubmit="showLoader()">
            <div class="input-group">
                <label>ভিডিও সিলেক্ট করুন:</label>
                <input type="file" name="video" accept="video/*" required>
            </div>
            
            <div class="input-group">
                <label>রেজোলিউশন সিলেক্ট করুন:</label>
                <select name="quality">
                    <option value="4k">4K Ultra Glossy (60 FPS)</option>
                    <option value="3k">3K Ultra Glossy (60 FPS)</option>
                    <option value="1080p" selected>HD 1080p Glossy (60 FPS - TikTok Master)</option>
                    <option value="720p">720p Fast Smooth (60 FPS)</option>
                </select>
            </div>
            
            <button type="submit">🚀 Process & Download Master Video</button>
        </form>
        <div class="loader" id="loader">⏳ ভিডিওর কাঁপনি রোধ, ডলবি ভিশন ও এইচডি রেন্ডারিং হচ্ছে... দয়া করে অপেক্ষা করুন!</div>
        
        <div class="footer-warning">
            ⚠️ এটি একটি আমানত। দয়া করে আমানতের খিয়ানত করবেন না এবং এটি পেইড হওয়ায় কারও সাথে শেয়ার করবেন না।
        </div>
    </div>
    <script>function showLoader() { document.getElementById('loader').style.display = 'block'; }</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # প্রথমে ইউজারকে সিকিউরিটি কোডের পেজ দেখাবে
    return LOGIN_TEMPLATE

@app.post("/verify")
async def verify_code(code: str = Form(...)):
    if code == ACCESS_CODE:
        # কোড সঠিক হলে কুকি সেট করে মূল পেজে রিডাইরেক্ট করবে
        response = RedirectResponse(url="/studio", status_code=303)
        response.set_cookie(key="auth", value="true")
        return response
    else:
        return HTMLResponse("<h3>ভুল সিকিউরিটি কোড! দয়া করে সঠিক কোড দিন।</h3><a href='/'>ফিরে যান</a>", status_code=400)

@app.get("/studio", response_class=HTMLResponse)
async def studio(request: Request):
    # কুকি চেক করে পাসওয়ার্ড ভেরিফাই করা আছে কি না দেখবে
    if request.cookies.get("auth") == "true":
        return HTML_TEMPLATE
    return RedirectResponse(url="/", status_code=303)

@app.post("/process")
async def process_video(request: Request, video: UploadFile = File(...), quality: str = Form(...)):
    if request.cookies.get("auth") != "true":
        raise HTTPException(status_code=403, unauthorized="Access Denied")

    input_path = os.path.join(UPLOAD_FOLDER, video.filename)
    with open(input_path, "wb") as buffer:
        buffer.write(await video.read())

    output_filename = f"AI_Ultra_Method_{quality}_{int(time.time())}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    if quality == '4k':
        scale_filter = "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840"
        crf, maxrate, bufsize = "11", "40M", "60M"
    elif quality == '3k':
        scale_filter = "scale=1620:2880:force_original_aspect_ratio=increase,crop=1620:2880"
        crf, maxrate, bufsize = "12", "30M", "45M"
    elif quality == '1080p':
        scale_filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        crf, maxrate, bufsize = "13", "25M", "35M"
    else:
        scale_filter = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
        crf, maxrate, bufsize = "15", "12M", "18M"

    filter_chain = (
        f"deshake,"
        f"{scale_filter},"
        f"eq=contrast=1.30:brightness=0.012:saturation=1.35:gamma=0.88,"
        f"hqdn3d=2.0:2.0:4.0:4.0,"
        f"unsharp=luma_msize_x=9:luma_msize_y=9:luma_amount=2.4:chroma_msize_x=7:chroma_msize_y=7:chroma_amount=1.3,"
        f"format=yuv420p"
    )

    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', filter_chain,
        '-c:v', 'libx264', '-preset', 'slow', '-crf', crf,
        '-maxrate', maxrate, '-bufsize', bufsize,
        '-profile:v', 'high', '-level', '5.1',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-r', '60', '-c:a', 'aac', '-b:a', '320k',
        output_path
    ]

    subprocess.run(ffmpeg_cmd)
    return FileResponse(output_path, media_type="video/mp4", filename=output_filename)

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=5000)

threading.Thread(target=run_server, daemon=True).start()

print("generating public link...")
import subprocess as sp
tunnel = sp.Popen(["lt", "--port", "5000"], stdout=sp.PIPE, stderr=sp.PIPE, text=True)

for line in tunnel.stdout:
    print("Your Public Website Link:", line.strip())
    break
