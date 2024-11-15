from ..models import Vehicle
from ..enums import Color
from ..database import db


def get_available_colors():
    # Fetch unique colors from the Vehicle table
    unique_colors = db.session.query(Vehicle.color).distinct().all()
    unique_colors = [color[0] for color in unique_colors if color[0]]  # Flatten list of tuples

    # If no colors are found, fall back to enum
    if not unique_colors:
        unique_colors = [color.value for color in Color]

    return unique_colors
