import os

from flask import render_template, url_for
from unidecode import unidecode
from weasyprint import HTML

from .. import ExpertiseType
from ..models import Report, Company, Vehicle, Customer, Staff, ExpertiseReport


def create_pdf(report_id):
    """
    Main function to create a PDF for a given report_id.

    Responsibilities orchestrated here:
      1. Fetch data from the database.
      2. Process package expertise reports.
      3. Build the output PDF filename.
      4. Render and generate the PDF file.
    """
    # 1. Fetch data from the database
    report, company, vehicle, customer, staff = _fetch_report_data(report_id)

    # 2. Process the package expertise reports (including Boya & Kaporta)
    package_expertise_reports = _process_expertise_reports(report)

    # 3. Gather fixed image paths (logo, motor, fren, etc.) and OBD icons
    images, motor_image_url, fren_image_url, info_image_url, obd_mapping = _gather_image_paths()

    # 4. Build a unique output filename
    filename = _build_output_filename(customer)

    # 5. Render the HTML template and generate PDF
    rendered_html = render_template(
        'report_pdf.html',
        report=report,
        company=company,
        vehicle=vehicle,
        customer=customer,
        staff=staff,
        package_expertise_reports=package_expertise_reports,
        motor_image_url=motor_image_url,
        fren_image_url=fren_image_url,
        images=images,
        obd_mapping=obd_mapping,
        info_image_url=info_image_url,
    )
    HTML(string=rendered_html).write_pdf(filename)

    return filename


def _fetch_report_data(report_id):
    """
    Fetches the main entities needed to generate the report:
      - Report
      - Company
      - Vehicle
      - Customer
      - Staff
    """
    report = Report.query.get(report_id)
    company = Company.query.first()
    vehicle = Vehicle.query.get(report.vehicle_id) if report else None
    customer = Customer.query.get(report.customer_id) if report else None
    staff = Staff.query.get(report.created_by) if report else None
    return report, company, vehicle, customer, staff


def _process_expertise_reports(report):
    """
    Processes the package expertises associated with the given report,
    separating special handling for Boya & Kaporta Ekspertiz.
    """
    if not report or not report.package:
        return []

    package_expertise_reports = []
    boya_features = []
    kaporta_features = []
    boya_comment = ""
    kaporta_comment = ""

    # Loop through package expertises
    for pe in report.package.package_expertises:
        expertise_reports = ExpertiseReport.query.filter_by(
            expertise_type_id=pe.expertise_type_id
        ).all()
        print(f"[DEBUG] Number of expertise reports: {len(expertise_reports)}")
        if expertise_reports:
            print(f"[DEBUG] Expertise report: {expertise_reports[0]}")
        else:
            print("[DEBUG] No expertise reports found.")

        expertise_report = expertise_reports[0] if expertise_reports else None
        if expertise_report:
            # Check if it's "Boya & Kaporta Ekspertiz" to handle specially
            if expertise_report.expertise_type.name == "Boya & Kaporta Ekspertiz":
                # Extract Boya and Kaporta features
                (boya_features,
                 kaporta_features,
                 boya_comment,
                 kaporta_comment) = _extract_boya_kaporta_features(expertise_report)
            else:
                # Normal expertise report
                package_expertise_reports.append(
                    _build_expertise_report_dict(expertise_report)
                )

    # Combine Boya & Kaporta Ekspertiz into a single report block
    if boya_features or kaporta_features:
        package_expertise_reports.append({
            'expertise_type_name': "Boya & Kaporta Ekspertiz",
            'boya_features': boya_features,
            'kaporta_features': kaporta_features,
            'boya_comment': boya_comment,
            'kaporta_comment': kaporta_comment
        })

    return package_expertise_reports


