from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..database import db
from ..enums import FuelType, TransmissionType, Color, ReportStatus
from ..models import Report, Customer, Package, Staff, Vehicle, PackageExpertise, ExpertiseReport, ExpertiseType
from datetime import datetime
from ..services.enum_service import COLOR_MAPPING, TRANSMISSION_TYPE_MAPPING, FUEL_TYPE_MAPPING, map_to_enum
from ..services.report_service import (get_or_create_customer, create_report, get_or_create_vehicle_owner,
                                       get_or_create_agent, get_or_create_vehicle, get_or_create_staff_by_name)
from sqlalchemy.exc import IntegrityError
from ..forms.report_form import ReportForm


reports = Blueprint('reports', __name__)


@reports.route('/reports')
def report_list():
    page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
    per_page = request.args.get('per_page', 10, type=int)  # Items per page, default is 10
    paginated_reports = Report.query.filter_by(status=ReportStatus.OPENED).paginate(page=page, per_page=per_page, error_out=False)
    form = ReportForm()
    return render_template('report_sections/report_list.html', reports=paginated_reports.items, pagination=paginated_reports, form=form)


@reports.route('/report/add', methods=['GET', 'POST'])
def add_report():
    form = ReportForm()
    print("Initialized ReportForm", flush=True)

    # Define choices for the form fields
    fuel_types = [(fuel.name, fuel.value) for fuel in FuelType]
    transmission_types = [(transmission.name, transmission.value) for transmission in TransmissionType]
    colors = [(color.name, color.value) for color in Color]

    # Populate dynamic choices for SelectFields
    form.package_id.choices = [(pkg.id, pkg.name) for pkg in Package.query.all()]
    form.color.choices = colors
    form.gear_type.choices = transmission_types
    form.fuel_type.choices = fuel_types

    form.created_by.choices = [(staff.id, staff.full_name) for staff in Staff.query.all()]

    packages = Package.query.all()
    current_year = datetime.now().year

    form.created_at.data = datetime.now()
    form.inspection_date.data = datetime.now()

    vehicle_info = None  # Initialize vehicle_info

    if form.validate_on_submit():
        print(f"Form data: {form.data}", flush=True)

        try:
            # Create the Vehicle
            vehicle = get_or_create_vehicle({
                'vehicle_plate': form.vehicle_plate.data,
                'engine_number': form.engine_number.data,
                'brand': form.brand.data,
                'model': form.model.data,
                'chassis_number': form.chassis_number.data,
                'color': form.color.data,
                'model_year': form.model_year.data,
                'gear_type': form.gear_type.data,
                'fuel_type': form.fuel_type.data,
                'vehicle_km': form.vehicle_km.data,
            })
            print(f"Created vehicle: {vehicle}", flush=True)

            # Update vehicle_info for use in rendering the form
            vehicle_info = {
                'plate': vehicle.plate,
                'brand': vehicle.brand,
                'model': vehicle.model,
                'chassis_number': vehicle.chassis_number,
                'color': vehicle.color.value,
                'model_year': vehicle.model_year,
                'transmission_type': vehicle.transmission_type.value,
                'fuel_type': vehicle.fuel_type.value,
                'mileage': vehicle.mileage
            }
            print(f"Vehicle info updated: {vehicle_info}", flush=True)

            # Create or get the Customer with all provided data
            customer_data = {
                'customer_name': form.customer_name.data,
                'customer_phone': form.customer_phone.data,
                'customer_tax_no': form.customer_tax_no.data,
                'customer_email': form.customer_email.data,
                'customer_address': form.customer_address.data
            }
            customer = get_or_create_customer(customer_data)
            print(f"Created or retrieved customer: {customer}", flush=True)

            # Optionally create or get the VehicleOwner if the data is provided
            vehicle_owner = None
            if form.owner_name.data:
                vehicle_owner_data = {
                    'owner_name': form.owner_name.data,
                    'owner_tax_no': form.owner_tax_no.data,
                    'owner_phone': form.owner_phone.data,
                    'owner_address': form.owner_address.data
                }
                vehicle_owner = get_or_create_vehicle_owner(vehicle_owner_data)
                print(f"Created or retrieved vehicle owner: {vehicle_owner}", flush=True)

            # Optionally create or get the Agent if the name is provided
            agent = None
            if form.agent_name.data:
                agent = get_or_create_agent(form.agent_name.data)
                print(f"Created or retrieved agent: {agent}", flush=True)

            # Get or create the staff with name
            staff = Staff.query.get(form.created_by.data)
            print(f"Retrieved staff: {staff}", flush=True)

            # Create a new Report with the generated vehicle details
            new_report = create_report(
                inspection_date=form.inspection_date.data,
                vehicle_id=vehicle.id,
                customer_id=customer.id,
                package_id=form.package_id.data,
                operation=form.operation.data,
                created_by=staff.id,
                registration_document_seen=form.registration_document_seen.data
            )
            print(f"Created new report: {new_report}", flush=True)

            # Optionally link VehicleOwner to the report if it was created
            if vehicle_owner:
                vehicle_owner.report_id = new_report.id
                db.session.add(vehicle_owner)
                print(f"Linked vehicle owner to report: {vehicle_owner}", flush=True)

            # Optionally link Agent to the report if it was created
            if agent:
                agent.report_id = new_report.id
                db.session.add(agent)
                print(f"Linked agent to report: {agent}", flush=True)

            # Commit all changes
            db.session.commit()
            print("Database changes committed successfully", flush=True)

            flash('Rapor başarıyla oluşturuldu!', 'success')
            return redirect(url_for('reports.report_list'))

        except IntegrityError as e:
            db.session.rollback()
            flash('Tüm değerleri doğru girdiğinize emin olun!', 'error')
            print(f"IntegrityError: {e}", flush=True)

        except Exception as e:
            db.session.rollback()
            flash('Beklenmedik bir hata oluştu!', 'error')
            print(f"Unexpected Error: {e}", flush=True)

    else:
        print("Form validation failed", flush=True)
        print(f"Form errors: {form.errors}", flush=True)

    # Render the form with errors and vehicle info if available
    return render_template(
        'reports.html',
        form=form,
        fuel_types=fuel_types,
        transmission_types=transmission_types,
        colors=colors,
        vehicle_info=vehicle_info,
        packages=packages,
        current_year=current_year
    )


