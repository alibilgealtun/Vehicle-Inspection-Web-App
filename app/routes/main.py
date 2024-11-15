from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Home Page
@main.route('/')
def index():
    return render_template('home.html')
