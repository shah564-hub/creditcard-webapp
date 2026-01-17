from datetime import datetime


def now_ts():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def clean_card_number(card_number: str) -> str:
    return "".join([c for c in str(card_number) if c.isdigit()])


def luhn_check(card_number: str) -> bool:
    """Validate card number using Luhn Algorithm"""
    digits = [int(d) for d in card_number if d.isdigit()]
    if len(digits) < 12:
        return False

    checksum = 0
    reverse_digits = digits[::-1]

    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d

    return checksum % 10 == 0
