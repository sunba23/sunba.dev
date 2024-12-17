import hmac
import hashlib
from typing import Optional

def verify_signature(payload_body: bytes, secret_token: str, signature_header: Optional[str]) -> bool:
    if not signature_header:
        return False
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)
