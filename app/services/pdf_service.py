import os

from flask import render_template, url_for
from unidecode import unidecode
from weasyprint import HTML

from .. import ExpertiseType
from ..models import Report, Company, Vehicle, Customer, Staff, PackageExpertise, ExpertiseFeature, ExpertiseReport


def create_pdf(report_id):
    report = Report.query.get(report_id)
    company = Company.query.first()
    vehicle = Vehicle.query.get(report.vehicle_id)

    customer = Customer.query.get(report.customer_id)
    package = report.package
    staff = Staff.query.get(report.created_by)

    package_expertise_reports = []
    boya_features = []
    kaporta_features = []
    boya_comment = ""
    kaporta_comment = ""

    # Loop through all package expertises and find Boya and Kaporta
    for pe in package.package_expertises:
        expertise_reports = ExpertiseReport.query.filter_by(expertise_type_id=pe.expertise_type_id).all()
        print(f"[DEBUG] Number of expertise reports: {len(expertise_reports)}")
        if expertise_reports:
            print(f"[DEBUG] Expertise report: {expertise_reports[0]}")
        else:
            print("[DEBUG] No expertise reports found.") 

        expertise_report = expertise_reports[0] if expertise_reports else None

        if expertise_report:
            # Handle Boya & Kaporta Ekspertiz by checking if it's Boya & Kaporta Ekspertiz
            if expertise_report.expertise_type.name == "Boya & Kaporta Ekspertiz":
                # Get child expertise types (Boya Ekspertiz and Kaporta Ekspertiz)
                child_expertise_types = expertise_report.expertise_type.children

                boya_features = []
                kaporta_features = []
                boya_comment = ""
                kaporta_comment = ""

                # Iterate through child expertise types to extract Boya and Kaporta features
                for child_type in child_expertise_types:
                    if child_type.name == "Boya Ekspertiz":
                        # Filter features belonging to Boya Ekspertiz
                        for report in child_type.expertise_reports:
                            boya_features = [
                                {
                                    'name': feature.name,
                                    'status': feature.status,
                                    'image_path': url_for('static', filename=feature.image_path,
                                                          _external=True) if feature.image_path else None
                                } for feature in report.features
                            ]
                            boya_comment = report.comment

                    elif child_type.name == "Kaporta Ekspertiz":
                        # Filter features belonging to Kaporta Ekspertiz
                        for report in child_type.expertise_reports:
                            kaporta_features = [
                                {
                                    'name': feature.name,
                                    'status': feature.status,
                                    'image_path': url_for('static', filename=feature.image_path,
                                                          _external=True) if feature.image_path else None
                                } for feature in report.features
                            ]
                            kaporta_comment = report.comment

            # If it's a normal expertise report, add it as-is
            else:
                features_with_images = [
                    {
                        'name': feature.name,
                        'status': feature.status,
                        'image_path': url_for('static', filename=feature.image_path,
                                              _external=True) if feature.image_path else None
                    } for feature in expertise_report.features
                ]

                package_expertise_reports.append({
                    'expertise_type_name': expertise_report.expertise_type.name,
                    'comment': expertise_report.comment,
                    'features': features_with_images
                })

    # Combine Boya & Kaporta Ekspertiz into a single report
    if boya_features or kaporta_features:
        package_expertise_reports.append({
            'expertise_type_name': "Boya & Kaporta Ekspertiz",
            'boya_features': boya_features,
            'kaporta_features': kaporta_features,
            'boya_comment': boya_comment,
            'kaporta_comment': kaporta_comment
        })

    motor_image_url = url_for('static', filename='assets/pdf_imgs/motor_expertise.png', _external=True)
    fren_image_url = url_for('static', filename='assets/pdf_imgs/lastik.png', _external=True)
    info_image_url = url_for('static', filename='assets/pdf_imgs/info.png', _external=True)
    images = [
        {'filename': 'logo.jpeg', 'url': url_for('static', filename='assets/pdf_imgs/logo.jpeg', _external=True),
         'type': 'logo'},
        {'filename': 'motor_expertise.png',
         'url': url_for('static', filename='assets/pdf_imgs/motor_expertise.png', _external=True), 'type': 'motor'},
        {'filename': 'lastik.png', 'url': url_for('static', filename='assets/pdf_imgs/lastik.png', _external=True),
         'type': 'fren'},
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

    # Define the output directory and filename
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, 'pdfs')
    if not os.path.exists(directory):
        os.makedirs(directory)

    sanitized_customer_name = unidecode(customer.full_name.replace(" ", "_").replace("/", "_"))
    base_filename = os.path.join(directory, f"RAPOR_{sanitized_customer_name}.pdf")
    filename = os.path.join(directory, base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(directory, f"RAPOR_{sanitized_customer_name}_{counter}.pdf")
        counter += 1

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
