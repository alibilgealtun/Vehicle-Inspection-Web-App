from ..database import db


class ExpertiseType(db.Model):
    # ExpertiseType defines the type of expertise (e.g., Kaporta, Boya) and can be associated with multiple ExpertiseR.
    __tablename__ = 'expertise_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('expertise_types.id'), nullable=True)

    # Relationship to associate expertise type with multiple ExpertiseReports
    expertise_reports = db.relationship('ExpertiseReport', back_populates='expertise_type')
    children = db.relationship('ExpertiseType', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f'<ExpertiseType {self.name}>'


class ExpertiseReport(db.Model):
    __tablename__ = 'expertise_reports'
    id = db.Column(db.Integer, primary_key=True)
    expertise_type_id = db.Column(db.Integer, db.ForeignKey('expertise_types.id'), nullable=False)
    comment = db.Column(db.Text, nullable=True)

    # Relationships
    expertise_type = db.relationship('ExpertiseType', back_populates='expertise_reports')
    features = db.relationship('ExpertiseFeature', back_populates='expertise_report')
    # package_expertise = db.relationship('PackageExpertise', back_populates='expertise_reports')

    def __repr__(self):
        return f'<ExpertiseReport {self.expertise_type.name}>'


class ExpertiseFeature(db.Model):
    __tablename__ = 'expertise_features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    expertise_report_id = db.Column(db.Integer, db.ForeignKey('expertise_reports.id'), nullable=False)

    # Relationship back to ExpertiseReport
    expertise_report = db.relationship('ExpertiseReport', back_populates='features')

    def __repr__(self):
        return f'<ExpertiseFeature {self.name} - {self.status}>'



class PackageExpertise(db.Model):
    # Model between package & expertise types
    __tablename__ = 'package_expertises'
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    expertise_type_id = db.Column(db.Integer, db.ForeignKey('expertise_types.id'), nullable=False)

    # Relationships
    package = db.relationship('Package', back_populates='package_expertises')
    expertise_type = db.relationship('ExpertiseType')
    # expertise_reports = db.relationship('ExpertiseReport', back_populates='package_expertise')

    def __repr__(self):
        return f'<PackageExpertise {self.package.name} - {self.expertise_type.name}>'
