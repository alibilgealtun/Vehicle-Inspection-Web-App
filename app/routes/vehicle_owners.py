from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import VehicleOwner

vehicle_owners = Blueprint('vehicle_owners', __name__)

@vehicle_owners.route('/vehicle_owners')
def vehicle_owner_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_vehicle_owners = VehicleOwner.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('vehicle_owner/vehicle_owner_list.html', vehicle_owners=paginated_vehicle_owners.items, pagination=paginated_vehicle_owners)

@vehicle_owners.route('/vehicle_owner/add', methods=['GET', 'POST'])
def add_vehicle_owner():
    if request.method == 'POST':
        full_name = request.form['full_name']
        tc_tax_number = request.form['tc_tax_number']
        phone_number = request.form['phone_number']
        address = request.form['address']
        report_id = int(request.form['report_id'])

        new_vehicle_owner = VehicleOwner(
            full_name=full_name,
            tc_tax_number=tc_tax_number,
            phone_number=phone_number,
            address=address,
            report_id=report_id
        )
        db.session.add(new_vehicle_owner)
        db.session.commit()
        flash('New vehicle owner successfully created!')
        return redirect(url_for('vehicle_owners.vehicle_owner_list'))

    return render_template('vehicle_owner/add_vehicle_owner.html')

@vehicle_owners.route('/vehicle_owner/update/<int:vehicle_owner_id>', methods=['GET', 'POST'])
def update_vehicle_owner(vehicle_owner_id):
    vehicle_owner = VehicleOwner.query.get_or_404(vehicle_owner_id)

    if request.method == 'POST':
        vehicle_owner.full_name = request.form['full_name']
        vehicle_owner.tc_tax_number = request.form['tc_tax_number']
        vehicle_owner.phone_number = request.form['phone_number']
        vehicle_owner.address = request.form['address']
        vehicle_owner.report_id = int(request.form['report_id'])

        db.session.commit()
        flash('Vehicle owner successfully updated!')
        return redirect(url_for('vehicle_owners.vehicle_owner_list'))

    return render_template('vehicle_owner/update_vehicle_owner.html', vehicle_owner=vehicle_owner)

@vehicle_owners.route('/vehicle_owner/delete/<int:vehicle_owner_id>', methods=['POST'])
def delete_vehicle_owner(vehicle_owner_id):
    vehicle_owner = VehicleOwner.query.get_or_404(vehicle_owner_id)
    db.session.delete(vehicle_owner)
    db.session.commit()
    flash('Vehicle owner successfully deleted!')
    return redirect(url_for('vehicle_owners.vehicle_owner_list'))
