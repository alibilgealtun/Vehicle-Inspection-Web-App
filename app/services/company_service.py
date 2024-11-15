from ..database import db
from ..models import Company


def get_first_company():
    return Company.query.first()


def create_company(data):
    new_company = Company(
        name=data['name'],
        phone_1=data.get('phone_1'),
        phone_2=data.get('phone_2'),
        fax=data.get('fax'),
        email=data.get('email'),
        website=data.get('website'),
        address=data.get('address'),
        my_business_address_link=data.get('my_business_address_link')
    )
    db.session.add(new_company)
    db.session.commit()
    return new_company


def update_company_service(company, data):
    company.name = data['name']
    company.phone_1 = data.get('phone_1')
    company.phone_2 = data.get('phone_2')
    company.fax = data.get('fax')
    company.email = data.get('email')
    company.website = data.get('website')
    company.address = data.get('address')
    company.my_business_address_link = data.get('my_business_address_link')

    db.session.commit()
    return company


def delete_company(company):
    db.session.delete(company)
    db.session.commit()


def create_default_company():
    first_company = get_first_company() # if there is no instance, returns None
    if first_company:
        return first_company
    default_company = Company(
        name="Firma Adı",
        phone_1="000-000-0000",
        phone_2="000-000-0000",
        fax="000-000-0000",
        email="deneme@company.com",
        website="https://www.defaultcompany.com",
        address="X sokağı Y Mah. Buca İzmir",
        my_business_address_link="https://maps.google.com"
    )
    db.session.add(default_company)
    db.session.commit()
    return default_company


