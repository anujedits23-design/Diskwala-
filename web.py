from flask import Flask, request, render_template, Response, redirect
from extractor import extract_video
from utils import generate_token, verify_token
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return "✅ Running"


@app.route("/generate")
def generate():
    url = request.args.get("url")

    data = extract_video(url)
    first = data["formats"][0]

    token = generate_token(first["url"])

    return render_template(
        "download.html",
        title=data["title"],
        token=token
    )


@app.route("/download")
def download():
    token = request.args.get("token")

    video_url = verify_token(token)

    if not video_url:
        return "Expired"

    try:
        r = requests.get(video_url, stream=True)

        return Response(
            r.iter_content(chunk_size=1024),
            headers={"Content-Disposition": "attachment; filename=video.mp4"},
            content_type=r.headers.get("content-type")
        )
    except:
        return redirect(video_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
