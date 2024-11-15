from flask import Blueprint, render_template, request
from ..models import Customer

customers = Blueprint('customers', __name__)

# Customer List with Pagination
@customers.route('/customers')
def customer_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of customers per page
    paginated_customers = Customer.query.paginate(page=page, per_page=per_page)

    return render_template('customers.html', paginated_customers=paginated_customers)
