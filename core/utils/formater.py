from decimal import Decimal


def format_price(amount: Decimal, currency: str = "₽") -> str:
    if currency == "₽":
        return f"{amount:.0f} {currency}"
    return f"{amount:.2f} {currency}"