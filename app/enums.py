from enum import Enum


class TransmissionType(Enum):
    MANUAL = "Düz vites"
    AUTOMATIC = "Otomatik"
    SEMI_AUTOMATIC = "Yarı otomatik"


class FuelType(Enum):
    GASOLINE = "Benzin"
    LPG = "Benzin + LPG"
    DIESEL = "Dizel"
    ELECTRIC = "Elektrikli"
    HYBRID = "Hibrit"


class Color(Enum):
    BEIGE = "Bej"
    WHITE = "Beyaz"
    BURGUNDY = "Bordo"
    SMOKE = "Füme"
    GRAY = "Gri"
    SILVER_GRAY = "Gümüş Gri"
    BROWN = "Kahverengi"
    RED = "Kırmızı"
    NAVY_BLUE = "Lacivert"
    BLUE = "Mavi"
    PURPLE = "Mor"
    PINK = "Pembe"
    YELLOW = "Sarı"
    BLACK = "Siyah"
    CHAMPAGNE = "Şampanya"
    TURQUOISE = "Turkuaz"
    ORANGE = "Turuncu"
    GREEN = "Yeşil"


class ReportStatus(Enum):
    OPENED = "Açılmış"
    COMPLETED = "Tamamlanmış"
    CANCELLED = "İptal edilmiş"


class ExpertiseTypeEnum(Enum):
    BOYA = "Boya Ekspertiz"
    KAPORTA = "Kaporta Ekspertiz"
    MOTOR = "Motor Ekspertiz"
    YANAL_KAYMA = "Yanal Kayma Ekspertiz"
    SUSPANSIYON = "Süspansiyon Ekspertiz"
    FRENI = "Fren Ekspertiz"
    YOL = "Yol Ekspertiz"
    DYNO = "Dyno Ekspertiz"
    BEYIN = "Beyin Ekspertiz"
    IC = "İç Ekspertiz"
    DIS = "Dış Ekspertiz"
    MEKANIK = "Mekanik Ekspertiz"


class ExpertiseAnswer:
    class IntStatus(Enum):
        ZERO = 0

    class ExpertiseStatus(Enum):
        NO_ISSUE = "YOK"
        PASSED = "Kontrolden Geçti"
        MAY_CAUSE_ISSUES = "Sorun Çıkarabilir"
        NEEDS_MAINTENANCE = "Bakım Gerekli"

    class PaintStatus(Enum):
        ORIGINAL = "ORİJİNAL"
        PLASTIC = "PLASTİK"
        PAINTED = "BOYALI"
        LOCALLY_PAINTED = "LOKAL BOYALI"
        REPLACED = "DEĞİŞMİŞ"
        COATED = "KAPLAMA"
        NONE = "YOK"

    class ExtraConditions(Enum):
        REMOVED_REPLACED = "SÖKÜLMÜŞ / TAKILMIŞ"
        DENTLESS = "BOYASIZ GÖÇÜK"
        DENTED_SCRATCHED = "EZİK-ÇİZİK"
        VARNISH = "VERNİK"

    class BodyworkStatus(Enum):
        NO_ISSUE = "SORUNSUZ"
        SCRATCHED = "ÇİZİK"
        DENTED = "EZİK / KIRIK / GÖÇÜK"
        PAINTED = "İŞLEMLİ / BOYALI"

    class OBDStatus(Enum):
        NO_ERROR = "ARIZA KAYDI YOK"
        ERROR_LOGGED = "HATA KAYDI VAR"
        NO_CONNECTION = "BAĞLANTI KURULAMADI"

