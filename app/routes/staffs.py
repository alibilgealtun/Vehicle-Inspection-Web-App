from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Staff
from ..forms import StaffForm

staff = Blueprint('staff', __name__)


@staff.route('/staff')
def staff_list():
    staff_members = Staff.query.all()
    form = StaffForm()
    return render_template('staff/staff.html', staff=staff_members, form=form)


@staff.route('/staff/add', methods=['GET', 'POST'])
def add_staff():
    form = StaffForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)
        new_staff = Staff(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,  # Store the hashed password
            phone_number=form.phone_number.data,
            department="Default",
            role=form.role.data,
            branch_id=1
        )
        try:
            db.session.add(new_staff)
            db.session.commit()
            flash('Yeni personel başarıyla eklendi!', 'success')
            return redirect(url_for('staff.staff_list'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Tüm değerleri doğru girdiğinize emin olun!', 'error')
            print(f"IntegrityError: {e}")
    else:
        print(form.errors)
    staff_members = Staff.query.all()
    return render_template('staff/staff.html', staff=staff_members, form=form, modal_open=True)


@staff.route('/staff/edit/<int:id>', methods=['GET', 'POST'])
def edit_staff(id):
    staff_member = Staff.query.get_or_404(id)
    form = StaffForm(obj=staff_member)

    if form.validate_on_submit():
        print("Form data:", form.first_name.data, form.last_name.data, form.phone_number.data, form.role.data)  # Debugging line
        staff_member.first_name = form.first_name.data
        staff_member.last_name = form.last_name.data
        staff_member.phone_number = form.phone_number.data
        staff_member.role = form.role.data

        if form.password.data:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)
            staff_member.password = hashed_password

        try:
            db.session.commit()
            flash('Personel başarıyla güncellendi!', 'success')
            return redirect(url_for('staff.staff_list'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Güncelleme sırasında bir hata oluştu. Tüm değerleri doğru girdiğinize emin olun!', 'error')
            print(f"IntegrityError: {e}")
    else:
        print(form.errors)  # Debugging line

    return render_template('staff/staff.html', staff=Staff.query.all(), form=form)



@staff.route('/staff/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    staff_member = Staff.query.get_or_404(id)
    try:
        db.session.delete(staff_member)
        db.session.commit()
        flash('Personel başarıyla silindi!', 'success')
    except IntegrityError as e:
        db.session.rollback()
        flash('Silme sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'error')
        print(f"IntegrityError: {e}")

    return redirect(url_for('staff.staff_list'))
