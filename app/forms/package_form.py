from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired

class PackageForm(FlaskForm):
    name = StringField('Paket Adı', validators=[DataRequired()])
    price = DecimalField('Paket Fiyatı', validators=[DataRequired()])
    contents = SelectMultipleField('Uygulanan Ekspertizler', validators=[DataRequired()])
    active = SelectField('Paket Durumu', choices=[('active', 'Aktif'), ('inactive', 'Pasif')])
