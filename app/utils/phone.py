import phonenumbers as pn
from fastapi import HTTPException


def normalize_phone(raw: str, country: str) -> tuple[str, str]:
    try:
        num = pn.parse(raw, country)
        if not pn.is_valid_number(num):
            raise ValueError("invalid phone")
        e164 = pn.format_number(num, pn.PhoneNumberFormat.E164)
        last4 = str(num.national_number)[-4:].rjust(4, "0")
        return e164, last4
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid phone: {e}")