import yt_dlp
import requests
import re


def is_terabox(url):
    return "terabox" in url


def is_diskwala(url):
    return "diskwala" in url


# 🔥 TeraBox
def extract_terabox(url):
    api = f"https://terabox-downloader-api.vercel.app/api?url={url}"

    try:
        res = requests.get(api, timeout=10).json()
        link = res.get("download")

        if not link:
            raise Exception("No link")

        return {
            "title": res.get("filename", "TeraBox File"),
            "formats": [
                {"quality": "Default", "url": link, "size": 0}
            ]
        }

    except Exception as e:
        print("TeraBox Error:", e)


# 🔥 DiskWala
def extract_diskwala(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text

        patterns = [
            r'href="(https?://[^"]+)"',
            r'"file":"(https?://[^"]+)"',
            r'"download":"(https?://[^"]+)"'
        ]

        for p in patterns:
            match = re.search(p, html)
            if match:
                link = match.group(1).replace("\\/", "/")

                return {
                    "title": "DiskWala File",
                    "formats": [
                        {"quality": "Direct", "url": link, "size": 0}
                    ]
                }

    except Exception as e:
        print("DiskWala Error:", e)

    return {
        "title": "DiskWala Link",
        "formats": [
            {"quality": "Open Link", "url": url, "size": 0}
        ]
    }


# 🔥 yt-dlp
def extract_ytdlp(url):
    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'geo_bypass': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get("formats", []):
            if f.get("url"):
                formats.append({
                    "quality": str(f.get("height", "Audio")),
                    "url": f["url"],
                    "size": f.get("filesize") or 0
                })

        return {
            "title": info.get("title"),
            "formats": formats[:5]
        }


# 🎯 MAIN
def extract_video(url):
    try:
        if is_diskwala(url):
            return extract_diskwala(url)

        if is_terabox(url):
            return extract_terabox(url)

        return extract_ytdlp(url)

    except Exception as e:
        print("Main Extract Error:", e)

        return {
            "title": "Fallback",
            "formats": [
                {"quality": "Open Link", "url": url, "size": 0}
            ]
        }
