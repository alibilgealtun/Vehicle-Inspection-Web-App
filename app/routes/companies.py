from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..forms import CompanyForm
from ..services.company_service import *

companies = Blueprint('companies', __name__)

@companies.route('/company')
def company_detail():
    company = get_first_company()
    form = CompanyForm()

    if company:
        form.name.data = company.name
        form.phone.data = company.phone
        form.fax.data = company.fax
        form.email.data = company.email
        form.website.data = company.website
        form.street_address.data = company.address.street_address
        form.city.data = company.address.city
        form.state.data = company.address.state
        form.postal_code.data = company.address.postal_code
        form.my_business_address_link.data = company.my_business_address_link

        # Get the first staff member from the first branch
        if company.branches:
            first_branch = company.branches[0]
            if first_branch.staff_members:
                first_staff = first_branch.staff_members[0]
                form.contact_name.data = f"{first_staff.first_name} {first_staff.last_name}"
                form.contact_phone.data = first_staff.phone_number

    return render_template('settings/settings.html', company=company, form=form)


@companies.route('/company/add', methods=['GET', 'POST'])
def add_company():
    form = CompanyForm()

    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'phone': form.phone.data,
            'fax': form.fax.data,
            'email': form.email.data,
            'website': form.website.data,
            'street_address': form.street_address.data,
            'city': form.city.data,
            'state': form.state.data,
            'postal_code': form.postal_code.data,
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
            'phone': form.phone.data,
            'fax': form.fax.data,
            'email': form.email.data,
            'website': form.website.data,
            'street_address': form.street_address.data,
            'city': form.city.data,
            'state': form.state.data,
            'postal_code': form.postal_code.data,
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