@reports.route('/report/update/<int:report_id>', methods=['GET', 'POST'])
def update_report(report_id):
    report = Report.query.get_or_404(report_id)
    form = ReportForm(obj=report)
    if form.validate_on_submit():
        form.populate_obj(report)

        try:
            db.session.commit()
            flash('Rapor başarıyla güncellendi!', 'success')
            return redirect(url_for('reports.report_list'))
        except IntegrityError as e:
            db.session.rollback()
            print("integrity err")
            flash(f'Tüm değerleri doğru girdiğinize emin olun!', 'error')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f'Beklenmedik bir hata oluştu!', 'error')

    # Retrieve necessary data for the form
    customers = Customer.query.all()
    packages = Package.query.all()
    staff_members = Staff.query.all()
    return render_template('report/update_report.html', form=form, customers=customers, packages=packages,
                           staff=staff_members)


@reports.route('/report/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report successfully deleted!')
    return redirect(url_for('reports.report_list'))


@reports.route('/report/cancel/<int:report_id>', methods=['POST'])
def cancel_report(report_id):
    report = Report.query.get_or_404(report_id)
    report.status = ReportStatus.CANCELLED
    db.session.commit()
    flash('Rapor başarıyla iptal edildi.', 'success')
    return redirect(url_for('reports.report_list'))


@reports.route('/report/complete/<int:report_id>', methods=['POST'])
def complete_report(report_id):
    # Here you can set the report to COMPLETED status if needed or navigate to the next page
    # report = Report.query.get_or_404(report_id)
    # report.status = ReportStatus.COMPLETED
    # db.session.commit()

    return redirect(url_for('reports.show_complete_report', report_id=report_id))


@reports.route('/report/complete_report/<int:report_id>')
def show_complete_report(report_id):
    report = Report.query.get_or_404(report_id)
    package_expertises = PackageExpertise.query.filter_by(package_id=report.package_id).all()

    # Fetch expertise reports through the package expertises
    expertise_reports = ExpertiseReport.query.filter(
        ExpertiseReport.expertise_type_id.in_([pe.expertise_type_id for pe in package_expertises])
    ).all()

    # Add this line to include the package's expertises
    package_expertise_types = [pe.expertise_type for pe in package_expertises]

    return render_template('report_sections/complete_report.html', report=report, package_expertises=package_expertises, expertise_reports=expertise_reports, package_expertise_types=package_expertise_types)


