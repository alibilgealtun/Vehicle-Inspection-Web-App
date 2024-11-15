from flask import Blueprint, render_template, jsonify, current_app
from werkzeug.exceptions import HTTPException

from ..database import db

errors = Blueprint('errors', __name__)

# 404 Not Found
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# 500 Internal Server Error
@errors.app_errorhandler(500)
def error_500(error):
    db.session.rollback()  # Rollback any failed database transactions
    return render_template('errors/500.html'), 500

# 403 Forbidden
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# 400 Bad Request (Optional)
@errors.app_errorhandler(400)
def error_400(error):
    return render_template('errors/400.html'), 400


@errors.app_errorhandler(Exception)
def handle_exception(error):
    # If the error is an HTTPException, use its code
    if isinstance(error, HTTPException):
        return error_500(error)
    # Otherwise, return a 500 Internal Server Error
    current_app.logger.error(f'Unhandled Exception: {str(error)}')
    return render_template('errors/500.html'), 500
