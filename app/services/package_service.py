from app.models import Package


def get_expertises(package: Package):
    return [pe.expertise_type for pe in package.package_expertises]
