import base64, time
from config import LINK_EXPIRY


def generate_token(url):
    data = f"{url}|{int(time.time())}"
    return base64.urlsafe_b64encode(data.encode()).decode()


def verify_token(token):
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        url, ts = decoded.split("|")

        if time.time() - int(ts) > LINK_EXPIRY:
            return None

        return url
    except:
        return None
