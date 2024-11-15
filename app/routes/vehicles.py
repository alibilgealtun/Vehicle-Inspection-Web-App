from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Vehicle

vehicles = Blueprint('vehicles', __name__)

@vehicles.route('/vehicles')
def vehicle_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_vehicles = Vehicle.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('vehicle/vehicle_list.html', vehicles=paginated_vehicles.items, pagination=paginated_vehicles)

@vehicles.route('/vehicle/add', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        plate = request.form['plate']
        engine_number = request.form['engine_number']
        brand = request.form['brand']
        model = request.form['model']
        chassis_number = request.form['chassis_number']
        color = request.form['color']
        model_year = int(request.form['model_year'])
        transmission_type = request.form['transmission_type']
        fuel_type = request.form['fuel_type']
        mileage = int(request.form['mileage'])
        report_id = int(request.form['report_id'])

        new_vehicle = Vehicle(
            plate=plate,
            engine_number=engine_number,
            brand=brand,
            model=model,
            chassis_number=chassis_number,
            color=color,
            model_year=model_year,
            transmission_type=transmission_type,
            fuel_type=fuel_type,
            mileage=mileage,
            report_id=report_id
        )
        db.session.add(new_vehicle)
        db.session.commit()
        flash('New vehicle successfully created!')
        return redirect(url_for('vehicles.vehicle_list'))

    return render_template('vehicle/add_vehicle.html')

@vehicles.route('/vehicle/update/<int:vehicle_id>', methods=['GET', 'POST'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == 'POST':
        vehicle.plate = request.form['plate']
        vehicle.engine_number = request.form['engine_number']
        vehicle.brand = request.form['brand']
        vehicle.model = request.form['model']
        vehicle.chassis_number = request.form['chassis_number']
        vehicle.color = request.form['color']
        vehicle.model_year = int(request.form['model_year'])
        vehicle.transmission_type = request.form['transmission_type']
        vehicle.fuel_type = request.form['fuel_type']
        vehicle.mileage = int(request.form['mileage'])
        vehicle.report_id = int(request.form['report_id'])

        db.session.commit()
        flash('Vehicle successfully updated!')
        return redirect(url_for('vehicles.vehicle_list'))

    return render_template('vehicle/update_vehicle.html', vehicle=vehicle)

@vehicles.route('/vehicle/delete/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle successfully deleted!')
    return redirect(url_for('vehicles.vehicle_list'))
