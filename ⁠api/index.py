import os
import time
import subprocess
from fastapi import FastAPI, UploadFile, File, Form, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

app = FastAPI()
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔑 সিকিউরিটি কোড এবং আপনার হোয়াটসঅ্যাপ নম্বর
ACCESS_CODE = "ULTRA2026"
WHATSAPP_NUMBER = "8801619674023"

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
        .main-heading { color: #f8fafc; font-size: 24px; margin: 10px 0 5px 0; font-weight: 800; }
        .sub-heading { font-size: 13px; color: #38bdf8; margin-bottom: 22px; font-weight: 600; }
        .input-group { text-align: left; margin-bottom: 16px; }
        label { display: block; font-size: 13px; color: #cbd5e1; margin-bottom: 6px; font-weight: 600; }
        input[type="file"], select, input[type="password"] { width: 100%; padding: 13px; background: #1e293b; border: 1px solid #475569; border-radius: 12px; color: #fff; font-size: 14px; box-sizing: border-box; outline: none; }
        button { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; padding: 15px; border-radius: 12px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; margin-top: 10px; }
        .loader { display: none; margin-top: 18px; color: #38bdf8; font-weight: bold; font-size: 13px; }
        .free-badge { background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; color: #38bdf8; padding: 8px 12px; border-radius: 10px; font-size: 13px; margin-bottom: 15px; display: inline-block; font-weight: bold; }
        .whatsapp-box { margin-top: 20px; font-size: 13px; color: #94a3b8; border-top: 1px solid #334155; padding-top: 15px; }
        .whatsapp-btn { display: inline-block; background: #25d366; color: white; padding: 10px 15px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 8px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="top-title">AI Ultra Method Studio</div>
        <div class="main-heading">✨ এআই আল্ট্রা মেথড</div>
        <div class="sub-heading">ডলবি ভিশন ও এইচডি ভিডিও প্রসেসিং</div>
        
        <div class="free-badge">free_status</div>

        <form action="/api" method="post" enctype="multipart/form-data" onsubmit="showLoader()">
            <div class="input-group">
                <label>ভিডিও সিলেক্ট করুন:</label>
                <input type="file" name="video" accept="video/*" required>
            </div>
            
            <div class="input-group">
                <label>রেজোলিউশন সিলেক্ট করুন:</label>
                <select name="quality">
                    <option value="4k">4K Ultra Glossy (60 FPS)</option>
                    <option value="1080p" selected>HD 1080p Glossy (60 FPS)</option>
                    <option value="720p">720p Fast Smooth (60 FPS)</option>
                </select>
            </div>
            
            button_area
        </form>
        <div class="loader" id="loader">⏳ ভিডিও প্রসেসিং হচ্ছে... দয়া করে অপেক্ষা করুন!</div>

        <div class="whatsapp-box">
            আনলিমিটেড ব্যবহারের জন্য সিকিউরিটি কোড নিতে যোগাযোগ করুন:
            <br>
            <a href="https://wa.me/whatsapp_num?text=I%20want%20AI%20Ultra%20Method%20Security%20Code" class="whatsapp-btn" target="_blank">💬 WhatsApp এ মেসেজ দিন</a>
        </div>
    </div>
    <script>function showLoader() { document.getElementById('loader').style.display = 'block'; }</script>
</body>
</html>
"""

@app.get("/api", response_class=HTMLResponse)
async def index(request: Request):
    free_count = int(request.cookies.get("free_count", "0"))
    is_auth = request.cookies.get("auth") == "true"

    html = HTML_TEMPLATE.replace("whatsapp_num", WHATSAPP_NUMBER)

    if not is_auth and free_count < 2:
        rem = 2 - free_count
        html = html.replace("free_status", f"🎁 আপনি দুটি ভিডিও ফ্রিতে বানাতে পারবেন (বাকি আছে: {rem}টি)")
        html = html.replace("button_area", '<button type="submit">🚀 ফ্রি প্রসেস করুন</button>')
    elif is_auth:
        html = html.replace("free_status", "👑 প্রিমিয়াম এক্সেস সক্রিয় রয়েছে")
        html = html.replace("button_area", '<button type="submit">🚀 প্রসেস ও ডাউনলোড করুন</button>')
    else:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html lang="bn">
        <head><meta charset="UTF-8"><title>Package Update</title>
        <style>body{{font-family:sans-serif;background:#050b14;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}
        .box{{background:#111827;padding:30px;border-radius:18px;text-align:center;border:1px solid #334155;max-width:380px;width:90%;box-shadow:0 20px 40px rgba(0,0,0,0.8);}}
        input{{width:100%;padding:12px;margin:12px 0;background:#1e293b;border:1px solid #475569;border-radius:8px;color:#fff;box-sizing:border-box;text-align:center;font-size:16px;}}
        button{{background:#0284c7;color:#fff;border:none;padding:12px;width:100%;border-radius:8px;font-weight:bold;cursor:pointer;}}
        .wa-btn{{display:inline-block;background:#25d366;color:#fff;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold;margin-top:15px;width:100%;box-sizing:border-box;font-size:14px;}}
        .msg{{color:#f43f5e;font-size:14px;font-weight:bold;margin-bottom:15px;line-height:1.5;}}
        </style></head>
        <body>
        <div class="box">
            <div class="msg">⚠️ আপনার দুটি ভিডিও সম্পূর্ণ তৈরি হয়ে গেছে! আপনার প্যাকেজটি আপডেট করুন।</div>
            <p style="font-size:13px;color:#94a3b8;margin-bottom:15px;">আনলিমিটেড ভিডিও বানাতে সিকিউরিটি কোড দিন অথবা হোয়াটসঅ্যাপে যোগাযোগ করুন:</p>
            <form action="/api/verify" method="post">
                <input type="password" name="code" placeholder="সিকিউরিটি কোড লিখুন" required>
                <button type="submit">প্রবেশ করুন</button>
            </form>
            <a href="https://wa.me/{WHATSAPP_NUMBER}?text=I%20want%20AI%20Ultra%20Method%20Security%20Code" class="wa-btn" target="_blank">💬 হোয়াটসঅ্যাপে যোগাযোগ করুন</a>
        </div></body></html>
        """)
    return HTMLResponse(html)

@app.post("/api/verify")
async def verify_code(code: str = Form(...)):
    if code == ACCESS_CODE:
        res = RedirectResponse(url="/api", status_code=303)
        res.set_cookie(key="auth", value="true")
        return res
    return HTMLResponse("<h3>ভুল সিকিউরিটি কোড!</h3><a href='/api'>ফিরে যান</a>", status_code=400)

@app.post("/api", response_class=FileResponse)
async def process_video(request: Request, response: Response, video: UploadFile = File(...), quality: str = Form(...)):
    free_count = int(request.cookies.get("free_count", "0"))
    is_auth = request.cookies.get("auth") == "true"

    if not is_auth:
        if free_count < 2:
            response.set_cookie(key="free_count", value=str(free_count + 1))
        else:
            return RedirectResponse(url="/api", status_code=303)

    input_path = os.path.join(UPLOAD_FOLDER, video.filename)
    with open(input_path, "wb") as buffer:
        buffer.write(await video.read())

    output_filename = f"AI_Ultra_{quality}_{int(time.time())}.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    scale = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if quality == '4k':
        scale = "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840"

    filter_chain = f"deshake,{scale},eq=contrast=1.3:saturation=1.35,format=yuv420p"
    
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', filter_chain,
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', output_path
    ]
    subprocess.run(cmd)
    return FileResponse(output_path, media_type="video/mp4", filename=output_filename)
