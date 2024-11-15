from werkzeug.security import check_password_hash


def verify_login(staff, password):
    return check_password_hash(staff.password, password)
