import json
from ..models import (Report, Customer, VehicleOwner, Vehicle, Agent,
                      Staff, PackageExpertise,  ExpertiseReport, ExpertiseType, ExpertiseFeature)
from ..database import db
from datetime import datetime


def load_expertise_map(file_path='data/expertise_map.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            expertise_map = json.load(file)
        return expertise_map
    except FileNotFoundError:
        print(f"JSON file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}


def get_default_features_for_expertise_type(expertise_name, expertise_map=None):
    if expertise_map is None:
        expertise_map = load_expertise_map()

    return expertise_map.get(expertise_name, [])


def create_report(inspection_date, vehicle_id, customer_id, package_id, operation, created_by, registration_document_seen):
    report = Report(
        inspection_date=inspection_date,
        vehicle_id=vehicle_id,
        customer_id=customer_id,
        package_id=package_id,
        operation=operation,
        created_by=created_by,
        registration_document_seen=registration_document_seen
    )
    db.session.add(report)
    db.session.commit()

    package_expertises = PackageExpertise.query.filter_by(package_id=package_id).all()
    if not package_expertises:
        print(f"No expertise types found for package ID {package_id}.")
        return

    for package_expertise in package_expertises:
        expertise_report = ExpertiseReport(
            expertise_type_id=package_expertise.expertise_type_id,
            comment=""
        )
        db.session.add(expertise_report)
        db.session.commit()

        expertise_type = ExpertiseType.query.get(package_expertise.expertise_type_id)
        default_features = get_default_features_for_expertise_type(expertise_type.name)
        for feature_name, status in default_features:
            feature = ExpertiseFeature(
                name=feature_name,
                status=status,
                expertise_report_id=expertise_report.id
            )
            db.session.add(feature)

        db.session.commit()

    print(f"Report for vehicle '{vehicle_id}' created successfully with associated expertise reports.")
    return report


def get_or_create_customer(form_data):
    customer = Customer.query.filter_by(
        full_name=form_data.get('customer_name'),
        phone_number=form_data.get('customer_phone'),
        tc_tax_number=form_data.get('customer_tax_no'),
        email=form_data.get('customer_email'),
        address=form_data.get('customer_address')
    ).first()

    if not customer:
        customer = Customer(
            full_name=form_data.get('customer_name') or None,
            phone_number=form_data.get('customer_phone') or None,
            tc_tax_number=form_data.get('customer_tax_no') or None,
            email=form_data.get('customer_email') or None,
            address=form_data.get('customer_address') or None
        )
        db.session.add(customer)
        db.session.commit()

    return customer


def get_or_create_vehicle_owner(form_data):
    vehicle_owner = VehicleOwner.query.filter_by(
        full_name=form_data['owner_name'],
        tc_tax_number=form_data['owner_tax_no'],
        phone_number=form_data['owner_phone'],
        address=form_data['owner_address']
    ).first()

    if not vehicle_owner:
        vehicle_owner = VehicleOwner(
            full_name=form_data['owner_name'],
            tc_tax_number=form_data['owner_tax_no'],
            phone_number=form_data['owner_phone'],
            address=form_data['owner_address']
        )
        db.session.add(vehicle_owner)
        db.session.commit()
    return vehicle_owner


def get_or_create_agent(agent_name):
    agent = Agent.query.filter_by(full_name=agent_name).first()

    if not agent:
        agent = Agent(full_name=agent_name)
        db.session.add(agent)
        db.session.commit()
    return agent


def get_or_create_staff_by_name(staff_name):
    staff = Staff.query.filter_by(full_name=staff_name).first()
    if not staff:
        staff = Staff(full_name=staff_name)
        db.session.add(staff)
        db.session.commit()
    return staff


def get_or_create_vehicle(form_data):
    vehicle = Vehicle.query.filter_by(
        plate=form_data['vehicle_plate'],
        chassis_number=form_data['chassis_number']
    ).first()

    if not vehicle:
        vehicle = Vehicle(
            plate=form_data['vehicle_plate'],
            engine_number=form_data['engine_number'],
            brand=form_data['brand'],
            model=form_data['model'],
            chassis_number=form_data['chassis_number'],
            color=form_data['color'],
            model_year=int(form_data['model_year']),
            transmission_type=form_data['gear_type'],
            fuel_type=form_data['fuel_type'],
            mileage=int(form_data['vehicle_km']),
        )
        db.session.add(vehicle)
        db.session.commit()
    return vehicle



