from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Optional, Length
from ..enums import ReportStatus


class ReportForm(FlaskForm):
    # Customer Information
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=100)])
    customer_phone = StringField('Customer Phone', validators=[DataRequired(), Length(min=10, max=15)])
    customer_tax_no = StringField('Customer Tax No', validators=[Optional(), Length(max=11)])
    customer_email = StringField('Customer Email', validators=[Optional(), Length(max=100)])
    customer_address = TextAreaField('Customer Address', validators=[Optional(), Length(max=255)])

    # Owner Information
    owner_name = StringField('Owner Name', validators=[Optional(), Length(min=2, max=100)])
    owner_tax_no = StringField('Owner Tax No', validators=[Optional(), Length(max=11)])
    owner_phone = StringField('Owner Phone', validators=[Optional(), Length(min=10, max=15)])
    owner_address = TextAreaField('Owner Address', validators=[Optional(), Length(max=255)])

    # Vehicle Information
    vehicle_plate = StringField('Vehicle Plate', validators=[DataRequired(), Length(max=10)])
    brand = StringField('Brand', validators=[DataRequired(), Length(max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(max=50)])
    chassis_number = StringField('Chassis Number', validators=[DataRequired(), Length(max=17)])
    color = SelectField('Color', choices=[], validators=[DataRequired()])
    model_year = IntegerField('Model Year', validators=[DataRequired()])
    gear_type = SelectField('Gear Type', choices=[], validators=[DataRequired()])
    fuel_type = SelectField('Fuel Type', choices=[], validators=[DataRequired()])
    vehicle_km = IntegerField('Vehicle KM/Mileage', validators=[DataRequired()])
    engine_number = StringField('Engine Number', validators=[Optional(), Length(max=30)])

    # Inspection Information
    created_at = DateTimeField('Created At', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    inspection_date = DateTimeField('Inspection Date', validators=[Optional()], format='%Y-%m-%dT%H:%M')
    package_id = SelectField('Package ID', coerce=int, validators=[DataRequired()], choices=[])
    created_by = SelectField('Created By', coerce=int, validators=[DataRequired()], choices=[])
    registration_document_seen = BooleanField('Registration Document Seen')
    operation = StringField('Operation', validators=[Optional(), Length(max=255)])

    # Agent Information
    agent_name = StringField('Agent Name', validators=[Optional(), Length(min=2, max=100)])

    # Submit button
    submit = SubmitField('Create Report')