def _extract_boya_kaporta_features(expertise_report):
    """
    Given a "Boya & Kaporta Ekspertiz" report, this helper extracts
    Boya and Kaporta features (and comments) from the child expertise types.
    """
    boya_features = []
    kaporta_features = []
    boya_comment = ""
    kaporta_comment = ""

    child_expertise_types = expertise_report.expertise_type.children

    for child_type in child_expertise_types:
        if child_type.name == "Boya Ekspertiz":
            for rep in child_type.expertise_reports:
                boya_features = [
                    {
                        'name': feature.name,
                        'status': feature.status,
                        'image_path': url_for('static', filename=feature.image_path, _external=True)
                        if feature.image_path else None
                    } for feature in rep.features
                ]
                boya_comment = rep.comment
            for feature in boya_features:
                print(feature, flush=True)

        elif child_type.name == "Kaporta Ekspertiz":
            for rep in child_type.expertise_reports:
                kaporta_features = [
                    {
                        'name': feature.name,
                        'status': feature.status,
                        'image_path': url_for('static', filename=feature.image_path, _external=True)
                        if feature.image_path else None
                    } for feature in rep.features
                ]
                kaporta_comment = rep.comment

    return boya_features, kaporta_features, boya_comment, kaporta_comment


def _build_expertise_report_dict(expertise_report):
    """
    Builds a dictionary of data (features, comments) for a non-Boya/Kaporta expertise report.
    """
    features_with_images = [
        {
            'name': feature.name,
            'status': feature.status,
            'image_path': url_for('static', filename=feature.image_path, _external=True)
            if feature.image_path else None
        } for feature in expertise_report.features
    ]

    return {
        'expertise_type_name': expertise_report.expertise_type.name,
        'comment': expertise_report.comment,
        'features': features_with_images
    }


def _gather_image_paths():
    """
    Returns a tuple of:
      - a list of general images (logo, motor, fren),
      - motor_image_url,
      - fren_image_url,
      - info_image_url,
      - obd_mapping (dict of icons).
    """
    motor_image_url = url_for('static', filename='assets/pdf_imgs/motor_expertise.png', _external=True)
    fren_image_url = url_for('static', filename='assets/pdf_imgs/lastik.png', _external=True)
    info_image_url = url_for('static', filename='assets/pdf_imgs/info.png', _external=True)

    images = [
        {
            'filename': 'logo.jpeg',
            'url': url_for('static', filename='assets/pdf_imgs/logo.jpeg', _external=True),
            'type': 'logo'
        },
        {
            'filename': 'motor_expertise.png',
            'url': url_for('static', filename='assets/pdf_imgs/motor_expertise.png', _external=True),
            'type': 'motor'
        },
        {
            'filename': 'lastik.png',
            'url': url_for('static', filename='assets/pdf_imgs/lastik.png', _external=True),
            'type': 'fren'
        },
    ]

    obd_mapping = {
        'Hava Yastığı Elektroniğinde': url_for('static', filename='assets/pdf_imgs/airbag.png', _external=True),
        'Motor Arıza Lambası': url_for('static', filename='assets/pdf_imgs/engine.png', _external=True),
        'ABS / ESP / ESR Elektroniği': url_for('static', filename='assets/pdf_imgs/abs.png', _external=True),
        'Klima Elektroniği': url_for('static', filename='assets/pdf_imgs/air.png', _external=True),
        'Lastik Basınç Elektroniği': url_for('static', filename='assets/pdf_imgs/tire.png', _external=True),
        'Elektirikli Direksiyon': url_for('static', filename='assets/pdf_imgs/steering.png', _external=True),
        'Motor Beyin Elektroniği': url_for('static', filename='assets/pdf_imgs/brain.png', _external=True),
        'Şanzıman Elektroniği': url_for('static', filename='assets/pdf_imgs/gearbox.png', _external=True)
    }

    return images, motor_image_url, fren_image_url, info_image_url, obd_mapping


def _build_output_filename(customer):
    """
    Creates a unique output filename for the PDF based on the customer's name.
    Ensures files won't overwrite by appending a counter if needed.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, 'pdfs')
    if not os.path.exists(directory):
        os.makedirs(directory)

    sanitized_customer_name = ""
    if customer and customer.full_name:
        sanitized_customer_name = unidecode(
            customer.full_name.replace(" ", "_").replace("/", "_")
        )

    base_filename = os.path.join(directory, f"RAPOR_{sanitized_customer_name}.pdf")
    filename = base_filename
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(directory, f"RAPOR_{sanitized_customer_name}_{counter}.pdf")
        counter += 1

    return filename
