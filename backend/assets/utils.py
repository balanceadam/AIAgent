from decimal import Decimal


def format_wei(value, decimals=18):
    """
    Convert Wei to a human-readable format.
    """
    return Decimal(value) / Decimal(10**decimals)
