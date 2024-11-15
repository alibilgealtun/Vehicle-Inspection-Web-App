from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import db
from ..models import Branch, Company

branches = Blueprint('branches', __name__)

@branches.route('/branches')
def branch_list():
    branches = Branch.query.all()
    return render_template('branch/branch_list.html', branches=branches)

@branches.route('/branch/add', methods=['GET', 'POST'])
def add_branch():
    if request.method == 'POST':
        name = request.form['name']
        company_id = request.form['company_id']
        address = request.form.get('address')
        phone_1 = request.form.get('phone_1')
        phone_2 = request.form.get('phone_2')
        fax = request.form.get('fax')
        email = request.form.get('email')

        new_branch = Branch(
            name=name,
            company_id=company_id,
            address=address,
            phone_1=phone_1,
            phone_2=phone_2,
            fax=fax,
            email=email
        )
        db.session.add(new_branch)
        db.session.commit()
        flash('New branch successfully created!')
        return redirect(url_for('branches.branch_list'))

    companies = Company.query.all()
    return render_template('branch/add_branch.html', companies=companies)

@branches.route('/branch/update/<int:branch_id>', methods=['GET', 'POST'])
def update_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)

    if request.method == 'POST':
        branch.name = request.form['name']
        branch.company_id = request.form['company_id']
        branch.address = request.form.get('address')
        branch.phone_1 = request.form.get('phone_1')
        branch.phone_2 = request.form.get('phone_2')
        branch.fax = request.form.get('fax')
        branch.email = request.form.get('email')

        db.session.commit()
        flash('Branch successfully updated!')
        return redirect(url_for('branches.branch_list'))

    companies = Company.query.all()
    return render_template('branch/update_branch.html', branch=branch, companies=companies)

@branches.route('/branch/delete/<int:branch_id>', methods=['POST'])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    flash('Branch successfully deleted!')
    return redirect(url_for('branches.branch_list'))
