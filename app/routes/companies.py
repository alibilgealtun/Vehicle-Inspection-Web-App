from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..forms import CompanyForm
from ..services.company_service import *

companies = Blueprint('companies', __name__)

@companies.route('/company')
def company_detail():
    company = get_first_company()
    form = CompanyForm(obj=company)
    return render_template('settings/settings.html', company=company, form=form)


@companies.route('/company/add', methods=['GET', 'POST'])
def add_company():
    form = CompanyForm()

    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'phone_1': form.phone_1.data,
            'phone_2': form.phone_2.data,
            'fax': form.fax.data,
            'email': form.email.data,
            'website': form.website.data,
            'address': form.address.data,
            'my_business_address_link': form.my_business_address_link.data,
        }
        create_company(data)
        flash('New company successfully created!', 'success')
        return redirect(url_for('companies.company_detail'))

    return render_template('settings/add_company.html', form=form)


@companies.route('/company/update', methods=['GET', 'POST'])
def update_company():
    company = get_first_company()

    if not company:
        company = create_default_company()
        flash('Default company created. Please update the details.', 'warning')

    form = CompanyForm(obj=company)

    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'phone_1': form.phone_1.data,
            'phone_2': form.phone_2.data,
            'fax': form.fax.data,
            'email': form.email.data,
            'website': form.website.data,
            'address': form.address.data,
            'my_business_address_link': form.my_business_address_link.data,
        }
        update_company_service(company, data)
        flash('Company successfully updated!', 'success')
        return redirect(url_for('companies.company_detail'))

    return render_template('settings/settings.html', form=form, company=company)


@companies.route('/company/delete', methods=['POST'])
def delete_company():
    company = get_first_company()
    if company:
        delete_company(company)
        flash('Company successfully deleted!', 'success')
    else:
        flash('No company found to delete.', 'danger')
    return redirect(url_for('companies.company_detail'))
