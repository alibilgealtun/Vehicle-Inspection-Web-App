import logging

from app.database import db
from app.models import ExpertiseReport, ExpertiseFeature, ExpertiseType
from app.enums import ExpertiseTypeEnum, ExpertiseAnswer


class ExpertiseInitializer:

    @classmethod
    def load_expertise_map(cls, file_path='data/expertise_map.json'):
        from pathlib import Path
        import json

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        with file_path.open('r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def get_status_enum(cls, expertise_name):
        # Map expertise type to corresponding enum
        expertise_enum_map = {
            "Boya Ekspertiz": ExpertiseAnswer.PaintStatus,
            "Kaporta Ekspertiz": ExpertiseAnswer.BodyworkStatus,
            "Motor Ekspertiz": ExpertiseAnswer.ExpertiseStatus,
            "Yanal Kayma Ekspertiz": ExpertiseAnswer.IntStatus,
            "Süspansiyon Ekspertiz": ExpertiseAnswer.IntStatus,
            "Fren Ekspertiz": ExpertiseAnswer.IntStatus,
            "Yol Ekspertiz": ExpertiseAnswer.IntStatus,
            "Dyno Ekspertiz": ExpertiseAnswer.IntStatus,
            "Beyin Ekspertiz": ExpertiseAnswer.OBDStatus,
            "İç Ekspertiz": ExpertiseAnswer.ExpertiseStatus,
            "Dış Ekspertiz": ExpertiseAnswer.ExpertiseStatus,
            "Mekanik Ekspertiz": ExpertiseAnswer.ExpertiseStatus,
        }

        return expertise_enum_map.get(expertise_name)

    @classmethod
    def add_expertise_report(cls, expertise_name, parts_and_statuses, comment="", parent_name=None):
        # Find or create the parent expertise type if provided
        parent_expertise_type = None
        if parent_name:
            parent_expertise_type = ExpertiseType.query.filter_by(name=parent_name).first()
            if not parent_expertise_type:
                parent_expertise_type = ExpertiseType(name=parent_name)
                db.session.add(parent_expertise_type)
                db.session.commit()

        # Find or create the main expertise type
        expertise_type = ExpertiseType.query.filter_by(name=expertise_name).first()
        if not expertise_type:
            expertise_type = ExpertiseType(name=expertise_name, parent=parent_expertise_type)
            db.session.add(expertise_type)
            db.session.commit()
        else:
            existing_report = ExpertiseReport.query.filter_by(expertise_type=expertise_type).first()
            if existing_report:
                return False

        # Create the expertise report
        expertise_report = ExpertiseReport(expertise_type=expertise_type, comment=comment)
        db.session.add(expertise_report)
        db.session.commit()

        status_enum_class = cls.get_status_enum(expertise_name)

        for part in parts_and_statuses:
            status_value = part['default_status']

            if status_enum_class is None:
                status = status_value
            else:
                try:
                    status_enum = status_enum_class(status_value)
                    status = status_enum.value
                except ValueError:
                    raise ValueError(f"Status '{status_value}' not found in {status_enum_class.__name__} for expertise '{expertise_name}'")

            feature = ExpertiseFeature(name=part['part_name'], status=status, expertise_report=expertise_report)
            db.session.add(feature)

        db.session.commit()

        return True



    @classmethod
    def initialize_expertise_reports(cls):
        expertise_map = cls.load_expertise_map()

        # Define parent-child relationships
        parent_child_mapping = {
            "İç & Dış Ekspertiz": ["İç Ekspertiz", "Dış Ekspertiz"],
            "Yol & Dyno Ekspertiz": ["Yol Ekspertiz", "Dyno Ekspertiz"],
            "Boya & Kaporta Ekspertiz": ["Boya Ekspertiz", "Kaporta Ekspertiz"],
        }

        created_reports = []
        existing_reports = []

        for parent_name, children in parent_child_mapping.items():
            for child_name in children:
                parts_and_statuses = expertise_map.get(child_name, [])
                if cls.add_expertise_report(child_name, parts_and_statuses, parent_name=parent_name):
                    created_reports.append(f"{parent_name} - {child_name}")
                else:
                    existing_reports.append(f"{parent_name} - {child_name}")
        for expertise_name, parts_and_statuses in expertise_map.items():
            if expertise_name not in [child for children in parent_child_mapping.values() for child in children]:
                if cls.add_expertise_report(expertise_name, parts_and_statuses):
                    created_reports.append(f"{expertise_name} (Standalone)")
                else:
                    existing_reports.append(f"{expertise_name} (Standalone)")
        # Print a summary message
        if created_reports:
            print(f"Successfully created reports: {', '.join(created_reports)}")
        if existing_reports:
            print(f"Reports already exist: {', '.join(existing_reports)}")

