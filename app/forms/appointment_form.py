from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from datetime import date, time


class AppointmentForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=100, message="Lütfen isim girin.")])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=9, max=15, message="Telefon numarası 9 ile 15 karakter arasında olmalıdır.")
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    brand = StringField('Brand', validators=[Optional(), Length(min=2, max=50)])
    model = StringField('Model', validators=[Optional(), Length(min=2, max=50)])
    reminder_sent = BooleanField('Reminder Sent')
    submit = SubmitField('Add Appointment')

    def validate_date(self, date_input):
        if date_input.data < date.today():
            print("Validation error: Date is in the past.")
            raise ValidationError('The appointment date cannot be in the past.')
