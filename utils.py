import base64
import time
import hmac
import hashlib
from config import LINK_EXPIRY, SECRET_KEY


def generate_token(url):
    ts = str(int(time.time()))
    data = f"{url}|{ts}"

    signature = hmac.new(
        SECRET_KEY.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

    token = f"{data}|{signature}"

    return base64.urlsafe_b64encode(token.encode()).decode()


def verify_token(token):
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        url, ts, sig = decoded.split("|")

        # verify expiry
        if time.time() - int(ts) > LINK_EXPIRY:
            return None

        # verify signature
        data = f"{url}|{ts}"
        expected_sig = hmac.new(
            SECRET_KEY.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(sig, expected_sig):
            return None

        return url

    except Exception as e:
        print("Token Error:", e)
        return None