@reports.route('/report/expertise_detail_ajax', methods=['GET'])
def expertise_detail_ajax():
    expertise_type = request.args.get('expertise_type')
    print("Ekspertiz tipi:", expertise_type)
    report_id = request.args.get('report_id')

    # Retrieve the report
    report = Report.query.get_or_404(report_id)

    # Find the corresponding PackageExpertise
    package_expertise = PackageExpertise.query.filter_by(package_id=report.package_id).join(ExpertiseType).filter(ExpertiseType.name == expertise_type).first()

    if not package_expertise:
        return jsonify({"error": "Invalid expertise type or package does not include this expertise type"}), 400

    # Fetch the ExpertiseReport using expertise_type_id
    expertise_report = ExpertiseReport.query.filter_by(expertise_type_id=package_expertise.expertise_type_id).first()
    expertise_report2 = None

    if not expertise_report:
        return jsonify({"error": "Expertise report not found"}), 404

    # Handle combined expertise reports
    if expertise_type == "İç & Dış Ekspertiz":
        ic_expertise_type_id = ExpertiseType.query.filter_by(name="İç Ekspertiz").first().id
        dis_expertise_type_id = ExpertiseType.query.filter_by(name="Dış Ekspertiz").first().id

        expertise_report = ExpertiseReport.query.filter_by(expertise_type_id=ic_expertise_type_id).first()
        expertise_report2 = ExpertiseReport.query.filter_by(expertise_type_id=dis_expertise_type_id).first()
    elif expertise_type == "Yol & Dyno Ekspertiz":
        dyno_expertise_type_id = ExpertiseType.query.filter_by(name="Dyno Ekspertiz").first().id
        yol_expertise_type_id = ExpertiseType.query.filter_by(name="Yol Ekspertiz").first().id

        expertise_report = ExpertiseReport.query.filter_by(expertise_type_id=dyno_expertise_type_id).first()
        expertise_report2 = ExpertiseReport.query.filter_by(expertise_type_id=yol_expertise_type_id).first()
    elif expertise_type == "Boya & Kaporta Ekspertiz":
        boya_expertise_type_id = ExpertiseType.query.filter_by(name="Boya Ekspertiz").first().id
        kaporta_expertise_type_id = ExpertiseType.query.filter_by(name="Kaporta Ekspertiz").first().id

        expertise_report = ExpertiseReport.query.filter_by(expertise_type_id=boya_expertise_type_id).first()
        expertise_report2 = ExpertiseReport.query.filter_by(expertise_type_id=kaporta_expertise_type_id).first()

    expertise_template_map = {
        "Motor Ekspertiz": "report_sections/expertises/motor_expertise.html",
        "Kaporta Ekspertiz": "report_sections/expertises/kaporta_expertise.html",
        "Beyin Ekspertiz": "report_sections/expertises/beyin_expertise.html",
        "Mekanik Ekspertiz": "report_sections/expertises/mekanik_expertise.html",
        "Süspansiyon Ekspertiz": "report_sections/expertises/suspansiyon_expertise.html",
        "Yanal Kayma Ekspertiz": "report_sections/expertises/yanal_expertise.html",
        "Fren Ekspertiz": "report_sections/expertises/fren_expertise.html",
        "Boya Ekspertiz": "report_sections/expertises/boya_expertise.html",
        "Yol Ekspertiz": "report_sections/expertises/yol_expertise.html",
        "Dyno Ekspertiz": "report_sections/expertises/dyno_expertise.html",
        "İç & Dış Ekspertiz": "report_sections/expertises/ic_dis_expertise.html",
        "İç Ekspertiz": "report_sections/expertises/ic_dis_expertise.html",
        "Dış Ekspertiz": "report_sections/expertises/dis_expertise.html",
        "Yol & Dyno Ekspertiz": "report_sections/expertises/dyno_expertise.html",
        "Boya & Kaporta Ekspertiz": "report_sections/expertises/boya_kaporta_expertise.html",
    }

    template_path = expertise_template_map.get(expertise_type)

    if not template_path:
        return jsonify({"error": "Invalid expertise type"}), 400

    return render_template(template_path, report=report, expertise_report=expertise_report, expertise_report2=expertise_report2)






@reports.route('/report/expertise/<int:expertise_report_id>', methods=['GET', 'POST'])
def expertise_detail(expertise_report_id):

    expertise_report = ExpertiseReport.query.get_or_404(expertise_report_id)

    expertise_report2_id = request.form.get('expertise_report2_id')

    expertise_report2 = None
    if expertise_report2_id:
        expertise_report2 = ExpertiseReport.query.get(expertise_report2_id)

    if request.method == 'POST':
        try:
            reports_to_update = [expertise_report]
            if expertise_report2:
                reports_to_update.append(expertise_report2)

            status_directory_map = {
                'ORİJİNAL': 'orijinal',
                'PLASTİK': 'plastik',
                'BOYALI': 'boyalı',
                'LOKAL BOYALI': 'lokal_boyalı',
                'DEĞİŞMİŞ': 'değişmiş',
                'KAPLAMA': 'kaplama',
                'YOK': 'yok',
            }

            for report in reports_to_update:
                for feature in report.features:
                    new_status = request.form.get(f'feature_{feature.id}')
                    print(f'Feature {feature.id}: Current Status = {feature.status}, New Status = {new_status}',
                          flush=True)

                    if new_status and new_status != feature.status:
                        feature.status = new_status
                        feature.image_path = f'assets/car_parts/{status_directory_map.get(new_status, "default")}/{feature.name}.png'
                        db.session.add(feature)
                        print(f'Feature {feature.id} updated to {new_status}', flush=True)

                # Update comments if present
                new_comment = request.form.get('technician_comment')
                if new_comment is not None and new_comment != report.comment:
                    report.comment = new_comment
                    print(f'Comment updated for report {report.id}', flush=True)


            db.session.commit()
            print('Changes committed successfully', flush=True)
            return jsonify({"success": True}), 200
        except Exception as e:
            db.session.rollback()
            print(f'Error: {str(e)}', flush=True)
            return jsonify({"success": False, "error": str(e)}), 500

    return render_template('report_sections/complete_report.html', expertise_report=expertise_report,
                           expertise_report2=expertise_report2)

