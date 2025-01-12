from ..database import db


class ExpertiseType(db.Model):
    __tablename__ = 'expertise_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('expertise_types.id'), nullable=True, index=True)

    expertise_reports = db.relationship('ExpertiseReport', back_populates='expertise_type', lazy=True)
    children = db.relationship('ExpertiseType', backref=db.backref('parent', remote_side=[id]), lazy=True)

    def __repr__(self):
        return f'{self.name}'


class ExpertiseReport(db.Model):
    __tablename__ = 'expertise_reports'
    id = db.Column(db.Integer, primary_key=True)
    expertise_type_id = db.Column(db.Integer, db.ForeignKey('expertise_types.id'), nullable=False, index=True)
    comment = db.Column(db.Text, nullable=True)

    expertise_type = db.relationship('ExpertiseType', back_populates='expertise_reports', lazy=True)
    features = db.relationship('ExpertiseFeature', back_populates='expertise_report', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<ExpertiseReport {self.expertise_type.name}>'


class ExpertiseFeature(db.Model):
    __tablename__ = 'expertise_features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    expertise_report_id = db.Column(db.Integer, db.ForeignKey('expertise_reports.id'), nullable=False, index=True)

    expertise_report = db.relationship('ExpertiseReport', back_populates='features', lazy=True)

    def __repr__(self):
        return f'<ExpertiseFeature {self.name} - {self.status}>'


class PackageExpertise(db.Model):
    __tablename__ = 'package_expertises'
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False, index=True)
    expertise_type_id = db.Column(db.Integer, db.ForeignKey('expertise_types.id'), nullable=False, index=True)

    package = db.relationship('Package', back_populates='package_expertises', lazy=True)
    expertise_type = db.relationship('ExpertiseType', lazy=True)

    def __repr__(self):
        return f'<PackageExpertise {self.package.name} - {self.expertise_type.name}>'