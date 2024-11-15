from flask import Flask
from app.services.expertise_initializer import ExpertiseInitializer

def register_commands(app: Flask):
    @app.cli.command("init-expertise")
    def init_expertise():
        """Initialize the database with expertise reports."""
        ExpertiseInitializer.initialize_expertise_reports()
