from ..enums import TransmissionType, FuelType, Color

COLOR_MAPPING = {
    'BEJ': Color.BEIGE,
    'BEYAZ': Color.WHITE,
    'BORDO': Color.BURGUNDY,
    'FÜME': Color.SMOKE,
    'GRİ': Color.GRAY,
    'GÜMÜŞ GRİ': Color.SILVER_GRAY,
    'KAHVERENGİ': Color.BROWN,
    'KIRMIZI': Color.RED,
    'LACİVERT': Color.NAVY_BLUE,
    'MAVİ': Color.BLUE,
    'MOR': Color.PURPLE,
    'PEMBE': Color.PINK,
    'SARI': Color.YELLOW,
    'SİYAH': Color.BLACK,
    'ŞAMPANYA': Color.CHAMPAGNE,
    'TURKUAZ': Color.TURQUOISE,
    'TURUNCU': Color.ORANGE,
    'YEŞİL': Color.GREEN,
}

TRANSMISSION_TYPE_MAPPING = {
    'DÜZ VİTES': TransmissionType.MANUAL,
    'OTOMATİK': TransmissionType.AUTOMATIC,
    'YARI OTOMATİK': TransmissionType.SEMI_AUTOMATIC,
}

FUEL_TYPE_MAPPING = {
    'BENZİN': FuelType.GASOLINE,
    'BENZİN + LPG': FuelType.LPG,
    'DİZEL': FuelType.DIESEL,
    'ELEKTRİKLİ': FuelType.ELECTRIC,
    'HİBRİT': FuelType.HYBRID,
}


def map_to_enum(input_value: str, mapping: dict):
    """
    Map the input value to the corresponding Enum using the provided mapping.
    """
    mapped_value = mapping.get(input_value.upper())
    if not mapped_value:
        raise ValueError(f"Invalid value: {input_value}. Expected one of {list(mapping.keys())}.")
    return mapped_value
