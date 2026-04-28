from flask import Flask, request, render_template, Response, redirect
from extractor import extract_video
from utils import generate_token, verify_token
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return "✅ Server Running"


# 🔗 GENERATE DOWNLOAD PAGE
@app.route("/generate")
def generate():
    url = request.args.get("url")

    if not url:
        return "❌ No URL provided"

    try:
        data = extract_video(url)
    except Exception as e:
        print("Extract Error:", e)
        return "❌ استخراج failed"

    formats = data.get("formats", [])

    if not formats:
        return "❌ No downloadable formats found"

    first = formats[0]

    token = generate_token(first["url"])

    return render_template(
        "download.html",
        title=data.get("title", "Download"),
        token=token
    )


# 📥 DOWNLOAD ROUTE
@app.route("/download")
def download():
    token = request.args.get("token")

    if not token:
        return "❌ Invalid request"

    video_url = verify_token(token)

    if not video_url:
        return "⏳ Link expired"

    try:
        r = requests.get(video_url, stream=True, timeout=15)

        def generate():
            for chunk in r.iter_content(chunk_size=1024 * 512):
                if chunk:
                    yield chunk

        return Response(
            generate(),
            headers={
                "Content-Disposition": "attachment; filename=video.mp4"
            },
            content_type=r.headers.get("content-type", "application/octet-stream")
        )

    except Exception as e:
        print("Download Error:", e)
        return redirect(video_url)


if __name__ == "__main__":
    print("🌐 Flask server running...")
    app.run(host="0.0.0.0", port=5000, debug=False)
