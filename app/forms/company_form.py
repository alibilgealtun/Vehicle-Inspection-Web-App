from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, URL


class CompanyForm(FlaskForm):
    name = StringField('Firma Adı', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Telefon', validators=[Optional(), Length(max=15)])
    fax = StringField('Faks', validators=[Optional(), Length(max=15)])
    email = StringField('E-posta', validators=[Optional(), Email(), Length(max=100)])
    website = StringField('Web Site', validators=[Optional(), URL(), Length(max=100)])
    street_address = StringField('Adres', validators=[Optional(), Length(max=255)])
    city = StringField('Şehir', validators=[DataRequired(), Length(max=100)])
    state = StringField('Eyalet', validators=[Optional(), Length(max=100)])
    postal_code = StringField('Posta Kodu', validators=[Optional(), Length(max=20)])
    my_business_address_link = StringField('My Business Adres Linki', validators=[Optional(), URL(), Length(max=255)])
    contact_name = StringField('Adı ve Soyadı', validators=[Optional(), Length(max=100)])
    contact_phone = StringField('Cep Telefonu', validators=[Optional(), Length(max=15)])
    submit = SubmitField('KAYDET')
