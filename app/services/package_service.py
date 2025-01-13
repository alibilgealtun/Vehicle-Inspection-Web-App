from app.models import Package, PackageExpertise, ExpertiseType
from app.database import db


def get_expertises(package: Package):
    return [pe.expertise_type for pe in package.package_expertises]

def create_default_package():
    # Check if the default package already exists
    if not Package.query.filter_by(name='Default Package').first():
        # Create a new package instance
        default_package = Package(
            name='Default Package',
            price=100.0,  # Set a default price
            active=True
        )

        # Add the package to the session
        db.session.add(default_package)
        db.session.flush()  # Flush to generate the package ID

        # Add default expertises to the package
        default_expertises = ExpertiseType.query.limit(3).all()
        for expertise in default_expertises:
            package_expertise = PackageExpertise(
                package_id=default_package.id,
                expertise_type_id=expertise.id
            )
            db.session.add(package_expertise)

        # Commit all changes to the database
        db.session.commit()

