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
    res = requests.get(api).json()

    return {
        "title": res.get("filename", "TeraBox File"),
        "formats": [
            {"quality": "Default", "url": res.get("download"), "size": 0}
        ]
    }


# 🔥 DiskWala bypass
def extract_diskwala(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text

        patterns = [
            r'href="(https?://[^"]+\.mp4[^"]*)"',
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
    except:
        pass

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
        'format': 'bestvideo+bestaudio/best',
        'geo_bypass': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get("formats", []):
            if f.get("url") and f.get("height"):
                formats.append({
                    "quality": f"{f['height']}p",
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

    except:
        return {
            "title": "Fallback",
            "formats": [
                {"quality": "Open Link", "url": url, "size": 0}
            ]
        }
