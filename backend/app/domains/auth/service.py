"""Authentication and token services."""
from __future__ import annotations

import datetime
import hashlib
import hmac
import os
import uuid
from typing import Any

from app.config import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    """Hash password using salt + pbkdf2_hmac sha256 (standard library)."""
    salt = os.urandom(16).hex()
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"pbkdf2:sha256:100000${salt}${dk.hex()}"


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify password against hashed string."""
    try:
        parts = hashed.split("$")
        if len(parts) != 3:
            return False
        _, salt, expected_hex = parts
        dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100_000)
        return hmac.compare_digest(dk.hex(), expected_hex)
    except Exception:
        return False


def create_access_token(user_id: uuid.UUID, email: str, role: str, expires_delta: datetime.timedelta | None = None) -> str:
    """Create a self-contained JWT-like token (using standard library HMAC-SHA256 for maximum reliability)."""
    import base64
    import json

    now = datetime.datetime.now(datetime.timezone.utc)
    exp = now + (expires_delta or datetime.timedelta(hours=24))

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    def b64_encode(d: dict[str, Any]) -> str:
        s = json.dumps(d, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(s).decode("utf-8").rstrip("=")

    h_b64 = b64_encode(header)
    p_b64 = b64_encode(payload)
    sig_data = f"{h_b64}.{p_b64}".encode("utf-8")
    sig = hmac.new(settings.secret_key.encode("utf-8"), sig_data, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")

    return f"{h_b64}.{p_b64}.{sig_b64}"


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode and verify HMAC-SHA256 token."""
    import base64
    import json

    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        h_b64, p_b64, sig_b64 = parts

        sig_data = f"{h_b64}.{p_b64}".encode("utf-8")
        expected_sig = hmac.new(settings.secret_key.encode("utf-8"), sig_data, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "==")
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = base64.urlsafe_b64decode(p_b64 + "==")
        payload = json.loads(payload_bytes.decode("utf-8"))

        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        if payload.get("exp", 0) < now:
            return None  # Expired

        return payload
    except Exception:
        return None
