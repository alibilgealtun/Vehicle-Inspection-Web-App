import os
import sys

from dotenv import load_dotenv
from flask import Flask
from .database import db, migrate
from .models import (
    Address,    Agent, Appointment, Branch, Company,
    Customer, Package, Report, Staff, Vehicle, VehicleOwner,
    ExpertiseType, ExpertiseFeature, ExpertiseReport, PackageExpertise)
import logging
from logging.handlers import RotatingFileHandler
from .services.commands import register_commands
from .services.expertise_initializer import ExpertiseInitializer
from .tests.test_config import TestConfig
from .services.company_service import create_default_company
from .services.package_service import create_default_package

# Import blueprints
from .routes.appointments import appointments as appointments_bp
from .routes.customers import customers as customers_bp
from .routes.reports import reports as reports_bp
from .routes.staffs import staff as staff_bp
from .routes.main import main as main_bp
from .routes.branches import branches as branches_bp
from .routes.companies import companies as companies_bp
from .routes.errors import errors as errors_bp
from .routes.packages import packages as packages_bp
from .routes.pdfs import pdfs as pdfs_bp


def create_app(config_object=None):
    load_dotenv()
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    if config_object == 'testing':
        app.config.from_object(TestConfig)
        app.logger.setLevel(logging.DEBUG)

    else:
        app.config.from_object('config.Config')
        if not os.path.exists('logs'):
            os.mkdir('logs')
        app.logger.setLevel(logging.DEBUG)
        file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        app.logger.addHandler(stream_handler)


    logging.getLogger('fontTools.subset').setLevel(logging.WARNING)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://dbms:dbms123@localhost/flask_app')
    db.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        db.session.commit()
        ExpertiseInitializer.initialize_expertise_reports()  # Initialize expertise reports
        create_default_company() 
        create_default_package()

    register_commands(app)

    # Register blueprints here
    app.register_blueprint(pdfs_bp)
    app.register_blueprint(packages_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(branches_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(main_bp)

    return app
