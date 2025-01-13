from ..database import db
from ..models import Company, Address, Branch, Staff


def get_first_company():
    company = Company.query.first()
    return company


def create_company(data):
    # Create or get the address instance
    address = Address(
        street_address=data.get('street_address'),
        city=data['city'],
        state=data.get('state'),
        postal_code=data.get('postal_code')
    )
    db.session.add(address)
    db.session.flush()  # Ensure address ID is available

    new_company = Company(
        name=data['name'],
        phone=data.get('phone'),
        fax=data.get('fax'),
        email=data.get('email'),
        website=data.get('website'),
        address=address  # Assign the Address instance
    )
    db.session.add(new_company)
    db.session.commit()
    return new_company


def update_company_service(company, data):
    company.name = data['name']
    company.phone = data.get('phone')
    company.fax = data.get('fax')
    company.email = data.get('email')
    company.website = data.get('website')

    # Update or create the address
    if company.address:
        company.address.street_address = data.get('street_address')
        company.address.city = data['city']
        company.address.state = data.get('state')
        company.address.postal_code = data.get('postal_code')
    else:
        address = Address(
            street_address=data.get('street_address'),
            city=data['city'],
            state=data.get('state'),
            postal_code=data.get('postal_code')
        )
        db.session.add(address)
        company.address = address

    # Update associated branches and their staff
    for branch in company.branches:
        for staff in branch.staff_members:
            # Update staff details if needed
            staff.first_name = data.get('contact_name', staff.first_name)
            staff.phone_number = data.get('contact_phone', staff.phone_number)

    db.session.commit()
    return company


def delete_company(company):
    db.session.delete(company)
    db.session.commit()


def create_default_company():
    first_company = get_first_company()
    if first_company:
        return first_company

    # Create a default address
    default_address = Address(
        street_address="X sokağı Y Mah. Buca İzmir",
        city="İzmir",
        state="",
        postal_code=""
    )
    db.session.add(default_address)
    db.session.flush()  # Ensure address ID is available

    default_company = Company(
        name="Firma Adı",
        phone="000-000-0000",
        fax="000-000-0000",
        email="deneme@company.com",
        website="https://www.defaultcompany.com",
        address=default_address  # Assign the Address instance
    )
    db.session.add(default_company)
    db.session.flush()  # Ensure company ID is available

    # Create a default branch
    default_branch = Branch(
        name="Bayi",
        company_id=default_company.id,
        address_id=default_address.id
    )
    db.session.add(default_branch)
    db.session.flush()  # Ensure branch ID is available

    # Create a default staff member
    default_staff = Staff(
        first_name="Yetkili",
        last_name="Kişi",
        password="defaultpassword",  # Ensure to hash passwords in a real application
        phone_number="000-000-0000",
        department="Default Department",
        role="Manager",
        branch_id=default_branch.id
    )
    db.session.add(default_staff)

    db.session.commit()
    return default_company


