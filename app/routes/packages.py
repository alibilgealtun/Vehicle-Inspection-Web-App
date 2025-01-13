from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import db
from app.models import Report, ExpertiseType, PackageExpertise, Package
from app.forms import PackageForm
from app.services.package_service import get_expertises

packages = Blueprint('packages', __name__, url_prefix='/packages')

@packages.route('/', methods=['GET', 'POST'])
def packages_list():
    form = PackageForm(request.form)
    packs = Package.query.all()
    expertises = ExpertiseType.query.all()  # to show all as a choice
    expertise_choices = [(str(expertise.id), expertise.name) for expertise in expertises]
    return render_template('packages.html', form=form, packages=packs, get_expertises=get_expertises, expertises=expertises)

@packages.route('/add', methods=['GET', 'POST'])
def add_pckg():
    expertises = ExpertiseType.query.all()  # to show all as a choice
    expertise_choices = [(str(expertise.id), expertise.name) for expertise in expertises]

    form = PackageForm(request.form)
    form.contents.choices = expertise_choices  # Set choices for SelectMultipleField dynamically

    if request.method == 'POST' and form.validate_on_submit():
        # Create a new package instance
        new_package = Package(
            name=form.name.data,
            price=form.price.data,
            active=form.active.data == 'active'  # Convert to Boolean
        )

        # Add the new package to the database session
        db.session.add(new_package)
        db.session.flush()  # Flush to generate the package ID

        # Add the selected expertises to the package
        selected_expertises = form.contents.data
        for expertise_id in selected_expertises:
            package_expertise = PackageExpertise(
                package_id=new_package.id,  # Use the new package ID
                expertise_type_id=int(expertise_id)
            )
            db.session.add(package_expertise)

        # Commit all changes to the database
        db.session.commit()

        #flash('Paket başarıyla oluşturuldu!', 'success')
        return redirect(url_for('packages.packages_list'))
    else:
        print(form.errors)
        #flash('Formu doğru doldurduğunuza emin olun!', 'error')
        return redirect(url_for('packages.packages_list'))


@packages.route('/update/<int:package_id>', methods=['GET', 'POST'])
def update_package(package_id):
    package = Package.query.get_or_404(package_id)
    expertises = ExpertiseType.query.all()
    expertise_choices = [(str(expertise.id), expertise.name) for expertise in expertises]

    form = PackageForm(request.form)
    form.contents.choices = expertise_choices

    if request.method == 'POST' and form.validate_on_submit():
        package.name = form.name.data
        package.price = form.price.data
        package.active = form.active.data == 'active'

        # Clear existing package expertises
        PackageExpertise.query.filter_by(package_id=package.id).delete()

        # Add the updated expertises
        selected_expertises = form.contents.data
        for expertise_id in selected_expertises:
            package_expertise = PackageExpertise(
                package_id=package.id,
                expertise_type_id=int(expertise_id)
            )
            db.session.add(package_expertise)

        db.session.commit()
        #flash('Paket başarıyla güncellendi!', 'success')
        return redirect(url_for('packages.packages_list'))

    # Check for an AJAX request
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return {
            'id': package.id,
            'name': package.name,
            'price': package.price,
            'contents': [str(pe.expertise_type_id) for pe in package.package_expertises],
            'active': 'active' if package.active else 'inactive'
        }

    # Pre-populate the form with existing data for regular form handling
    form.name.data = package.name
    form.price.data = package.price
    form.contents.data = [str(pe.expertise_type_id) for pe in package.package_expertises]
    form.active.data = 'active' if package.active else 'inactive'

    return render_template('packages.html', form=form, expertises=expertises, update=True)

@packages.route('/delete/<int:package_id>', methods=['POST'])
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)

    # Check if any reports are associated with this package
    associated_reports = Report.query.filter_by(package_id=package_id).all()

    if associated_reports:
        #flash('Bu paket birden fazla raporda kullanıldığı için silinemez!', 'danger')
        return redirect(url_for('packages.packages_list'))

    db.session.delete(package)
    db.session.commit()
    #flash('Paket başarıyla silindi!', 'success')

    return redirect(url_for('packages.packages_list'))
